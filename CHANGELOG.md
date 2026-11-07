# Changelog

All notable changes to RA-Trabecular will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-11-07

Refinement of the initial implementation, aligning the code with the formal
IRCE specification and improving usability and reproducibility.

### IRCE formulation
- All three components (M, T, A) are normalized against the healthy
  reference network, so that IRCE = 1 for the pristine network and
  IRCE → 0 after fragmentation, as specified in `docs/irce_definition.md`.
- Anisotropy component defined as the fraction of healthy fabric retained
  along the principal load axis of the load-bearing subnetwork
  (`anisotropy_mode="retention"`, default). The original formulation remains
  available as `anisotropy_mode="ratio"` for comparison.
- Effective-modulus estimator applies the Gibson–Ashby scaling to the
  load-bearing subnetwork, so connectivity enters the IRCE through a single
  explicit term. The original estimator remains available via
  `connectivity_penalty=True`.
- Domain volume and erosion geometry take `anisotropy_factor` into account.
- Default `max_removal_fraction` extended from 0.5 to 0.8 so trajectories
  fully cover the percolation transition.

### Usability
- Simplified repository layout: `pip install -e .` works directly after
  cloning.
- Fully executable example notebook reproducing
  `figures/01_irce_trajectory.png`.
- Updated README, documentation and roadmap.
- New helpers: `load_bearing_subnetwork`, `anisotropy_component`,
  `irce_components`; `IRCEResult` reports `anisotropy_local` and
  `anisotropy_mode`.
- Expanded test suite (21 tests).

## [0.1.0] — 2026-05-30

### Added
- Concept paper v1.0 (archived independently on Zenodo).
- Initial repository structure: `src/`, `notebooks/`, `docs/`, `tests/`, `data/`, `figures/`.
- Voronoi network generation module (`voronoi.py`).
- Basic stochastic edge-removal erosion model (`erosion.py`).
- Graph-theoretic connectivity metrics (`connectivity.py`).
- Anisotropy estimation via mean intercept length (`anisotropy.py`).
- IRCE computation (additive form) (`irce.py`).
- First reproducible example notebook (`01_voronoi_basic.ipynb`).
- Formal IRCE definition document (`docs/irce_definition.md`).
- Theoretical foundation document (`docs/theory.md`).
- Development roadmap (`docs/roadmap.md`).
- Apache 2.0 license with explicit patent grant.
- Machine-readable citation file (`CITATION.cff`).
- Test scaffolding (`tests/test_irce.py`).

### Notes
- This release establishes prior art and timestamps the IRCE formulation.
- FEM module is scaffolded but not yet integrated; targeted for v0.3.0.

## [Unreleased]

### Added
- `ra_trabecular.ml`: machine-learning early warning of structural collapse.
  - Reference-free structural features (density, topology, anisotropy),
    including connectivity density, dangling-end and bridge fractions,
    mean finite-cluster size and the Molloy–Reed ratio.
  - Synthetic population generator with heterogeneous individuals
    (cell size, strut thickness, anisotropy, baseline connectivity) and
    parallel execution.
  - Gradient-boosting models with cross-validation grouped by individual,
    leave-one-regime-out evaluation and permutation importance.
- `notebooks/02_early_warning.ipynb` and `figures/02_early_warning.png`.
- `docs/machine_learning.md` (method, results, limitations) and
  `docs/ra_morphometry.md` (published RA HR-pQCT morphometry for
  calibration).
- Optional dependency group `ml` (`scikit-learn`, `pandas`).

### Planned for v0.2.0
- Direction-selective erosion models (so the anisotropy term carries
  information independent of T).
- Full fabric-tensor anisotropy (Cowin-Mehrabadi).
- Sensitivity analysis on α, β, γ weights.

### Planned for v0.3.0
- FEM beam/truss element formulation.
- Effective modulus extraction under uniaxial compression.
- Comparison with Gibson-Ashby scaling laws.

### Planned for v0.4.0
- Validation pipeline against public micro-CT datasets.
- Calibration of critical IRCE threshold (IRCE_c).
