# Formal Definition of the IRCE

**Index of Effective Mechanical Connectivity**

**Author:** Verónica Zumpano Blumenfeld
**ORCID:** 0009-0006-2030-1849
**Version:** 0.1.0 (concept-paper aligned)

---

## 1. Definition (additive form)

Let

$$
M = \frac{E^{*}_{\mathrm{eroded}}}
         {E^{*}_{\mathrm{healthy}}}
$$

$$
T=\frac{N_{LCC}}{N_{total}}
$$

$$
A=\frac{A_{local}}{A_{local}^{healthy}}
$$

denote the normalized mechanical, topological, and anisotropy components, respectively.

The Index of Effective Mechanical Connectivity (IRCE) is defined as

$$
\mathrm{IRCE}
=============

\alpha M
+
\beta T
+
\gamma A
$$

subject to

$$
\alpha+\beta+\gamma=1,
\qquad
\alpha,\beta,\gamma\ge0,
\qquad
\mathrm{IRCE}\in[0,1].
$$

By construction, the pristine reference network satisfies

$$
M=T=A=1,
$$

and therefore

$$
\mathrm{IRCE}=1.
$$

---

## 2. Definition (multiplicative form)

An alternative synergistic formulation is

$$
\mathrm{IRCE}_{mult}
====================

M^\alpha
\cdot
T^\beta
\cdot
A^\gamma.
$$

Equivalently,

$$
\mathrm{IRCE}_{mult}
====================

\left(
\frac{E^*_{eroded}}
{E^**{healthy}}
\right)^\alpha
\cdot
\left(
\frac{N*{LCC}}
{N_{total}}
\right)^\beta
\cdot
\left(
\frac{A_{local}}
{A_{local}^{healthy}}
\right)^\gamma.
$$

The multiplicative form models *synergistic structural collapse*: degradation in one component cannot be fully compensated by preservation of the others. It is expected to provide greater sensitivity near the critical regime, where network failure becomes strongly non-linear.

---

## 3. Component Definitions

### 3.1 Effective Modulus Ratio

$$
M=
\frac{E^*_{eroded}}
{E^*_{healthy}}
\in[0,1]
$$

where $E^*$ denotes the apparent elastic modulus of the trabecular network under uniaxial compression along the principal anisotropy axis.

In v0.1.0, $E^*$ is estimated using a Gibson–Ashby-inspired approximation modulated by a connectivity penalty (see `mechanics.py`). Future releases (v0.3.0+) will replace this approximation with full finite-element beam/truss simulations.

Interpretation:

* $M=1$: no mechanical degradation.
* $M\rightarrow0$: near-complete loss of stiffness.

---

### 3.2 Topological Connectivity Ratio

$$
T=
\frac{N_{LCC}}
{N_{total}}
\in[0,1]
$$

where:

* $N_{LCC}$ is the number of load-bearing edges belonging to the Largest Connected Component (LCC);
* $N_{total}$ is the number of load-bearing edges in the pristine network.

Properties:

* Pristine fully connected network: $T=1$.
* Fully fragmented network: $T\rightarrow0$.
* $T$ is monotone non-increasing along any erosion trajectory.

---

### 3.3 Normalized Local Anisotropy

First define the local anisotropy scalar

$$
A_{local}
=========

\frac{\lambda_1-\lambda_3}
{\lambda_1+\lambda_3},
\qquad
0\le A_{local}\le1
$$

where

$$
\lambda_1\ge\lambda_2\ge\lambda_3
$$

are the eigenvalues of the length-weighted edge-orientation tensor

$$
T_{ij}
======

\frac{
\sum_e \ell_e
u_i^{(e)}
u_j^{(e)}
}{
\sum_e \ell_e
}.
$$

Here:

* $\ell_e$ is the length of edge $e$;
* $u^{(e)}$ is the unit direction vector associated with edge $e$.

The normalized anisotropy component used by IRCE is

$$
A
=

\frac{A_{local}}
{A_{local}^{healthy}}.
$$

Interpretation:

* $A=1$: anisotropy preserved relative to the healthy reference.
* $A<1$: degradation of directional load-transfer organization.
* $A\rightarrow0$: collapse of preferential structural alignment.

Future versions will incorporate full fabric-tensor formulations based on Cowin–Mehrabadi theory.

---

## 4. Weight Convention

Default weights:

$$
\alpha=0.4,
\qquad
\beta=0.4,
\qquad
\gamma=0.2.
$$

Rationale:

* Mechanical competence ($M$) and structural connectivity ($T$) are treated as co-dominant contributors.
* Anisotropy ($A$) modulates load-transfer organization but is considered secondary in pure load-bearing failure.

These weights are provisional and will be evaluated through sensitivity analysis and empirical calibration.

---

## 5. Critical IRCE Threshold

The framework hypothesizes the existence of a critical value

$$
\mathrm{IRCE}_c
$$

such that:

* For $\mathrm{IRCE}>\mathrm{IRCE}_c$, the load-bearing backbone remains continuous and mechanical competence is largely preserved.
* For $\mathrm{IRCE}<\mathrm{IRCE}_c$, the network enters a fragmented regime characterized by accelerated stiffness loss.

The threshold is not assumed to be strictly universal. Rather, it is hypothesized to exhibit limited variability within a given topology class and erosion regime.

Estimation procedure:

1. Generate multiple realizations of erosion trajectories.
2. Compute $\mathrm{IRCE}(p_{rem})$.
3. Identify the point of maximal curvature or maximal negative second derivative.
4. Verify stability through finite-size scaling analyses.

---

## 6. Properties

| Property                         | Additive               | Multiplicative     |
| -------------------------------- | ---------------------- | ------------------ |
| Bounds                           | $[0,1]$                | $[0,1]$            |
| Dimensionless                    | Yes                    | Yes                |
| Monotone under erosion           | Yes                    | Yes                |
| Pristine value                   | $1$ (by normalization) | $1$                |
| Sensitive to topological failure | Yes                    | Yes, more strongly |
| Captures non-linear collapse     | Moderately             | Strongly           |
| Falsifiable predictions          | Yes                    | Yes                |

---

## 7. Falsifiability

The IRCE framework makes three explicit, testable predictions:

### Prediction 1: Critical Transition

A reproducible inflection point exists along erosion trajectories and corresponds to the onset of rapid mechanical degradation.

### Prediction 2: Divergence from Density Metrics

Conventional density-based descriptors (BV/TV, BMD) systematically overestimate residual mechanical competence near the critical regime.

### Prediction 3: Superior Mechanical Correlation

IRCE correlates more strongly with measured stiffness and structural competence than density-only metrics when evaluated on realistic trabecular architectures.

Each prediction can be evaluated through the validation pipeline described in `docs/roadmap.md`.

---

*This document constitutes the public and citable specification of the Index of Effective Mechanical Connectivity (IRCE) as implemented in RA-Trabecular v0.1.0. Future revisions will be versioned through GitHub releases and archived through Zenodo to ensure transparency, reproducibility, and traceability.*
