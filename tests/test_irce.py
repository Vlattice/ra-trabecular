"""
Tests for the IRCE computation and core framework components.
Run with: pytest tests/
"""

import pytest
import numpy as np

from ra_trabecular import (
    generate_voronoi_network,
    progressive_erosion,
    ErosionRegime,
    compute_irce,
    compute_irce_multiplicative,
    connectivity_ratio,
    compute_local_anisotropy,
)


@pytest.fixture
def small_network():
    """A small reproducible Voronoi network for tests."""
    return generate_voronoi_network(n_seeds=80, domain_size=10.0, rng_seed=42)


def test_network_generation_basic(small_network):
    """Network is created with non-zero nodes and edges."""
    assert small_network.n_nodes > 0
    assert small_network.n_edges > 0
    assert small_network.domain_size == 10.0


def test_network_coordination_in_reasonable_range(small_network):
    """Mean coordination number is in the expected range for 3D Voronoi."""
    z = small_network.mean_coordination
    # 3D Poisson Voronoi tessellations have z ≈ 4 for the edge graph,
    # though pruning at boundaries can lower this value.
    assert 2.0 <= z <= 7.0


@pytest.mark.parametrize("compute", [compute_irce, compute_irce_multiplicative])
def test_irce_pristine_equals_one(small_network, compute):
    """The pristine network compared against itself has IRCE = 1, with every
    component (M, T, A) equal to 1, as stated in docs/irce_definition.md."""
    result = compute(small_network, small_network)
    assert result.irce == pytest.approx(1.0, abs=1e-9)
    assert result.modulus_ratio == pytest.approx(1.0, abs=1e-9)
    assert result.connectivity_ratio == pytest.approx(1.0, abs=1e-9)
    assert result.anisotropy == pytest.approx(1.0, abs=1e-9)


@pytest.mark.parametrize("regime", list(ErosionRegime))
@pytest.mark.parametrize("compute", [compute_irce, compute_irce_multiplicative])
def test_irce_monotone_along_erosion(small_network, regime, compute):
    """IRCE is non-increasing at every step of an erosion trajectory, for
    every erosion regime and both formulations."""
    trajectory = progressive_erosion(
        small_network, n_steps=12, max_removal_fraction=0.9,
        regime=regime, rng_seed=42
    )
    irce_values = np.array([
        compute(state.network, small_network).irce for state in trajectory
    ])
    assert np.all(np.diff(irce_values) <= 1e-9), irce_values


def test_irce_collapses_after_percolation(small_network):
    """Past the percolation transition the IRCE approaches 0."""
    trajectory = progressive_erosion(
        small_network, n_steps=10, max_removal_fraction=0.9,
        regime=ErosionRegime.UNIFORM, rng_seed=42
    )
    final = compute_irce(trajectory[-1].network, small_network)
    assert final.irce < 0.1


def test_default_trajectory_crosses_transition(small_network):
    """With default parameters the trajectory reaches the fragmented regime."""
    trajectory = progressive_erosion(small_network, rng_seed=42)
    final = compute_irce(trajectory[-1].network, small_network)
    assert final.connectivity_ratio < 0.3


def test_anisotropy_ratio_mode_bounds(small_network):
    """The v0.1.0 ratio definition is still available and bounded."""
    trajectory = progressive_erosion(small_network, n_steps=5, rng_seed=1)
    for state in trajectory:
        r = compute_irce(state.network, small_network, anisotropy_mode="ratio")
        assert 0.0 <= r.anisotropy <= 1.0
    with pytest.raises(ValueError):
        compute_irce(small_network, small_network, anisotropy_mode="nope")


def test_legacy_connectivity_penalty(small_network):
    """The v0.1.0 modulus estimator can be reproduced for comparison."""
    from ra_trabecular.mechanics import effective_modulus_approx
    trajectory = progressive_erosion(small_network, n_steps=5, rng_seed=1)
    eroded = trajectory[2].network
    e_new = effective_modulus_approx(eroded)
    e_old = effective_modulus_approx(
        eroded, reference_total_edges=small_network.n_edges,
        connectivity_penalty=True,
    )
    assert 0 < e_old < e_new


def test_domain_volume_accounts_for_anisotropy():
    """A z-stretched network uses the stretched domain volume."""
    net = generate_voronoi_network(
        n_seeds=40, domain_size=10.0, anisotropy_factor=2.0, rng_seed=0
    )
    assert net.domain_volume == pytest.approx(2000.0)


def test_weights_must_sum_to_one(small_network):
    """compute_irce raises when weights don't sum to 1."""
    with pytest.raises(ValueError):
        compute_irce(small_network, small_network, alpha=0.5, beta=0.5, gamma=0.5)


def test_weights_must_be_non_negative(small_network):
    """compute_irce raises with negative weights."""
    with pytest.raises(ValueError):
        compute_irce(small_network, small_network, alpha=-0.1, beta=0.6, gamma=0.5)


def test_connectivity_ratio_bounds(small_network):
    """N_LCC/N_total is in [0, 1]."""
    cr = connectivity_ratio(small_network, small_network.n_edges)
    assert 0.0 <= cr <= 1.0


def test_anisotropy_bounds(small_network):
    """A_local is in [0, 1]."""
    a = compute_local_anisotropy(small_network)
    assert 0.0 <= a <= 1.0


def test_multiplicative_irce_bounds(small_network):
    """Multiplicative IRCE is in [0, 1]."""
    result = compute_irce_multiplicative(small_network, small_network)
    assert 0.0 <= result.irce <= 1.0
    assert result.formulation == "multiplicative"


def test_anisotropic_network_more_anisotropic(small_network):
    """A z-stretched network has higher anisotropy than a uniform one."""
    aniso_net = generate_voronoi_network(
        n_seeds=80, domain_size=10.0, anisotropy_factor=2.5, rng_seed=42
    )
    a_uniform = compute_local_anisotropy(small_network)
    a_aniso = compute_local_anisotropy(aniso_net)
    assert a_aniso > a_uniform
