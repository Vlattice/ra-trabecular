# Formal Definition of the IRCE

**Index of Effective Mechanical Connectivity**

**Author:** Verónica Zumpano Blumenfeld
**ORCID:** 0009-0006-2030-1849
**Version:** 0.1.0 https://doi.org/10.5281/zenodo.20467022

---

## 1. Definition (additive form)

Let

$$
M = \frac{E_{eroded}}{E_{healthy}}
$$

$$
T = \frac{N_{LCC}}{N_{total}}
$$

$$
A = \frac{A_{local}}{A_{healthy}}
$$

denote the normalized mechanical, topological, and anisotropy components, respectively.

The Index of Effective Mechanical Connectivity (IRCE) is defined as

$$
IRCE = \alpha M + \beta T + \gamma A
$$

subject to

$$
\alpha + \beta + \gamma = 1
$$

with

$$
\alpha,\beta,\gamma \ge 0
$$

and

$$
0 \le IRCE \le 1
$$

---

## 2. Definition (multiplicative form)

An alternative synergistic formulation is

$$\mathrm{IRCE}_{\mathrm{mult}} = M^{\alpha} \cdot T^{\beta} \cdot A^{\gamma}$$

Equivalently,

$$\mathrm{IRCE}_{\mathrm{mult}} = \left( \frac{E_{\mathrm{eroded}}}{E_{\mathrm{healthy}}} \right)^{\alpha} \cdot \left( \frac{N_{\mathrm{LCC}}}{N_{\mathrm{total}}} \right)^{\beta} \cdot \left( \frac{A_{\mathrm{local}}}{A_{\mathrm{healthy}}} \right)^{\gamma}$$

The multiplicative form models synergistic structural collapse: degradation in one component cannot be fully compensated by preservation of the others. It is expected to provide greater sensitivity near the critical regime, where network failure becomes strongly non-linear.

## 3. Component Definitions

### 3.1 Effective Modulus Ratio

$$
M =
\frac{E_{eroded}}
{E_{healthy}}
$$

with

$$
0 \le M \le 1
$$

where:

* $E_{eroded}$ is the effective elastic modulus after erosion.
* $E_{healthy}$ is the effective elastic modulus of the pristine reference network.

In v0.1.0, the effective modulus is estimated using a Gibson–Ashby-inspired approximation modulated by a connectivity penalty (see `mechanics.py`). Future releases (v0.3.0+) will replace this approximation with full finite-element beam/truss simulations.

**Interpretation**

* $M = 1$: no mechanical degradation.
* $M \rightarrow 0$: near-complete loss of stiffness.

### 3.2 Topological Connectivity Ratio

$$
T =
\frac{N_{LCC}}
{N_{total}}
$$

with

$$
0 \le T \le 1
$$

where:

* $N_{LCC}$ is the number of edges in the largest connected component.
* $N_{total}$ is the total number of load-bearing edges in the pristine network.

**Interpretation**

* $T = 1$: fully connected network.
* $T \rightarrow 0$: highly fragmented network.

### 3.3 Local Anisotropy Ratio

$$
A =
\frac{A_{local}}
{A_{healthy}}
$$

with

$$
0 \le A \le 1
$$

where:

* $A_{local}$ is the anisotropy of the eroded network.
* $A_{healthy}$ is the anisotropy of the healthy reference network.

**Interpretation**

* $A = 1$: anisotropy preserved.
* $A \rightarrow 0$: anisotropic structure lost.

---

## 4. Weight Convention

Default weights:

$$
\alpha = 0.4
$$

$$
\beta = 0.4
$$

$$
\gamma = 0.2
$$

Rationale: modulus ratio and connectivity ratio are co-dominant contributors to structural competence, while anisotropy acts as a secondary modifier.

---

## 5. Critical IRCE Threshold

The framework hypothesizes the existence of a critical value:

$$
IRCE_c
$$

such that:

* $IRCE > IRCE_c$: mechanically competent network.
* $IRCE < IRCE_c$: fragmented network with catastrophic stiffness loss.

The value of $IRCE_c$ depends on topology class and erosion regime and will be estimated through finite-size scaling and trajectory analysis.

---

## 6. Falsifiable Predictions

The IRCE framework makes three testable predictions:

1. Existence of a reproducible critical transition along erosion trajectories.
2. Divergence between IRCE and density-based metrics near structural collapse.
3. Stronger correlation with measured stiffness than density-only descriptors.

---

*This document is part of the public, citable record of the IRCE formulation (v0.1.0). Subsequent revisions will be tracked through GitHub releases and Zenodo archives.*
