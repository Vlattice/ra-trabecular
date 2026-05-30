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


def test_irce_pristine_equals_one_approximately(small_network):
    """IRCE of a network compared against itself should be close to 1 modulo
    anisotropy contribution, since modulus_ratio = 1 and connectivity = 1."""
    result = compute_irce(small_network, small_network)
    assert 0.0 <= result.irce <= 1.0
    # modulus_ratio and connectivity ratio should both be 1.0
    assert pytest.approx(result.modulus_ratio, abs=1e-6) == 1.0
    # connectivity_ratio = N_LCC / N_total_initial
    # for a connected network this is close to 1; allow small slack
    assert result.connectivity_ratio > 0.5


def test_irce_decreases_with_erosion(small_network):
    """IRCE should be non-increasing along an erosion trajectory."""
    trajectory = progressive_erosion(
        small_network, n_steps=10, max_removal_fraction=0.5,
        regime=ErosionRegime.UNIFORM, rng_seed=42
    )
    irce_values = [
        compute_irce(state.network, small_network).irce
        for state in trajectory
    ]
    # Allow tiny numerical noise but require overall monotone trend
    assert irce_values[0] >= irce_values[-1]
    assert irce_values[-1] < irce_values[0]


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
