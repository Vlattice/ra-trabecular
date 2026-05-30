# Notebooks

This folder contains the computational notebooks for the RA-Trabecular framework.

### Notebooks List

* **01: First Reproducible Example** [ Ver vista previa rápida en GitHub (Recomendado)] (01_voronoi_basic.md) | [ Descargar archivo original (.ipynb)](01_voronoi_basic.ipynb) | 

This directory contains reproducible Jupyter notebooks demonstrating the RA-Trabecular framework.

## Index

| Notebook | Version | Description |
|----------|---------|-------------|
| `01_voronoi_basic.ipynb` | v0.1.0 | First reproducible example: Voronoi generation, erosion under three regimes, IRCE trajectory, critical point estimation. |
| `02_irce_sensitivity.ipynb` | v0.2.0 (planned) | Sensitivity analysis on α, β, γ weights and multi-realization statistics. |
| `03_fem_vs_approx.ipynb` | v0.3.0 (planned) | Full FEM modulus vs. approximate Gibson-Ashby estimator. |
| `04_microct_validation.ipynb` | v0.4.0 (planned) | Validation against public micro-CT datasets. |

## How to run

From the repository root:

```bash
pip install -e ".[all]"
jupyter notebook notebooks/
```

All notebooks use `RNG_SEED = 42` by default for reproducibility. Output figures are written to `../figures/`.
