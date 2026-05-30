# Theoretical Foundation

This document summarizes the theoretical pillars on which RA-Trabecular rests. Each pillar is independently established in the literature; the contribution of RA-Trabecular is to integrate the three under a common predictive framework specific to inflammatory bone disease.

---

## 1. Trabecular Bone as a Cellular Solid

Following the canonical treatment of Gibson and Ashby (1997), trabecular (cancellous) bone is mechanically modeled as an open-cell cellular solid.

The normalized effective elastic modulus is approximated by

$$
\frac{E_{eff}}{E_{solid}}
=========================

C
\left(
\frac{\rho_{eff}}{\rho_{solid}}
\right)^n
$$

where:

* (E_{eff}) is the apparent elastic modulus of the trabecular structure.
* (E_{solid}) is the modulus of the bone matrix.
* (\rho_{eff}) is the apparent density.
* (\rho_{solid}) is the density of solid bone tissue.
* (C) is a geometric constant.
* (n) is a topology-dependent exponent.

Typical values are:

* (n \approx 2) for bending-dominated open-cell structures.
* (n \approx 1) for stretch-dominated structures.

### Critical limitation

The Gibson–Ashby scaling law assumes a mechanically connected network.

As trabeculae become disconnected, mechanical competence can collapse abruptly even when density remains relatively high. Density alone therefore becomes a poor predictor of structural integrity near failure.

---

## 2. Voronoi Tessellation as a Generative Geometric Model

A three-dimensional Voronoi tessellation partitions space into convex polyhedral cells generated from a set of seed points.

The resulting edge network provides a useful approximation of trabecular architecture because it is:

* Topologically similar to open-cell cellular solids.
* Statistically controllable through the seed distribution.
* Computationally efficient to generate and analyze.

### Advantages of a Voronoi Representation

1. Reproducible generation of large synthetic trabecular networks.
2. Direct control of density and anisotropy.
3. Compatibility with graph-theoretic analysis.
4. Compatibility with finite-element simulations.
5. Access to analytical concepts from percolation theory.

Patient-specific HR-pQCT and micro-CT models remain the long-term validation target, but are not required for theoretical development.

---

## 3. Percolation and the Rigidity Transition

Percolation theory studies the emergence and disappearance of system-spanning connected components in random networks.

Let

$$
p
$$

denote the fraction of surviving structural elements.

There exists a critical threshold

$$
p_c
$$

at which the largest connected component undergoes a phase transition.

Near this threshold, the giant component follows the scaling relation

$$
P_{\infty}(p)
\sim
(p-p_c)^{\beta}
$$

where:

* (P_{\infty}) is the fraction of elements belonging to the giant connected component.
* (p_c) is the critical threshold.
* (\beta) is a critical exponent.

### Mechanical Interpretation

For cellular solids, loss of stiffness generally occurs before complete geometric disconnection.

This phenomenon is known as rigidity percolation.

A network may remain geometrically connected while no longer possessing a mechanically continuous load-bearing skeleton.

This regime is the primary focus of RA-Trabecular.

---

## 4. RA-Driven Erosion as a Graph Degradation Process

RA-Trabecular models inflammatory trabecular degradation as progressive edge removal on a Voronoi network.

Three erosion regimes are implemented.

| Regime       | Biological Motivation         | Removal Strategy          |
| ------------ | ----------------------------- | ------------------------- |
| Uniform      | Baseline control              | Random edge removal       |
| Peripheral   | Synovial inflammatory erosion | Distance-weighted removal |
| Osteoclastic | Localized osteoclast activity | Hotspot-driven removal    |

Each erosion process generates a degradation trajectory that is evaluated using the IRCE framework.

---

## 5. Why This Integration Matters

The three theoretical pillars already exist independently:

* Cellular-solids theory provides density–stiffness relationships.
* Voronoi modeling provides realistic synthetic trabecular geometries.
* Percolation theory describes connectivity loss and critical transitions.

However, these frameworks are rarely combined into a single quantitative model of inflammatory bone degradation.

RA-Trabecular integrates them through the Index of Effective Mechanical Connectivity (IRCE), a dimensionless metric designed to track the progression from a mechanically competent trabecular network to a fragmented structure approaching failure.

The central hypothesis is that clinically relevant deterioration is driven primarily by loss of connectivity rather than loss of mass alone.

---

## References

See the concept paper, README.md, and associated Zenodo release for the complete bibliography.
