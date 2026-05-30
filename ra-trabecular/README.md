# RA-Trabecular

**A Percolation-Based Framework for Modeling Trabecular Bone Degradation in Rheumatoid Arthritis Using Voronoi Tessellation and Effective Mechanical Connectivity**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--2030--1849-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0006-2030-1849)
[DOI]https://doi.org/10.5281/zenodo.20466007

> **Status:** Concept paper + initial implementation (v0.1.0)
> **Author:** Verónica Zumpano Blumenfeld
> **ORCID:** [0009-0006-2030-1849](https://orcid.org/0009-0006-2030-1849)

---

## Overview

**RA-Trabecular** is an open-source computational framework that reformulates trabecular bone degradation in rheumatoid arthritis (RA) as a **percolation transition over a Voronoi-tessellated network**, rather than as a gradual reduction in bone mineral density.

The framework introduces the **Index of Effective Mechanical Connectivity (IRCE)**, a dimensionless composite metric that integrates:

- **Normalized effective elastic modulus** (from finite element analysis)
- **Topological connectivity** of the load-bearing subnetwork
- **Local anisotropy** of trabecular architecture

The central hypothesis is that RA-driven erosion produces a **critical structural transition** at which the trabecular network fragments mechanically — a regime invisible to standard density-based metrics.

## Why this matters

Current clinical assessment of RA-related bone loss relies on morphological descriptors (erosion volume, BMD, semi-quantitative scoring) that **systematically miss the topological event that determines failure**: loss of structural connectivity.

By treating trabecular degradation as a critical phenomenon, RA-Trabecular aims to identify patients approaching mechanical failure **before** erosion becomes radiographically conspicuous.

## Framework architecture

```
                ┌─────────────────────┐
                │  Voronoi Generation │
                │  (3D seed-based)    │
                └──────────┬──────────┘
                           │
                ┌──────────▼──────────┐
                │ Progressive Erosion │
                │ (edge removal)      │
                └──────────┬──────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──────┐ ┌───▼────┐ ┌────▼─────┐
       │ FEM (E_eff) │ │ Graph  │ │Anisotropy│
       │             │ │ (LCC)  │ │  (MIL)   │
       └──────┬──────┘ └───┬────┘ └────┬─────┘
              └────────────┼────────────┘
                           │
                ┌──────────▼──────────┐
                │       IRCE          │
                │  + critical point   │
                └─────────────────────┘
```

## Key concept: the IRCE

IRCE = α(E_eroded / E_healthy)
     + β(N_LCC / N_total)
     + γA_local

with α + β + γ = 1, IRCE ∈ [0, 1].

- **IRCE = 1** → pristine, fully load-bearing network
- **IRCE → 0** → fragmented, mechanically incompetent structure
- **IRCE_c** → hypothesized critical threshold (universal within a topology class)

A multiplicative (synergistic) formulation is also implemented as an alternative:

$$
\mathrm{IRCE}_{mult} = \left( \frac{E^*_{eroded}}{E^*_{healthy}} \right)^\alpha \cdot \left( \frac{N_{LCC}}{N_{total}} \right)^\beta \cdot A_{local}^\gamma
$$

## Repository structure

```
ra-trabecular/
├── README.md                  # This file
├── LICENSE                    # Apache 2.0
├── CITATION.cff               # Machine-readable citation
├── .zenodo.json               # Zenodo metadata for auto-release
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contribution guidelines
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Package configuration
├── docs/
│   ├── theory.md              # Theoretical foundation
│   ├── irce_definition.md     # Formal IRCE specification
│   └── roadmap.md             # Development plan
├── src/ra_trabecular/
│   ├── __init__.py
│   ├── voronoi.py             # Network generation
│   ├── erosion.py             # Progressive erosion models
│   ├── mechanics.py           # FEM and effective modulus
│   ├── connectivity.py        # Graph-theoretic metrics
│   ├── anisotropy.py          # MIL and anisotropy tensor
│   └── irce.py                # IRCE computation
├── notebooks/
│   └── 01_voronoi_basic.ipynb # First reproducible example
├── tests/
│   └── test_irce.py
├── data/                      # Datasets (or pointers to public ones)
└── figures/                   # Reproducible outputs
```

## Quick start

```bash
# Clone the repository
git clone https://github.com/Vlattice/ra-trabecular.git
cd ra-trabecular

# Create environment and install
pip install -e .

# Run the first example notebook
jupyter notebook notebooks/01_voronoi_basic.ipynb
```

## Minimal example

```python
from ra_trabecular.voronoi import generate_voronoi_network
from ra_trabecular.erosion import progressive_erosion
from ra_trabecular.irce import compute_irce

# 1. Generate a 3D Voronoi trabecular network
network = generate_voronoi_network(n_seeds=200, domain_size=10.0, seed=42)

# 2. Simulate progressive erosion
trajectory = progressive_erosion(network, removal_fraction_steps=20)

# 3. Compute IRCE along the trajectory
irce_values = [compute_irce(state) for state in trajectory]
```

## Citation

If you use RA-Trabecular in academic work, please cite:

> Zumpano Blumenfeld, V. (2026). *RA-Trabecular: A Percolation-Based Framework for Modeling Trabecular Bone Degradation in Rheumatoid Arthritis Using Voronoi Tessellation and Effective Mechanical Connectivity* (Version 0.1.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

Or use the machine-readable `CITATION.cff` file (GitHub will render a "Cite this repository" button automatically).

## Roadmap

- [x] **v0.1.0** — Concept paper + Voronoi generation + basic erosion
- [ ] **v0.2.0** — Connectivity metrics and IRCE (additive form)
- [ ] **v0.3.0** — FEM integration (beam/truss formulation)
- [ ] **v0.4.0** — Validation against public micro-CT datasets
- [ ] **v0.5.0** — Multiplicative IRCE and sensitivity analysis
- [ ] **v1.0.0** — Short Communication submission to *Bone* / *Journal of Biomechanics*

## License

This project is licensed under the **Apache License 2.0** — see [LICENSE](LICENSE) for details.

Apache 2.0 was chosen over MIT because it includes an explicit patent grant clause, providing stronger protection against patent litigation for both authors and users.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Contact

**Verónica Zumpano Blumenfeld**
ORCID: [0009-0006-2030-1849](https://orcid.org/0009-0006-2030-1849)

---

*This work follows open science principles. Each release is archived with a persistent DOI through Zenodo, ensuring long-term reproducibility and citability.*
