"""
Index of Effective Mechanical Connectivity (IRCE).

The IRCE is a dimensionless composite metric in [0, 1] integrating:
  (i)   normalized effective elastic modulus,
  (ii)  topological connectivity of the load-bearing subnetwork,
  (iii) local anisotropy of the trabecular architecture.

Both additive and multiplicative formulations are provided. The additive
form is used as the default for v0.1.0 (concept paper). The multiplicative
form models synergistic structural collapse and is provided as an alternative
for future calibration and sensitivity analysis.

Formal definition (additive):

    IRCE = α · (E*_eroded / E*_healthy)
         + β · (N_LCC / N_total)
         + γ · A_local

    with α + β + γ = 1,   α, β, γ ≥ 0,   IRCE ∈ [0, 1].

Formal definition (multiplicative):

    IRCE_mult = (E*_eroded / E*_healthy)^α
              · (N_LCC / N_total)^β
              · A_local^γ
"""

from __future__ import annotations
from dataclasses import dataclass

from .voronoi import TrabecularNetwork
from .connectivity import connectivity_ratio
from .anisotropy import compute_local_anisotropy
from .mechanics import effective_modulus_approx


@dataclass
class IRCEResult:
    """Container for IRCE computation results."""
    irce: float
    modulus_ratio: float
    connectivity_ratio: float
    anisotropy: float
    weights: tuple
    formulation: str   # "additive" or "multiplicative"


def _validate_weights(alpha: float, beta: float, gamma: float, tol: float = 1e-6) -> None:
    if min(alpha, beta, gamma) < 0:
        raise ValueError("Weights must be non-negative.")
    s = alpha + beta + gamma
    if abs(s - 1.0) > tol:
        raise ValueError(f"Weights must sum to 1.0; got {s:.6f}.")


def compute_irce(
    current_network: TrabecularNetwork,
    reference_network: TrabecularNetwork,
    alpha: float = 0.4,
    beta: float = 0.4,
    gamma: float = 0.2,
    matrix_modulus: float = 20e3,
) -> IRCEResult:
    """
    Compute the additive IRCE.

    Parameters
    ----------
    current_network : TrabecularNetwork
        Eroded network state.
    reference_network : TrabecularNetwork
        Pristine (healthy) reference network.
    alpha, beta, gamma : float
        Component weights; must satisfy α + β + γ = 1, all ≥ 0.
        Defaults: α = β = 0.4, γ = 0.2 (modulus and connectivity equally weighted).
    matrix_modulus : float
        Bone matrix modulus (MPa) used for the approximate FE estimator.

    Returns
    -------
    IRCEResult
    """
    _validate_weights(alpha, beta, gamma)

    E_healthy = effective_modulus_approx(
        reference_network,
        reference_total_edges=reference_network.n_edges,
        matrix_modulus=matrix_modulus,
    )
    E_eroded = effective_modulus_approx(
        current_network,
        reference_total_edges=reference_network.n_edges,
        matrix_modulus=matrix_modulus,
    )
    modulus_ratio = (E_eroded / E_healthy) if E_healthy > 0 else 0.0
    modulus_ratio = max(0.0, min(1.0, modulus_ratio))

    conn_ratio = connectivity_ratio(current_network, reference_network.n_edges)
    conn_ratio = max(0.0, min(1.0, conn_ratio))

    anisotropy = compute_local_anisotropy(current_network)
    anisotropy = max(0.0, min(1.0, anisotropy))

    irce_val = alpha * modulus_ratio + beta * conn_ratio + gamma * anisotropy

    return IRCEResult(
        irce=float(irce_val),
        modulus_ratio=float(modulus_ratio),
        connectivity_ratio=float(conn_ratio),
        anisotropy=float(anisotropy),
        weights=(alpha, beta, gamma),
        formulation="additive",
    )


def compute_irce_multiplicative(
    current_network: TrabecularNetwork,
    reference_network: TrabecularNetwork,
    alpha: float = 0.4,
    beta: float = 0.4,
    gamma: float = 0.2,
    matrix_modulus: float = 20e3,
) -> IRCEResult:
    """
    Compute the multiplicative (synergistic) IRCE.

    See module docstring for the formal definition.

    Note: γ = 0 with A_local = 0 would force IRCE_mult = 0 in the strict
    multiplicative form. We therefore clamp A_local to a small epsilon for
    the multiplicative evaluation when γ > 0 and A_local = 0, to avoid
    spurious collapses driven by isotropy alone.
    """
    _validate_weights(alpha, beta, gamma)

    E_healthy = effective_modulus_approx(
        reference_network,
        reference_total_edges=reference_network.n_edges,
        matrix_modulus=matrix_modulus,
    )
    E_eroded = effective_modulus_approx(
        current_network,
        reference_total_edges=reference_network.n_edges,
        matrix_modulus=matrix_modulus,
    )
    modulus_ratio = (E_eroded / E_healthy) if E_healthy > 0 else 0.0
    modulus_ratio = max(0.0, min(1.0, modulus_ratio))

    conn_ratio = connectivity_ratio(current_network, reference_network.n_edges)
    conn_ratio = max(0.0, min(1.0, conn_ratio))

    anisotropy = compute_local_anisotropy(current_network)
    anisotropy = max(0.0, min(1.0, anisotropy))

    eps = 1e-9
    aniso_for_mult = max(anisotropy, eps) if gamma > 0 else 1.0

    irce_val = (
        (modulus_ratio ** alpha)
        * (conn_ratio ** beta)
        * (aniso_for_mult ** gamma)
    )

    return IRCEResult(
        irce=float(irce_val),
        modulus_ratio=float(modulus_ratio),
        connectivity_ratio=float(conn_ratio),
        anisotropy=float(anisotropy),
        weights=(alpha, beta, gamma),
        formulation="multiplicative",
    )
