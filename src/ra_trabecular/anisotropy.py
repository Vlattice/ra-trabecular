"""
Anisotropy estimation for trabecular networks.

Implements descriptors based on the length-weighted edge orientation
(fabric) tensor, inspired by the mean intercept length (MIL) tensor and
fabric tensor formalism (Cowin-Mehrabadi, Whitehouse).

Two quantities are provided:

* ``compute_local_anisotropy`` — a scalar degree of anisotropy A_local in
  [0, 1] computed from the eigenvalues of the normalized fabric tensor.
* ``anisotropy_component`` — the normalized anisotropy component ``A`` used
  in the IRCE, which compares an eroded network against its healthy
  reference (A = 1 for the pristine network).
"""

from __future__ import annotations
from typing import Literal
import numpy as np

from .voronoi import TrabecularNetwork, load_bearing_subnetwork


AnisotropyMode = Literal["retention", "ratio"]


def fabric_tensor(network: TrabecularNetwork, normalize: bool = True) -> np.ndarray:
    """
    Compute the second-order, length-weighted orientation (fabric) tensor.

    Each edge contributes a dyad ``L u u^T``, where ``u`` is the unit vector
    along the edge and ``L`` its length.

    Parameters
    ----------
    network : TrabecularNetwork
        Trabecular network.
    normalize : bool
        If True (default), divide by the trace so that trace = 1. If False,
        return the raw tensor, whose trace equals the total strut length.

    Returns
    -------
    np.ndarray, shape (3, 3)
        Symmetric, positive semi-definite tensor.
    """
    if network.n_edges == 0:
        return np.eye(3) / 3.0 if normalize else np.zeros((3, 3))

    edges_arr = np.array(network.edges)
    vecs = network.nodes[edges_arr[:, 1]] - network.nodes[edges_arr[:, 0]]
    lengths = np.linalg.norm(vecs, axis=1)
    valid = lengths > 1e-12
    vecs = vecs[valid]
    lengths = lengths[valid]
    if len(lengths) == 0:
        return np.eye(3) / 3.0 if normalize else np.zeros((3, 3))
    units = vecs / lengths[:, None]

    T = (lengths[:, None, None] * units[:, :, None] * units[:, None, :]).sum(axis=0)
    if normalize:
        T = T / np.trace(T)
    return T


# Backwards-compatible alias (v0.1.0 name)
def edge_orientation_tensor(network: TrabecularNetwork) -> np.ndarray:
    """Normalized fabric tensor (alias kept for backwards compatibility)."""
    return fabric_tensor(network, normalize=True)


def compute_local_anisotropy(network: TrabecularNetwork) -> float:
    """
    Compute a normalized degree of anisotropy A_local in [0, 1].

    A_local is defined from the eigenvalues (λ1 >= λ2 >= λ3) of the
    normalized fabric tensor as:

        A_local = (λ1 - λ3) / (λ1 + λ3)

    Bounds:
      - Perfectly isotropic network: A_local = 0
      - Highly aligned (single dominant axis): A_local → 1

    Note: this is a *descriptor of the architecture*, not the IRCE
    component. Use :func:`anisotropy_component` for the IRCE.
    """
    T = fabric_tensor(network, normalize=True)
    eigvals = np.sort(np.linalg.eigvalsh(T))[::-1]
    l1, l3 = float(eigvals[0]), float(eigvals[-1])
    denom = l1 + l3
    if denom <= 0:
        return 0.0
    return (l1 - l3) / denom


def anisotropy_component(
    current_network: TrabecularNetwork,
    reference_network: TrabecularNetwork,
    mode: AnisotropyMode = "retention",
) -> float:
    """
    Normalized anisotropy component ``A`` of the IRCE, in [0, 1].

    Both modes are evaluated on the load-bearing subnetwork (largest
    connected component) of the eroded network, and both return
    ``A = 1`` for the pristine network.

    Modes
    -----
    ``"retention"`` (default, v0.1.1)
        Fraction of the healthy fabric retained along the healthy principal
        (load) axis ``e1``:

            A = (e1^T F_eroded e1) / (e1^T F_healthy e1)

        where ``F`` is the *un-normalized* fabric tensor of the load-bearing
        subnetwork. A → 0 when the struts aligned with the principal load
        axis are lost. This is monotone along erosion trajectories.

    ``"ratio"`` (v0.1.0 definition)
        ``A = A_local(eroded LCC) / A_local(healthy)``, clipped to [0, 1].
        Note: for near-isotropic networks A_local(healthy) is small, so this
        ratio is dominated by noise and tends to *increase* as the network
        fragments (small clusters look anisotropic). It is kept for
        comparison and sensitivity analysis only.

    Returns
    -------
    float
        A in [0, 1].
    """
    current_lcc = load_bearing_subnetwork(current_network)
    if current_lcc.n_edges == 0:
        return 0.0
    reference_lcc = load_bearing_subnetwork(reference_network)

    if mode == "retention":
        F_ref = fabric_tensor(reference_lcc, normalize=False)
        _, eigvecs = np.linalg.eigh(F_ref)
        e1 = eigvecs[:, -1]
        denom = float(e1 @ F_ref @ e1)
        if denom <= 0:
            return 0.0
        F_cur = fabric_tensor(current_lcc, normalize=False)
        value = float(e1 @ F_cur @ e1) / denom
    elif mode == "ratio":
        a_ref = compute_local_anisotropy(reference_lcc)
        if a_ref <= 1e-12:
            return 1.0
        value = compute_local_anisotropy(current_lcc) / a_ref
    else:
        raise ValueError(f"Unknown anisotropy mode: {mode!r}")

    return float(min(1.0, max(0.0, value)))
