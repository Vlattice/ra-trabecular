"""
Early-warning models: how far is a trabecular network from collapse?

Given a single reference-free snapshot of a network, the models predict the
remaining erosion budget ``delta = p_c - p`` before the percolation
transition (see :mod:`ra_trabecular.ml.dataset`).

The central comparison is between feature sets:

* ``density``   — BV/TV-like descriptors only (standard morphometry),
* ``topology``  — connectivity / percolation descriptors only,
* ``density+topology`` and ``all`` (adds fabric-tensor shape).

If connectivity carries information about proximity to failure that density
does not, ``topology`` should outperform ``density`` — the testable form of
the framework's second prediction (divergence between IRCE-type and
density-based metrics near structural collapse).

All evaluations group samples by ``network_id``: snapshots of the same
"individual" never appear in both training and test folds.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

from .features import DENSITY_FEATURES, TOPOLOGY_FEATURES, ANISOTROPY_FEATURES


FEATURE_SETS: Dict[str, List[str]] = {
    "density": list(DENSITY_FEATURES),
    "topology": list(TOPOLOGY_FEATURES),
    "density+topology": list(DENSITY_FEATURES) + list(TOPOLOGY_FEATURES),
    "all": list(DENSITY_FEATURES) + list(TOPOLOGY_FEATURES) + list(ANISOTROPY_FEATURES),
}

#: Width of the "at risk" window: 0 <= delta <= AT_RISK_WINDOW.
AT_RISK_WINDOW = 0.10


def make_model(random_state: int = 0):
    """Default regressor: histogram gradient boosting (scikit-learn)."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    return HistGradientBoostingRegressor(
        max_iter=300, learning_rate=0.05, max_leaf_nodes=31,
        l2_regularization=1e-3, random_state=random_state,
    )


@dataclass
class EvaluationResult:
    """Cross-validated performance of one feature set."""
    feature_set: str
    mae_connected: float      # MAE of delta on still-connected states (delta >= 0)
    r2_connected: float       # R^2 on still-connected states
    auc_at_risk: float        # ROC-AUC for 0 <= delta <= AT_RISK_WINDOW vs. delta > window
    n_samples: int

    def as_dict(self) -> dict:
        return self.__dict__.copy()


def _metrics(y_true: np.ndarray, y_pred: np.ndarray):
    from sklearn.metrics import mean_absolute_error, r2_score, roc_auc_score
    connected = y_true >= 0
    mae = mean_absolute_error(y_true[connected], y_pred[connected])
    r2 = r2_score(y_true[connected], y_pred[connected])
    at_risk = (y_true[connected] <= AT_RISK_WINDOW).astype(int)
    if at_risk.min() == at_risk.max():
        auc = float("nan")
    else:
        # Smaller predicted delta = higher risk
        auc = roc_auc_score(at_risk, -y_pred[connected])
    return float(mae), float(r2), float(auc)


def cross_validated_predictions(
    df, features: Sequence[str], target: str = "delta",
    n_splits: int = 5, random_state: int = 0,
) -> np.ndarray:
    """Out-of-fold predictions with GroupKFold over ``network_id``."""
    from sklearn.model_selection import GroupKFold
    X = df[list(features)].to_numpy()
    y = df[target].to_numpy()
    groups = df["network_id"].to_numpy()
    pred = np.empty_like(y, dtype=float)
    for train, test in GroupKFold(n_splits=n_splits).split(X, y, groups):
        model = make_model(random_state).fit(X[train], y[train])
        pred[test] = model.predict(X[test])
    return pred


def evaluate_feature_sets(
    df, feature_sets: Optional[Dict[str, List[str]]] = None,
    n_splits: int = 5, random_state: int = 0,
) -> List[EvaluationResult]:
    """
    Compare feature sets with grouped cross-validation.

    Returns one :class:`EvaluationResult` per feature set.
    """
    feature_sets = feature_sets or FEATURE_SETS
    y = df["delta"].to_numpy()
    results = []
    for name, feats in feature_sets.items():
        pred = cross_validated_predictions(df, feats, n_splits=n_splits,
                                           random_state=random_state)
        mae, r2, auc = _metrics(y, pred)
        results.append(EvaluationResult(name, mae, r2, auc, len(df)))
    return results


def evaluate_cross_regime(
    df, features: Sequence[str], random_state: int = 0,
) -> Dict[str, EvaluationResult]:
    """
    Leave-one-regime-out evaluation: train on two erosion regimes, test on
    the held-out one (networks are also disjoint between train and test).

    Measures whether the model has learned a regime-independent signature
    of approaching collapse rather than the specifics of one erosion model.
    """
    ids = np.sort(df["network_id"].unique())
    rng = np.random.default_rng(random_state)
    test_ids = set(rng.choice(ids, size=max(1, len(ids) // 3), replace=False).tolist())

    out = {}
    for held_out in sorted(df["regime"].unique()):
        train = df[(df["regime"] != held_out) & (~df["network_id"].isin(test_ids))]
        test = df[(df["regime"] == held_out) & (df["network_id"].isin(test_ids))]
        model = make_model(random_state).fit(train[list(features)], train["delta"])
        pred = model.predict(test[list(features)])
        mae, r2, auc = _metrics(test["delta"].to_numpy(), pred)
        out[held_out] = EvaluationResult(f"held-out {held_out}", mae, r2, auc, len(test))
    return out


def fit_early_warning_model(df, features: Sequence[str] = FEATURE_SETS["all"],
                            random_state: int = 0):
    """Fit the early-warning regressor on the whole dataset."""
    return make_model(random_state).fit(df[list(features)], df["delta"])


def permutation_importance_table(model, df, features: Sequence[str],
                                 n_repeats: int = 10, random_state: int = 0):
    """Permutation importance of each feature (on still-connected states)."""
    import pandas as pd
    from sklearn.inspection import permutation_importance
    sub = df[df["delta"] >= 0]
    r = permutation_importance(model, sub[list(features)], sub["delta"],
                               n_repeats=n_repeats, random_state=random_state,
                               scoring="neg_mean_absolute_error")
    return (pd.DataFrame({"feature": list(features),
                          "importance": r.importances_mean,
                          "std": r.importances_std})
            .sort_values("importance", ascending=False)
            .reset_index(drop=True))
