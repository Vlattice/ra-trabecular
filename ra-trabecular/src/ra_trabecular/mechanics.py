"""
Effective mechanical modulus estimation for trabecular networks.

This module provides:
  (a) A fast approximate estimator based on Gibson-Ashby scaling laws
      combined with a connectivity correction (used in v0.1.0).
  (b) A scaffold for a full FEM beam/truss formulation, planned for v0.3.0.

The fast estimator is sufficient for the concept paper and for prototyping
the IRCE trajectory. Replacement with full FEM is straightforward because
the API is preserved.
"""

from __future__ import annotations
import numpy as np
import networkx as nx

from .voronoi import TrabecularNetwork
from .connectivity import largest_connected_component


def effective_modulus_approx(
    network: TrabecularNetwork,
    reference_total_edges: int,
    matrix_modulus: float = 20e3,
    gibson_ashby_exponent: float = 2.0,
    geometric_constant: float = 1.0,
) -> float:
    """
    Approximate effective elastic modulus using a Gibson-Ashby scaling law
    modulated by a connectivity penalty.

    The approximation reads:

        E* ≈ C · E_s · (φ_eff)^n · LCC_penalty

    where:
      - φ_eff = (sum of edge volumes in LCC) / (domain volume)
      - LCC_penalty = (N_LCC_edges / N_total_initial)
      - n is the Gibson-Ashby exponent (~2 for bending-dominated foams)

    This is a deliberate, transparent approximation. Replacement with a
    full FEM solver is planned for v0.3.0 via the same function signature
    or a sibling function `effective_modulus_fem(...)`.

    Parameters
    ----------
    network : TrabecularNetwork
        Current network state.
    reference_total_edges : int
        Initial pristine edge count (for LCC normalization).
    matrix_modulus : float
        Bone matrix modulus E_s (MPa).
    gibson_ashby_exponent : float
        Power-law exponent (typically 2 for bending, 1 for stretch).
    geometric_constant : float
        Pre-factor C in the Gibson-Ashby relation.

    Returns
    -------
    float
        Approximate effective modulus (MPa).
    """
    if network.n_edges == 0 or reference_total_edges == 0:
        return 0.0

    lcc = largest_connected_component(network)
    n_lcc_edges = lcc.number_of_edges()
    if n_lcc_edges == 0:
        return 0.0

    # Compute LCC edge volumes (cylindrical struts)
    lcc_edge_set = set(map(lambda e: tuple(sorted(e)), lcc.edges()))
    edges_arr = np.array(network.edges)
    lengths_all = np.linalg.norm(
        network.nodes[edges_arr[:, 1]] - network.nodes[edges_arr[:, 0]], axis=1
    )

    volume_sum = 0.0
    for idx, (a, b) in enumerate(network.edges):
        if tuple(sorted((a, b))) in lcc_edge_set:
            r = network.edge_thickness[idx] / 2.0
            volume_sum += np.pi * r * r * lengths_all[idx]

    domain_volume = network.domain_size ** 3
    phi_eff = volume_sum / domain_volume if domain_volume > 0 else 0.0

    lcc_penalty = n_lcc_edges / reference_total_edges

    E_eff = (
        geometric_constant
        * matrix_modulus
        * (phi_eff ** gibson_ashby_exponent)
        * lcc_penalty
    )
    return float(E_eff)


def effective_modulus_fem(network: TrabecularNetwork, **kwargs) -> float:
    """
    [Planned for v0.3.0] Full FEM beam/truss computation of effective modulus.

    Currently raises NotImplementedError. Will be implemented using
    scikit-fem with Euler-Bernoulli or Timoshenko beam elements.
    """
    raise NotImplementedError(
        "Full FEM evaluation is scheduled for v0.3.0. "
        "Use effective_modulus_approx() in v0.1.0."
    )
