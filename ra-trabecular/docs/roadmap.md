# Development Roadmap

This document outlines the planned trajectory of RA-Trabecular development. Each milestone corresponds to a tagged release archived on Zenodo with a persistent DOI.

## v0.1.0 — Foundation (current)

**Status:** released 2026-05-30.

- Concept paper v1.0 (archived independently on Zenodo).
- Voronoi network generation.
- Three erosion regimes: uniform, peripheral, osteoclastic.
- Connectivity metrics (LCC, percolation order parameter).
- Local anisotropy via length-weighted orientation tensor.
- IRCE additive and multiplicative formulations.
- Approximate effective modulus via Gibson-Ashby + LCC penalty.
- Test scaffolding and first reproducible notebook.

## v0.2.0 — Expanded metrics

**Target:** Q3 2026.

- Full fabric-tensor anisotropy (Cowin-Mehrabadi).
- Sensitivity analysis on $\alpha, \beta, \gamma$ weights.
- Multi-realization statistics: distribution of IRCE_c across seeds.
- Comparison plots: IRCE vs. BV/TV vs. SMI vs. Tb.Th.
- Companion notebook: `02_irce_sensitivity.ipynb`.

## v0.3.0 — Full FEM integration

**Target:** Q4 2026.

- Beam/truss FEM via `scikit-fem` (Euler-Bernoulli or Timoshenko).
- Effective modulus extraction under prescribed boundary conditions.
- Comparison of approximate vs. FEM-derived modulus.
- Calibration of Gibson-Ashby pre-factor against FEM results.
- Companion notebook: `03_fem_vs_approx.ipynb`.

## v0.4.0 — Validation pipeline

**Target:** Q1 2027.

- Loader for public micro-CT datasets (BoneJ, SciDataBank, Visible Human derivatives).
- Skeletonization and graph extraction from binary volumes.
- Cross-validation of IRCE against published mechanical testing data.
- Estimation of IRCE_c on real datasets.
- Companion notebook: `04_microct_validation.ipynb`.

## v0.5.0 — Clinical-scale extension

**Target:** Q2 2027.

- Patient-specific HR-pQCT pipeline (registration + segmentation interface).
- Comparison of IRCE in RA vs. control cohorts using public datasets where available.
- Integration with morphometric pipelines (BoneJ, ImageJ).
- Companion notebook: `05_patient_specific.ipynb`.

## v1.0.0 — Short Communication

**Target:** Q3 2027.

- Release coincident with submission of a peer-reviewed Short Communication to *Bone* or *Journal of Biomechanics*.
- Frozen, reproducible artifact backing all figures of the manuscript.
- Final calibration of weights and critical thresholds.
- Open dataset of synthetic Voronoi-based RA-trabecular networks for community use.

## Future directions (post v1.0)

- **Coupling to biology:** osteoclast/osteoblast feedback dynamics, cytokine field models.
- **Generalization:** osteoporosis, psoriatic arthritis, subcondral OA, avascular necrosis, peri-implant bone loss.
- **Hardware integration:** real-time IRCE estimation from HR-pQCT/micro-CT in clinical workflows.
- **Spinoff possibilities:** prognostic biomarker validation studies, partnership with imaging vendors.

---

*The roadmap is a living document. Pull requests proposing additions or reorderings are welcome.*
