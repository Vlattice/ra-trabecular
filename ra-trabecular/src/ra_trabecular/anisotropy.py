"""
Anisotropy estimation for trabecular networks.

Implements a normalized anisotropy ratio based on edge orientation distribution,
inspired by the mean intercept length (MIL) tensor and fabric tensor formalism
(Cowin-Mehrabadi, Whitehouse).
"""

from __future__ import annotations
import numpy as np

from .voronoi import TrabecularNetwork


def edge_orientation_tensor(network: TrabecularNetwork) -> np.ndarray:
    """
    Compute the second-order orientation tensor of trabecular struts.

    Each edge contributes a dyad u u^T weighted by edge length, where u is
    the unit vector along the edge.

    Returns
    -------
    np.ndarray, shape (3, 3)
        Symmetric, positive semi-definite orientation tensor (trace = 1
        after normalization).
    """
    if network.n_edges == 0:
        return np.eye(3) / 3.0

    edges_arr = np.array(network.edges)
    vecs = network.nodes[edges_arr[:, 1]] - network.nodes[edges_arr[:, 0]]
    lengths = np.linalg.norm(vecs, axis=1)
    valid = lengths > 1e-12
    vecs = vecs[valid]
    lengths = lengths[valid]
    units = vecs / lengths[:, None]

    # Length-weighted outer product accumulator
    T = (lengths[:, None, None] * units[:, :, None] * units[:, None, :]).sum(axis=0)
    T = T / np.trace(T)
    return T


def compute_local_anisotropy(network: TrabecularNetwork) -> float:
    """
    Compute a normalized anisotropy scalar A_local in [0, 1].

    A_local is defined from the eigenvalues (λ1 >= λ2 >= λ3) of the
    orientation tensor as:

        A_local = (λ1 - λ3) / (λ1 + λ3)         if (λ1 + λ3) > 0
                = 0                              otherwise

    Bounds:
      - Perfectly isotropic network: A_local = 0
      - Highly aligned (single dominant axis): A_local → 1

    Note: This is one of several admissible anisotropy descriptors and is
    chosen here for simplicity and boundedness. Full fabric tensor
    treatment is scheduled for v0.2.0.
    """
    T = edge_orientation_tensor(network)
    eigvals = np.linalg.eigvalsh(T)
    eigvals = np.sort(eigvals)[::-1]   # descending
    l1, l3 = float(eigvals[0]), float(eigvals[-1])
    denom = l1 + l3
    if denom <= 0:
        return 0.0
    return (l1 - l3) / denom
