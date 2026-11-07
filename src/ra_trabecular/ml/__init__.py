"""
Machine-learning tools for RA-Trabecular.

Early-warning prediction of proximity to the percolation transition from a
single, reference-free snapshot of a trabecular network.

Requires the optional dependencies ``scikit-learn`` and ``pandas``::

    pip install -e ".[ml]"
"""

from .features import (
    structural_features,
    DENSITY_FEATURES,
    TOPOLOGY_FEATURES,
    ANISOTROPY_FEATURES,
    ALL_FEATURES,
)
from .dataset import generate_dataset, critical_fraction, GenerationRanges
from .early_warning import (
    FEATURE_SETS,
    AT_RISK_WINDOW,
    EvaluationResult,
    evaluate_feature_sets,
    evaluate_cross_regime,
    cross_validated_predictions,
    fit_early_warning_model,
    permutation_importance_table,
)

__all__ = [
    "structural_features",
    "DENSITY_FEATURES",
    "TOPOLOGY_FEATURES",
    "ANISOTROPY_FEATURES",
    "ALL_FEATURES",
    "generate_dataset",
    "critical_fraction",
    "GenerationRanges",
    "FEATURE_SETS",
    "AT_RISK_WINDOW",
    "EvaluationResult",
    "evaluate_feature_sets",
    "evaluate_cross_regime",
    "cross_validated_predictions",
    "fit_early_warning_model",
    "permutation_importance_table",
]
