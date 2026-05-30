# Formal Definition of the IRCE

**Index of Effective Mechanical Connectivity**

Author: Verónica Zumpano Blumenfeld
ORCID: 0009-0006-2030-1849
Version: 0.1.0 (concept-paper aligned)

---

## 1. Definition (additive form)

$$
\mathrm{IRCE} = \alpha \cdot \frac{E^*_{eroded}}{E^*_{healthy}}
              + \beta  \cdot \frac{N_{LCC}}{N_{total}}
              + \gamma \cdot A_{local}
$$

subject to

$$
\alpha + \beta + \gamma = 1, \quad \alpha, \beta, \gamma \geq 0, \quad \mathrm{IRCE} \in [0, 1].
$$

## 2. Definition (multiplicative form)

$$
\mathrm{IRCE}_{mult} = \left( \frac{E^*_{eroded}}{E^*_{healthy}} \right)^\alpha
                     \cdot \left( \frac{N_{LCC}}{N_{total}} \right)^\beta
                     \cdot A_{local}^\gamma
$$

The multiplicative form models *synergistic* structural collapse: loss of one component cannot be compensated by the others. It is provided as an alternative and is expected to outperform the additive form near the critical regime, where collapse is non-linear.

## 3. Component definitions

### 3.1 Effective modulus ratio

$$
M = \frac{E^*_{eroded}}{E^*_{healthy}} \in [0, 1]
$$

with $E^*$ the apparent elastic modulus of the trabecular network under uniaxial compression along the principal anisotropy axis. In v0.1.0, $E^*$ is computed via the Gibson-Ashby approximation modulated by an LCC penalty (see `mechanics.py`); in v0.3.0 this will be replaced with a full FEM beam/truss computation.

### 3.2 Topological connectivity ratio

$$
T = \frac{N_{LCC}}{N_{total}} \in [0, 1]
$$

with $N_{LCC}$ the number of edges contained in the largest connected component of the load-bearing subnetwork, and $N_{total}$ the initial (pristine) number of load-bearing edges.

Properties:
- Pristine fully connected network: $T = 1$.
- Fully fragmented: $T \to 0$.
- $T$ is monotone non-increasing along any erosion trajectory.

### 3.3 Local anisotropy scalar

$$
A_{local} = \frac{\lambda_1 - \lambda_3}{\lambda_1 + \lambda_3} \in [0, 1]
$$

where $\lambda_1 \geq \lambda_2 \geq \lambda_3$ are the eigenvalues of the length-weighted edge-orientation tensor

$$
T_{ij} = \frac{\sum_e \ell_e \, u^{(e)}_i u^{(e)}_j}{\sum_e \ell_e}
$$

with $\ell_e$ the length of edge $e$ and $u^{(e)}$ its unit direction vector.

Interpretation:
- $A_{local} = 0$: perfectly isotropic edge orientation.
- $A_{local} \to 1$: strong alignment along a single principal axis.

In v0.2.0 this will be extended to the full fabric tensor (Cowin–Mehrabadi) formalism.

## 4. Weight convention

Default weights:

$$
\alpha = 0.4, \quad \beta = 0.4, \quad \gamma = 0.2.
$$

Rationale: modulus ratio and connectivity ratio are co-dominant; anisotropy modulates orientational integrity but is secondary in pure load-bearing failure. These weights are subject to sensitivity analysis (planned for v0.2.0) and to eventual data-driven calibration against micro-CT-based mechanical testing (planned for v0.4.0).

## 5. Critical IRCE threshold

The framework hypothesizes the existence of a critical IRCE value $\mathrm{IRCE}_c$ such that:

- For $\mathrm{IRCE} > \mathrm{IRCE}_c$: load-bearing backbone is continuous; mechanical competence is preserved.
- For $\mathrm{IRCE} < \mathrm{IRCE}_c$: backbone fragmented; catastrophic loss of stiffness.

The numerical value of $\mathrm{IRCE}_c$ depends on the topology class of the network (e.g., Voronoi vs. perturbed lattice) and on the erosion regime. It is estimated by:

1. Generating multiple realizations of an erosion trajectory.
2. Identifying the inflection point in $\mathrm{IRCE}(p_{rem})$ where the second derivative is maximally negative.
3. Validating via finite-size scaling that the inflection position is approximately invariant across realizations.

## 6. Properties

| Property | Additive | Multiplicative |
|----------|----------|----------------|
| Bounds | $[0, 1]$ | $[0, 1]$ |
| Monotone w.r.t. erosion | Yes | Yes |
| Pristine value | $\alpha + \beta + \gamma \cdot A_{local}^0 = 1$ (if $A_{local}^0 = 1$) | $1$ (if all components = 1) |
| Sensitive to topological failure even at finite density | Yes | Yes, more strongly |
| Dimensionless | Yes | Yes |
| Falsifiable predictions | Critical threshold; divergence from density metrics | Same, with sharper transition |

## 7. Falsifiability

The IRCE makes three falsifiable predictions:

1. **Inflection at $\mathrm{IRCE}_c$**: a regime of accelerated decrease of IRCE along the erosion trajectory exists and its location is approximately reproducible across realizations of the same topological class.
2. **Divergence from density**: standard density-based metrics overestimate residual mechanical competence near the critical regime, and the divergence is maximal in the early-to-moderate erosion regime (clinically relevant in early RA).
3. **Cross-validation against micro-CT**: when applied to real (or realistic) datasets, IRCE correlates with measured stiffness more strongly than BV/TV alone.

Each of these predictions can be tested by the validation pipeline in `docs/roadmap.md`.

---

*This document is part of the public, citable record of the IRCE formulation as of v0.1.0. Subsequent revisions will be tracked in `CHANGELOG.md` and reflected in new releases archived on Zenodo.*
