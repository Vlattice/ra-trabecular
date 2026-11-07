"""
Synthetic dataset generation for the early-warning task.

Each sample is a snapshot of an eroded network. Its label is the remaining
erosion budget before the network crosses the percolation transition:

    delta = p_c - p

where ``p`` is the fraction of struts removed so far and ``p_c`` is the
trajectory's critical erosion fraction, defined as the (interpolated) point
at which the percolation order parameter P_inf first drops below 0.5.
``delta > 0`` means the network is still mechanically connected.

Networks are drawn with heterogeneous generation parameters (seed density,
strut thickness, anisotropy, seed distribution), so that the initial bone
volume fraction varies between "individuals". Without this variation a
density-only model could trivially recover ``p`` from BV/TV.

Likewise, every Poisson–Voronoi network starts with nearly the same mean
coordination (z ≈ 3.8), so a topology model could read ``p`` directly from
the mean degree. To prevent this, each "healthy" network is first pruned by
a random fraction of struts (``initial_pruning``), so that individuals also
differ in their baseline connectivity. ``p`` and ``p_c`` are measured
relative to this individual baseline.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

import numpy as np

from ..voronoi import generate_voronoi_network, load_bearing_subnetwork
from ..erosion import progressive_erosion, ErosionRegime
from ..connectivity import percolation_order_parameter
from ..irce import compute_irce
from .features import structural_features


@dataclass(frozen=True)
class GenerationRanges:
    """Ranges from which per-network generation parameters are drawn."""
    n_seeds: tuple = (120, 260)
    mean_thickness: tuple = (0.10, 0.20)
    anisotropy_factor: tuple = (1.0, 2.0)
    domain_size: float = 10.0
    perturbed_lattice_prob: float = 0.3
    initial_pruning: tuple = (0.0, 0.25)


def critical_fraction(p: np.ndarray, p_inf: np.ndarray, threshold: float = 0.5) -> float:
    """
    Erosion fraction at which ``p_inf`` first drops below ``threshold``,
    linearly interpolated between steps. Returns ``nan`` if it never does.
    """
    below = np.flatnonzero(p_inf < threshold)
    if below.size == 0:
        return float("nan")
    i = int(below[0])
    if i == 0:
        return float(p[0])
    p0, p1 = p[i - 1], p[i]
    y0, y1 = p_inf[i - 1], p_inf[i]
    if y0 == y1:
        return float(p1)
    return float(p0 + (y0 - threshold) * (p1 - p0) / (y0 - y1))


def _simulate_network(
    net_id: int,
    seed: int,
    regimes: Sequence[ErosionRegime],
    n_steps: int,
    max_removal_fraction: float,
    ranges: GenerationRanges,
    include_irce: bool,
) -> List[dict]:
    """Generate one heterogeneous healthy network and all its trajectories."""
    rng = np.random.default_rng(seed)
    params = dict(
        n_seeds=int(rng.integers(*ranges.n_seeds)),
        mean_thickness=float(rng.uniform(*ranges.mean_thickness)),
        anisotropy_factor=float(rng.uniform(*ranges.anisotropy_factor)),
        seed_distribution=(
            "perturbed_lattice"
            if rng.random() < ranges.perturbed_lattice_prob else "uniform"
        ),
    )
    base = generate_voronoi_network(
        domain_size=ranges.domain_size,
        thickness_std=0.2 * params["mean_thickness"],
        rng_seed=int(rng.integers(2**31)),
        **params,
    )
    params["initial_pruning"] = float(rng.uniform(*ranges.initial_pruning))
    if params["initial_pruning"] > 0:
        healthy = progressive_erosion(
            base, n_steps=2,
            max_removal_fraction=params["initial_pruning"],
            regime=ErosionRegime.UNIFORM,
            rng_seed=int(rng.integers(2**31)),
        )[-1].network
        healthy = load_bearing_subnetwork(healthy)
    else:
        healthy = base
    n_ref_nodes = healthy.graph.number_of_nodes()

    rows: List[dict] = []
    for regime in regimes:
        traj = progressive_erosion(
            healthy, n_steps=n_steps,
            max_removal_fraction=max_removal_fraction,
            regime=regime, rng_seed=int(rng.integers(2**31)),
        )
        p = np.array([s.p_removed for s in traj])
        p_inf = np.array([
            percolation_order_parameter(s.network, n_ref_nodes) for s in traj
        ])
        p_c = critical_fraction(p, p_inf)

        for state, p_i, pinf_i in zip(traj, p, p_inf):
            row = {
                "network_id": net_id,
                "regime": regime.value,
                "p": float(p_i),
                "p_c": p_c,
                "delta": p_c - float(p_i),
                "p_inf": float(pinf_i),
                **{f"gen_{k}": v for k, v in params.items()},
                **structural_features(state.network),
            }
            if include_irce:
                row["irce"] = compute_irce(state.network, healthy).irce
            rows.append(row)
    return rows


def generate_dataset(
    n_networks: int = 60,
    regimes: Sequence[ErosionRegime] = tuple(ErosionRegime),
    n_steps: int = 37,
    max_removal_fraction: float = 0.9,
    ranges: GenerationRanges = GenerationRanges(),
    rng_seed: Optional[int] = 0,
    include_irce: bool = True,
    n_jobs: int = 1,
):
    """
    Generate a synthetic early-warning dataset.

    Parameters
    ----------
    n_networks : int
        Number of independent healthy networks ("individuals").
    regimes : sequence of ErosionRegime
        Erosion regimes applied to every network.
    n_steps, max_removal_fraction : int, float
        Trajectory resolution and extent.
    ranges : GenerationRanges
        Parameter ranges for heterogeneous network generation.
    rng_seed : int, optional
        Master seed for reproducibility. Results do not depend on ``n_jobs``.
    include_irce : bool
        Also store the (reference-based) IRCE, for comparison only.
    n_jobs : int
        Number of parallel worker processes (``-1`` = all cores).

    Returns
    -------
    pandas.DataFrame
        One row per snapshot with columns: ``network_id``, ``regime``, ``p``,
        ``p_c``, ``delta``, ``p_inf``, optionally ``irce``, the generation
        parameters (``gen_*``), and every feature in
        :data:`ra_trabecular.ml.features.ALL_FEATURES`.
    """
    import pandas as pd
    from joblib import Parallel, delayed

    seeds = np.random.default_rng(rng_seed).integers(2**31, size=n_networks)
    regimes = tuple(regimes)
    chunks = Parallel(n_jobs=n_jobs)(
        delayed(_simulate_network)(
            i, int(seeds[i]), regimes, n_steps, max_removal_fraction,
            ranges, include_irce,
        )
        for i in range(n_networks)
    )
    df = pd.DataFrame([row for chunk in chunks for row in chunk])
    return df[np.isfinite(df["p_c"])].reset_index(drop=True)
