# Changelog

All notable changes to RA-Trabecular will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] — 2026-11-07

### Fixed
- **IRCE of the pristine network is now exactly 1.** In v0.1.0 the anisotropy
  term used the raw descriptor `A_local` (≈ 0.08 for Voronoi networks) instead
  of a component normalized against the healthy reference, as specified in
  `docs/irce_definition.md`, so the pristine IRCE was ≈ 0.82.
- **Anisotropy component redefined** as the fraction of healthy fabric retained
  along the healthy principal load axis, evaluated on the load-bearing
  subnetwork (`anisotropy_mode="retention"`, default). The literal ratio
  `A_local / A_healthy` is noise-dominated for near-isotropic networks and
  grows as the network fragments, which prevented the IRCE from approaching 0;
  it remains available as `anisotropy_mode="ratio"`.
- **Connectivity no longer counted three times.** The modulus estimator
  multiplied the LCC-based volume fraction by an extra `N_LCC / N_total`
  factor, on top of the separate `T` term. The factor is now off by default
  (`connectivity_penalty=True` reproduces v0.1.0).
- Domain volume and erosion geometry now account for `anisotropy_factor`
  (z-stretched domains).
- The IRCE is now non-increasing along erosion trajectories for all regimes
  (tiny fluctuations, < 0.001, can remain deep in the fragmented regime when
  the identity of the largest cluster switches).

### Changed
- Default `max_removal_fraction` raised from 0.5 to 0.8 so default
  trajectories cross the percolation transition (≈ 50–60 % of edges removed).
- Repository flattened: the package now lives at the repository root, so
  `git clone … && cd ra-trabecular && pip install -e .` works.
- README: corrected the minimal example (it used non-existent arguments),
  the citation DOI and the roadmap status.
- `IRCEResult` gains `anisotropy_local` (raw descriptor) and `anisotropy_mode`.

### Added
- `notebooks/01_voronoi_basic.ipynb` now contains executable code that
  reproduces `figures/01_irce_trajectory.png`.
- `load_bearing_subnetwork`, `anisotropy_component`, `irce_components`.
- Tests: pristine IRCE = 1 for both formulations, monotonicity for every
  regime, collapse past the transition, legacy-mode reproducibility.

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
