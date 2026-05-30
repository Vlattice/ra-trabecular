"""
Progressive erosion models for simulating trabecular bone degradation.

Implements three erosion regimes:
  1. Uniform random edge removal (control).
  2. Peripheral / curvature-weighted removal (RA-driven inflammatory erosion).
  3. Coupled removal driven by a simulated osteoclastic activity field.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import copy
import numpy as np

from .voronoi import TrabecularNetwork


class ErosionRegime(str, Enum):
    UNIFORM = "uniform"
    PERIPHERAL = "peripheral"
    OSTEOCLASTIC = "osteoclastic"


@dataclass
class ErosionState:
    """A single state along an erosion trajectory."""
    network: TrabecularNetwork
    p_removed: float           # Fraction of edges removed so far
    n_removed: int             # Number of edges removed
    n_remaining: int           # Number of edges remaining
    regime: ErosionRegime
    step: int


def _edge_midpoints(network: TrabecularNetwork) -> np.ndarray:
    """Compute midpoint of each edge."""
    edges = np.array(network.edges)
    return 0.5 * (network.nodes[edges[:, 0]] + network.nodes[edges[:, 1]])


def _peripheral_weights(network: TrabecularNetwork) -> np.ndarray:
    """
    Compute removal weights biased toward the periphery of the domain.

    Models the spatial pattern of RA-driven peri-articular erosion, which
    progresses from the synovial interface inward.
    """
    midpoints = _edge_midpoints(network)
    center = np.full(3, network.domain_size / 2)
    dists = np.linalg.norm(midpoints - center, axis=1)
    # Higher weight for peripheral edges
    weights = dists / dists.max()
    return weights ** 2  # accentuate periphery


def _osteoclastic_weights(
    network: TrabecularNetwork, n_hotspots: int = 5, rng: np.random.Generator = None
) -> np.ndarray:
    """
    Compute removal weights based on a simulated osteoclastic activity field.

    Generates a sum-of-Gaussians scalar field with random hotspots and assigns
    each edge a weight proportional to the field intensity at its midpoint.
    """
    if rng is None:
        rng = np.random.default_rng()
    midpoints = _edge_midpoints(network)
    hotspots = rng.uniform(0, network.domain_size, size=(n_hotspots, 3))
    sigma = network.domain_size / 4
    weights = np.zeros(len(midpoints))
    for h in hotspots:
        d2 = np.sum((midpoints - h) ** 2, axis=1)
        weights += np.exp(-d2 / (2 * sigma ** 2))
    return weights


def progressive_erosion(
    network: TrabecularNetwork,
    n_steps: int = 20,
    max_removal_fraction: float = 0.5,
    regime: ErosionRegime = ErosionRegime.UNIFORM,
    rng_seed: Optional[int] = None,
) -> List[ErosionState]:
    """
    Generate a trajectory of progressively eroded networks.

    Parameters
    ----------
    network : TrabecularNetwork
        Initial (pristine) trabecular network.
    n_steps : int
        Number of erosion steps along the trajectory (including step 0).
    max_removal_fraction : float
        Maximum fraction of edges to remove by the final step.
    regime : ErosionRegime
        Erosion model to apply.
    rng_seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    list of ErosionState
        The erosion trajectory.
    """
    rng = np.random.default_rng(rng_seed)
    initial_n_edges = network.n_edges

    # Compute per-edge removal weights according to regime
    if regime == ErosionRegime.UNIFORM:
        weights = np.ones(initial_n_edges)
    elif regime == ErosionRegime.PERIPHERAL:
        weights = _peripheral_weights(network)
    elif regime == ErosionRegime.OSTEOCLASTIC:
        weights = _osteoclastic_weights(network, rng=rng)
    else:
        raise ValueError(f"Unknown regime: {regime}")

    probabilities = weights / weights.sum()

    # Pre-sample the global removal order ONCE so the trajectory is monotone
    n_total_to_remove = int(np.floor(max_removal_fraction * initial_n_edges))
    removal_order = rng.choice(
        initial_n_edges, size=n_total_to_remove, replace=False, p=probabilities
    )

    trajectory: List[ErosionState] = []
    fractions = np.linspace(0, max_removal_fraction, n_steps)

    for step, frac in enumerate(fractions):
        n_to_remove = int(np.floor(frac * initial_n_edges))
        removed_set = set(removal_order[:n_to_remove].tolist())

        # Build a new network with the surviving edges
        surviving_idx = [i for i in range(initial_n_edges) if i not in removed_set]
        new_edges = [network.edges[i] for i in surviving_idx]
        new_thickness = network.edge_thickness[surviving_idx]
        new_modulus = network.edge_modulus[surviving_idx]

        new_graph = network.graph.__class__()
        new_graph.add_nodes_from(network.graph.nodes())
        new_graph.add_edges_from(new_edges)

        new_network = TrabecularNetwork(
            nodes=network.nodes.copy(),
            edges=new_edges,
            graph=new_graph,
            edge_thickness=new_thickness,
            edge_modulus=new_modulus,
            domain_size=network.domain_size,
            metadata={
                **network.metadata,
                "erosion_regime": regime.value,
                "erosion_step": step,
                "p_removed": float(frac),
            },
        )

        trajectory.append(ErosionState(
            network=new_network,
            p_removed=float(frac),
            n_removed=n_to_remove,
            n_remaining=initial_n_edges - n_to_remove,
            regime=regime,
            step=step,
        ))

    return trajectory
