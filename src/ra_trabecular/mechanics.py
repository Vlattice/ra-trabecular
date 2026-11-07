"""
Effective mechanical modulus estimation for trabecular networks.

This module provides:
  (a) A fast approximate estimator based on Gibson-Ashby scaling laws
      applied to the load-bearing (largest connected) subnetwork.
  (b) A scaffold for a full FEM beam/truss formulation, planned for v0.3.0.

The fast estimator is sufficient for the concept paper and for prototyping
the IRCE trajectory. Replacement with full FEM is straightforward because
the API is preserved.
"""

from __future__ import annotations
import numpy as np

from .voronoi import TrabecularNetwork, load_bearing_subnetwork


def effective_modulus_approx(
    network: TrabecularNetwork,
    reference_total_edges: int | None = None,
    matrix_modulus: float = 20e3,
    gibson_ashby_exponent: float = 2.0,
    geometric_constant: float = 1.0,
    connectivity_penalty: bool = False,
) -> float:
    """
    Approximate effective elastic modulus using a Gibson-Ashby scaling law
    applied to the load-bearing subnetwork.

    The approximation reads:

        E* ≈ C · E_s · (φ_eff)^n

    where:
      - φ_eff = (volume of struts in the largest connected component, LCC)
                / (domain volume)
      - n is the Gibson-Ashby exponent (~2 for bending-dominated foams)

    Only struts in the LCC contribute, so disconnected fragments carry no
    load. Connectivity therefore already enters E* through φ_eff.

    Changed in v0.1.1: the extra multiplicative factor
    ``N_LCC / N_total`` used in v0.1.0 is now off by default
    (``connectivity_penalty=False``). Together with φ_eff and the separate
    T term of the IRCE it made connectivity count three times. It can still
    be enabled for comparison with v0.1.0 results.

    This is a deliberate, transparent approximation. Replacement with a
    full FEM solver is planned for v0.3.0 via a sibling function
    ``effective_modulus_fem(...)``.

    Parameters
    ----------
    network : TrabecularNetwork
        Current network state.
    reference_total_edges : int, optional
        Initial pristine edge count. Only used when
        ``connectivity_penalty=True``.
    matrix_modulus : float
        Bone matrix modulus E_s (MPa).
    gibson_ashby_exponent : float
        Power-law exponent (typically 2 for bending, 1 for stretch).
    geometric_constant : float
        Pre-factor C in the Gibson-Ashby relation.
    connectivity_penalty : bool
        Reproduce the v0.1.0 estimator (multiply by N_LCC / N_total).

    Returns
    -------
    float
        Approximate effective modulus (MPa).
    """
    if network.n_edges == 0:
        return 0.0

    lcc = load_bearing_subnetwork(network)
    if lcc.n_edges == 0:
        return 0.0

    edges_arr = np.array(lcc.edges)
    lengths = np.linalg.norm(
        lcc.nodes[edges_arr[:, 1]] - lcc.nodes[edges_arr[:, 0]], axis=1
    )
    radii = lcc.edge_thickness / 2.0
    volume_sum = float(np.sum(np.pi * radii ** 2 * lengths))

    domain_volume = network.domain_volume
    phi_eff = volume_sum / domain_volume if domain_volume > 0 else 0.0

    E_eff = geometric_constant * matrix_modulus * (phi_eff ** gibson_ashby_exponent)

    if connectivity_penalty:
        if not reference_total_edges:
            raise ValueError(
                "reference_total_edges is required when connectivity_penalty=True."
            )
        E_eff *= lcc.n_edges / reference_total_edges

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
