# Data

This directory is reserved for datasets used in validation pipelines (v0.4.0 onward).

## Planned public datasets

| Dataset | Type | URL | Use |
|---------|------|-----|-----|
| BoneJ test images | micro-CT, healthy + osteoporotic cancellous bone | https://bonej.org | Validation v0.4.0 |
| Visible Human Project | full-body CT/MR | https://www.nlm.nih.gov/research/visible/ | Reference geometry |
| SciDataBank bone repositories | μCT cancellous bone cubes | https://scidatabank.org (placeholder) | Calibration of E*/E_healthy |

## Local layout (when populated)

```
data/
├── raw/         # raw scans, not tracked by git
├── processed/   # binary volumes, skeletons, graphs
└── README.md
```

Raw data files are excluded from version control (see `.gitignore`).
