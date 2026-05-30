# Changelog

All notable changes to RA-Trabecular will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-30

### Added
- Concept paper v1.0 (archived independently on Zenodo). https://doi.org/10.5281/zenodo.20466007
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
- Zenodo metadata configuration (`.zenodo.json`).
- Test scaffolding (`tests/test_irce.py`).

### Notes
- This release establishes prior art and timestamps the IRCE formulation.
- FEM module is scaffolded but not yet integrated; targeted for v0.3.0.

## Work in progress

### Planned for v0.2.0
- Multiplicative (synergistic) IRCE formulation.
- Anisotropy tensor computation via fabric tensor (Cowin-Mehrabadi).
- Sensitivity analysis on α, β, γ weights.

### Planned for v0.3.0
- FEM beam/truss element formulation.
- Effective modulus extraction under uniaxial compression.
- Comparison with Gibson-Ashby scaling laws.

### Planned for v0.4.0
- Validation pipeline against public micro-CT datasets.
- Calibration of critical IRCE threshold (IRCE_c).
