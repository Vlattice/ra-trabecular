# Theoretical Foundation

This document summarizes the theoretical pillars on which RA-Trabecular rests. Each pillar is independently established in the literature; the contribution of RA-Trabecular is to integrate the three under a common predictive framework specific to inflammatory bone disease.

## 1. Trabecular bone as a cellular solid

Following the canonical treatment of Gibson and Ashby (1997), trabecular (cancellous) bone is mechanically modeled as an open-cell cellular solid. The effective elastic modulus $E^*$ scales with relative density $\rho^*/\rho_s$ as:

$$
\frac{E^*}{E_s} = C \cdot \left(\frac{\rho^*}{\rho_s}\right)^n
$$

with $n \approx 2$ for bending-dominated open-cell foams (the generic regime of cancellous bone), $n \approx 1$ for stretch-dominated structures, $C$ a geometric pre-factor, and $E_s$ the modulus of the solid bone matrix.

**Critical limitation:** the Gibson-Ashby law assumes a *connected* network. Once the load-bearing backbone fragments, the scaling fails non-linearly. This is the regime of clinical interest.

## 2. Voronoi tessellation as a generative geometric model

A 3D Voronoi tessellation partitions space into convex polyhedral cells given a set of seed points. The edge graph of the tessellation is:

- **Topologically faithful** to open-cell cellular solids (Roberts & Garboczi, 2002).
- **Statistically tunable**: seed distribution controls cell-size distribution; anisotropic seed perturbation produces preferential alignment matching physiological trabecular orientation.
- **Computationally tractable**: standard algorithms (Qhull, scipy.spatial) generate the tessellation in $O(N \log N)$ time.

**Why Voronoi rather than CT-derived geometry?** Voronoi enables:
1. Reproducible, parameterized degradation simulations.
2. Analytical access via random geometric graph theory.
3. Generation of large network ensembles for statistical analysis.

Patient-specific CT-derived models remain the validation target (planned for v0.4.0) but are not the right level for theoretical development.

## 3. Percolation and the rigidity transition

Percolation theory (Stauffer & Aharony, 1994) studies the emergence of system-spanning connected components in random networks as a function of an occupation parameter $p$. For 3D random networks there exists a critical fraction $p_c$ at which the largest connected component undergoes a phase transition.

Near the critical point, the order parameter — the fraction of nodes in the giant component — follows a universal scaling law:

$$
P_\infty(p) \sim (p - p_c)^\beta
$$

with $\beta$ a critical exponent characteristic of the universality class.

**Mechanical analog (rigidity percolation):** for bending-dominated networks, the effective elastic modulus exhibits a *rigidity transition* that generically *precedes* geometric percolation (Maxwell, 1864; Thorpe & Phillips). This means a network can lose its mechanical integrity while still being geometrically connected — its struts no longer form a rigid skeleton.

This is exactly the regime in which RA-Trabecular predicts that standard density-based metrics fail catastrophically.

## 4. RA-driven erosion as an erosion regime on the Voronoi graph

The framework treats RA-driven trabecular degradation as a stochastic edge-removal process on the Voronoi graph, with three regimes implemented in `erosion.py`:

| Regime | Biological motivation | Removal weight |
|--------|----------------------|----------------|
| Uniform | Control / baseline | Uniform |
| Peripheral | Synovial-interface inflammatory erosion | Distance from domain center, squared |
| Osteoclastic | Localized osteoclast activity fields | Sum of Gaussians around random hotspots |

All three regimes share the same downstream pipeline (IRCE computation), enabling direct comparison.

## 5. Why this integration is non-trivial

The three pillars exist in the literature in isolation:

- Gibson-Ashby is well-established in mechanical engineering but rarely combined with explicit topological metrics.
- Voronoi models of bone exist (Kadkhodapour, Wang, et al.) but are usually used for scaffold design, not pathological degradation.
- Percolation has been applied to osteoporotic bone (Parkinson & Fazzalari) but without an integrated, falsifiable mechanical index.

RA-Trabecular's contribution is the IRCE: a single, dimensionless, bounded, computable metric that operationalizes the convergence of these three frameworks into a clinically meaningful trajectory.

## References

See `README.md` and the v1.0 concept paper for the full reference list.
