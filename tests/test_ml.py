"""
Tests for the machine-learning early-warning module.
Run with: pytest tests/
"""

import numpy as np
import pytest

pytest.importorskip("sklearn")
pytest.importorskip("pandas")

from ra_trabecular import generate_voronoi_network, progressive_erosion, ErosionRegime
from ra_trabecular.ml import (
    ALL_FEATURES,
    DENSITY_FEATURES,
    TOPOLOGY_FEATURES,
    FEATURE_SETS,
    structural_features,
    critical_fraction,
    generate_dataset,
    evaluate_feature_sets,
)


@pytest.fixture(scope="module")
def network():
    return generate_voronoi_network(n_seeds=80, domain_size=10.0, rng_seed=7)


@pytest.fixture(scope="module")
def tiny_dataset():
    return generate_dataset(
        n_networks=6, regimes=[ErosionRegime.UNIFORM], n_steps=10,
        max_removal_fraction=0.9, rng_seed=1, include_irce=False,
    )


def test_features_complete_and_finite(network):
    feats = structural_features(network)
    assert list(feats) == ALL_FEATURES
    assert all(np.isfinite(v) for v in feats.values())


def test_feature_groups_are_disjoint():
    assert not set(DENSITY_FEATURES) & set(TOPOLOGY_FEATURES)


def test_features_respond_to_erosion(network):
    traj = progressive_erosion(network, n_steps=3, max_removal_fraction=0.6, rng_seed=0)
    f0 = structural_features(traj[0].network)
    f1 = structural_features(traj[-1].network)
    assert f1["bv_tv"] < f0["bv_tv"]
    assert f1["mean_degree"] < f0["mean_degree"]
    assert f1["frac_dangling"] > f0["frac_dangling"]
    assert f1["molloy_reed"] < f0["molloy_reed"]


def test_features_of_empty_network_are_zero(network):
    empty = progressive_erosion(network, n_steps=2, max_removal_fraction=1.0, rng_seed=0)[-1]
    feats = structural_features(empty.network)
    assert feats["bv_tv"] == 0.0
    assert feats["mean_degree"] == 0.0


def test_critical_fraction_interpolates():
    p = np.array([0.0, 0.1, 0.2, 0.3])
    p_inf = np.array([1.0, 0.9, 0.3, 0.1])
    # crosses 0.5 between 0.1 (0.9) and 0.2 (0.3): 0.1 + 0.4/0.6 * 0.1
    assert critical_fraction(p, p_inf) == pytest.approx(0.1 + 0.4 / 6)
    assert np.isnan(critical_fraction(p, np.ones(4)))


def test_dataset_structure(tiny_dataset):
    df = tiny_dataset
    assert df["network_id"].nunique() == 6
    for col in ["p", "p_c", "delta", "p_inf"] + ALL_FEATURES:
        assert col in df.columns
    assert np.allclose(df["delta"], df["p_c"] - df["p"])
    assert (df["p_c"] > 0).all() and (df["p_c"] < 0.9).all()


def test_dataset_reproducible_and_independent_of_jobs():
    kwargs = dict(n_networks=2, regimes=[ErosionRegime.UNIFORM], n_steps=5,
                  rng_seed=3, include_irce=False)
    a = generate_dataset(n_jobs=1, **kwargs)
    b = generate_dataset(n_jobs=2, **kwargs)
    import pandas as pd
    pd.testing.assert_frame_equal(a, b)


def test_evaluation_runs(tiny_dataset):
    results = evaluate_feature_sets(
        tiny_dataset, {"topology": FEATURE_SETS["topology"]}, n_splits=3
    )
    assert len(results) == 1
    assert np.isfinite(results[0].mae_connected)
