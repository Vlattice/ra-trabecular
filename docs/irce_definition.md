# Formal Definition of the IRCE

**Index of Effective Mechanical Connectivity**

**Author:** Verónica Zumpano Blumenfeld
**ORCID:** 0009-0006-2030-1849
**Version:** 0.1.1 — concept DOI: https://doi.org/10.5281/zenodo.20467022

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
A = \frac{\mathbf{e}_1^{\top} F_{eroded}\, \mathbf{e}_1}{\mathbf{e}_1^{\top} F_{healthy}\, \mathbf{e}_1}
$$

denote the normalized mechanical, topological, and anisotropy components, respectively (see Section 3.3 for $F$ and $\mathbf{e}_1$).

All three components equal 1 for the pristine network, so $IRCE = 1$ for the healthy reference and $IRCE \rightarrow 0$ as the network fragments.

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

Since v0.1.1, the effective modulus is estimated with a Gibson–Ashby scaling law applied to the load-bearing subnetwork only:

$$
E^* \approx C\, E_s\, \phi_{eff}^{\,n}, \qquad \phi_{eff} = \frac{V_{struts}(LCC)}{V_{domain}}
$$

with $n = 2$ (bending-dominated). Disconnected fragments carry no load, so connectivity enters $M$ through $\phi_{eff}$. Connectivity therefore enters the IRCE through a single explicit term, $T$. An estimator with an additional $N_{LCC}/N_{total}$ factor is available as `connectivity_penalty=True` for comparison (see `mechanics.py`). Future releases (v0.3.0+) will replace this approximation with full finite-element beam/truss simulations.

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

### 3.3 Anisotropy Component

Let $F$ be the length-weighted fabric (orientation) tensor of the load-bearing subnetwork (largest connected component):

$$
F = \sum_{k \in LCC} L_k\, \mathbf{u}_k \mathbf{u}_k^{\top}
$$

where $L_k$ and $\mathbf{u}_k$ are the length and unit direction of strut $k$, and let $\mathbf{e}_1$ be the principal eigenvector of $F_{healthy}$ (the dominant load axis of the healthy architecture). The anisotropy component is the fraction of healthy fabric retained along that axis:

$$
A = \frac{\mathbf{e}_1^{\top} F_{eroded}\, \mathbf{e}_1}{\mathbf{e}_1^{\top} F_{healthy}\, \mathbf{e}_1}
$$

clipped to $[0, 1]$, with $A = 0$ if no load-bearing subnetwork remains.

**Interpretation**

* $A = 1$: the struts aligned with the principal load axis are preserved.
* $A \rightarrow 0$: the load-axis architecture is lost.

**Alternative formulation.** The ratio $A = A_{local}/A_{healthy}$, with $A_{local} = (\lambda_1 - \lambda_3)/(\lambda_1 + \lambda_3)$, describes the *shape* of the orientation distribution rather than the amount of load-axis architecture retained. For near-isotropic networks ($A_{healthy} \approx 0.08$ for Poisson–Voronoi) it is not a stable measure of degradation, so the retention form above is used by default. The ratio form is available as `anisotropy_mode="ratio"` for sensitivity analysis.

**Scope.** Under spatially isotropic erosion, $A$ closely tracks $T$. The anisotropy term carries independent information only when erosion is direction-selective (e.g. preferential loss of transverse or longitudinal trabeculae), which is a target for future erosion models.

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

*This document is part of the public, citable record of the IRCE formulation (v0.1.1; changes from v0.1.0 are listed in `CHANGELOG.md`). Subsequent revisions will be tracked through GitHub releases and Zenodo archives.*
