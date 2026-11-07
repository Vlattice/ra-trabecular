# Machine-learning early warning of trabecular collapse

**Module:** `ra_trabecular.ml` · **Notebook:** [`notebooks/02_early_warning.ipynb`](../notebooks/02_early_warning.ipynb) · **Status:** v0.2.0-dev (synthetic data)

---

## 1. Question

Given a *single* scan of a trabecular network, with no access to the patient's healthy baseline, how close is it to mechanical collapse?

This is the clinically relevant form of the IRCE hypothesis: identify bone approaching structural failure *before* the failure is visible. The IRCE itself requires the healthy reference network (for $M$, $T$ and $A$); a patient scan does not provide one.

## 2. Task

Each sample is a snapshot of an eroded network. Its label is the remaining erosion budget before the percolation transition:

$$
\delta = p_c - p
$$

where $p$ is the fraction of struts removed and $p_c$ is the trajectory's critical erosion fraction, defined as the interpolated point at which the percolation order parameter $P_\infty$ first falls below 0.5. Networks with $0 \le \delta \le 0.10$ are labelled **at risk**.

## 3. Reference-free features

Computed from the snapshot alone (`ra_trabecular.ml.features`):

| Group | Features |
|---|---|
| Density | BV/TV, mean strut thickness, strut length density |
| Topology | connectivity density (cycle rank / volume), mean degree, fraction of dangling ends, fraction of bridges in the largest cluster, largest-cluster edge fraction, cluster density, mean finite-cluster size, cycle rank per edge, Molloy–Reed ratio $\langle k^2\rangle/\langle k\rangle$ |
| Anisotropy | normalized fabric-tensor eigenvalues, $A_{local}$ |

## 4. Synthetic population

Each "individual" is a Voronoi network drawn with heterogeneous parameters, so that neither density nor mean degree reveals $p$ trivially:

* seed count 120–260 (cell size), mean strut thickness 0.10–0.20, z-anisotropy 1.0–2.0, 30 % perturbed-lattice seeds;
* a random **baseline pruning** of 0–25 % of struts, so individuals differ in baseline connectivity (healthy mean degree 2.9–3.8).

Every individual is eroded under the three regimes (uniform, peripheral, osteoclastic) in 37 steps up to 90 % strut removal.

## 5. Evaluation

Gradient-boosted regression trees (`HistGradientBoostingRegressor`), 5-fold cross-validation **grouped by individual**, metrics on still-connected snapshots.

Results for 80 individuals (8,880 snapshots, `RNG_SEED = 2026`):

| Features | MAE | R² | AUC (at risk) |
|---|---|---|---|
| Density only | 0.131 | −0.07 | 0.80 |
| **Topology only** | **0.033** | **0.92** | **0.98** |
| All | 0.034 | 0.91 | 0.98 |
| Mean degree only | 0.041 | 0.88 | 0.97 |
| Molloy–Reed ratio only | 0.049 | 0.83 | 0.96 |
| IRCE (requires healthy baseline) | 0.043 | 0.88 | 0.97 |

**Unseen erosion regime** (train on two regimes, test on the third, disjoint individuals): topology R² = 0.72–0.89, AUC ≥ 0.97; density R² < 0.

## 6. Findings

1. **Density does not predict proximity to collapse** once individuals differ in strut thickness and cell size: equal BV/TV can correspond to very different distances from the transition.
2. **Connectivity does**, from a single snapshot and without a baseline, and it transfers across erosion regimes. This supports prediction 2 of the IRCE framework (divergence between connectivity-based and density-based metrics near collapse).
3. The dominant signal is the **node-degree distribution**: mean degree, dangling ends and the Molloy–Reed ratio. In random graphs a giant component exists iff $\langle k^2\rangle/\langle k\rangle > 2$; here the transition occurs at $\kappa = 2.48 \pm 0.15$, as expected for spatially embedded networks with loops.
4. A reference-free topology model matches or exceeds the reference-based IRCE for this task.

## 7. Limitations

* All data are synthetic (Voronoi edge networks with strut-removal erosion).
* Erosion removes struts but does not thin them; RA also causes trabecular thinning (see [`ra_morphometry.md`](ra_morphometry.md)).
* $p_c$ is defined topologically ($P_\infty$ = 0.5), not from a mechanical failure criterion; coupling to FEM is planned for v0.3.0.
* Clinical translation requires graph extraction from real micro-CT / HR-pQCT volumes by skeletonization, where node degree is measurable (roadmap v0.4.0).

## 8. Reproduce

```bash
pip install -e ".[ml]"
jupyter nbconvert --to notebook --execute notebooks/02_early_warning.ipynb
```

```python
from ra_trabecular.ml import generate_dataset, evaluate_feature_sets

df = generate_dataset(n_networks=80, rng_seed=2026, n_jobs=-1)
for r in evaluate_feature_sets(df):
    print(r.feature_set, round(r.r2_connected, 3), round(r.auc_at_risk, 3))
```
