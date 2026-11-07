"""
Index of Effective Mechanical Connectivity (IRCE).

The IRCE is a dimensionless composite metric in [0, 1] integrating:
  (i)   M — normalized effective elastic modulus,
  (ii)  T — topological connectivity of the load-bearing subnetwork,
  (iii) A — normalized anisotropy of the trabecular architecture.

All three components are normalized against the healthy reference network,
so that IRCE = 1 for the pristine network and IRCE → 0 as the network
fragments.

Both additive and multiplicative formulations are provided.

Formal definition (additive):

    IRCE = α · M + β · T + γ · A

    M = E*_eroded / E*_healthy
    T = N_LCC / N_total
    A = anisotropy component (see ``anisotropy.anisotropy_component``)

    with α + β + γ = 1,   α, β, γ ≥ 0,   IRCE ∈ [0, 1].

Formal definition (multiplicative):

    IRCE_mult = M^α · T^β · A^γ
"""

from __future__ import annotations
from dataclasses import dataclass

from .voronoi import TrabecularNetwork
from .connectivity import connectivity_ratio
from .anisotropy import (
    AnisotropyMode,
    anisotropy_component,
    compute_local_anisotropy,
)
from .mechanics import effective_modulus_approx


@dataclass
class IRCEResult:
    """Container for IRCE computation results."""
    irce: float
    modulus_ratio: float        # M
    connectivity_ratio: float   # T
    anisotropy: float           # A (normalized component used in the IRCE)
    anisotropy_local: float     # raw A_local descriptor of the eroded network
    weights: tuple
    formulation: str            # "additive" or "multiplicative"
    anisotropy_mode: str = "retention"


def _validate_weights(alpha: float, beta: float, gamma: float, tol: float = 1e-6) -> None:
    if min(alpha, beta, gamma) < 0:
        raise ValueError("Weights must be non-negative.")
    s = alpha + beta + gamma
    if abs(s - 1.0) > tol:
        raise ValueError(f"Weights must sum to 1.0; got {s:.6f}.")


def _clip01(x: float) -> float:
    return float(max(0.0, min(1.0, x)))


def irce_components(
    current_network: TrabecularNetwork,
    reference_network: TrabecularNetwork,
    matrix_modulus: float = 20e3,
    anisotropy_mode: AnisotropyMode = "retention",
) -> tuple[float, float, float, float]:
    """
    Compute the normalized IRCE components (M, T, A) and the raw A_local.

    Returns
    -------
    (M, T, A, A_local) : tuple of float
        M, T and A are clipped to [0, 1] and equal 1 for
        ``current_network is reference_network`` (provided the reference
        network is connected).
    """
    E_healthy = effective_modulus_approx(reference_network, matrix_modulus=matrix_modulus)
    E_eroded = effective_modulus_approx(current_network, matrix_modulus=matrix_modulus)
    M = _clip01(E_eroded / E_healthy) if E_healthy > 0 else 0.0

    T = _clip01(connectivity_ratio(current_network, reference_network.n_edges))

    A = anisotropy_component(current_network, reference_network, mode=anisotropy_mode)
    A_local = compute_local_anisotropy(current_network)
    return M, T, A, A_local


def compute_irce(
    current_network: TrabecularNetwork,
    reference_network: TrabecularNetwork,
    alpha: float = 0.4,
    beta: float = 0.4,
    gamma: float = 0.2,
    matrix_modulus: float = 20e3,
    anisotropy_mode: AnisotropyMode = "retention",
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
        Defaults: α = β = 0.4, γ = 0.2.
    matrix_modulus : float
        Bone matrix modulus (MPa) used for the approximate estimator.
    anisotropy_mode : {"retention", "ratio"}
        Definition of the anisotropy component; see
        :func:`ra_trabecular.anisotropy.anisotropy_component`.

    Returns
    -------
    IRCEResult
    """
    _validate_weights(alpha, beta, gamma)
    M, T, A, A_local = irce_components(
        current_network, reference_network, matrix_modulus, anisotropy_mode
    )
    irce_val = alpha * M + beta * T + gamma * A
    return IRCEResult(
        irce=_clip01(irce_val),
        modulus_ratio=M,
        connectivity_ratio=T,
        anisotropy=A,
        anisotropy_local=float(A_local),
        weights=(alpha, beta, gamma),
        formulation="additive",
        anisotropy_mode=anisotropy_mode,
    )


def compute_irce_multiplicative(
    current_network: TrabecularNetwork,
    reference_network: TrabecularNetwork,
    alpha: float = 0.4,
    beta: float = 0.4,
    gamma: float = 0.2,
    matrix_modulus: float = 20e3,
    anisotropy_mode: AnisotropyMode = "retention",
) -> IRCEResult:
    """
    Compute the multiplicative (synergistic) IRCE: M^α · T^β · A^γ.

    Because A is normalized against the healthy network (A = 1 when
    anisotropy is preserved), no epsilon clamping is needed: an isotropic
    healthy network no longer forces IRCE_mult to zero.
    """
    _validate_weights(alpha, beta, gamma)
    M, T, A, A_local = irce_components(
        current_network, reference_network, matrix_modulus, anisotropy_mode
    )
    irce_val = (M ** alpha) * (T ** beta) * (A ** gamma)
    return IRCEResult(
        irce=_clip01(irce_val),
        modulus_ratio=M,
        connectivity_ratio=T,
        anisotropy=A,
        anisotropy_local=float(A_local),
        weights=(alpha, beta, gamma),
        formulation="multiplicative",
        anisotropy_mode=anisotropy_mode,
    )
