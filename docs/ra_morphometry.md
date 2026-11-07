# Published trabecular morphometry in rheumatoid arthritis

Reference values for calibrating synthetic networks and erosion depth against published HR-pQCT studies of RA patients versus healthy controls. No raw images are required: only the summary statistics reported in the papers.

> **Before using these values in a manuscript, check each one against the original table.** Several entries were extracted from abstracts or search snippets; where the anatomical site or subgroup of a value could not be confirmed, it is flagged.

---

## 1. Summary table

| Study | Site | Population | Parameter | Controls | RA | Δ (RA vs controls) |
|---|---|---|---|---|---|---|
| Simon et al. 2017, *JBMR* 32(4):722–730 ([doi](https://doi.org/10.1002/jbmr.3025)) | 2nd metacarpal head and radius ⚠️ | 108 HC, 106 RA, men and women | BV/TV | 0.16 ± 0.03 | 0.14 ± 0.03 | −12.5 % |
| | | | Tb.N (1/mm) | 1.44 ± 0.43 | 1.27 ± 0.46 | −11.8 % |
| | | | Tb.Sp (mm) | 0.65 ± 0.24 | 0.79 ± 0.33 | +21.5 % |
| | second site ⚠️ | | BV/TV | 0.14 ± 0.03 | 0.12 ± 0.03 | −14.3 % |
| | | | Tb.Sp (mm) | 0.44 ± 0.11 | 0.51 ± 0.14 | +15.9 % |
| Watanabe et al. 2024, *Bone* ([PubMed 39237048](https://pubmed.ncbi.nlm.nih.gov/39237048/)) | 2nd–3rd MCP joints | 50 HC, 50 RA, women 50–79 y | Tb.BMD (mg/cm³) | 167 | 127 | −24 % |
| | | | Tb.Th (mm) | 0.21 | 0.20 | −4.8 % |
| | | | Tb.N (1/mm) | 1.55 | 1.49 | −3.9 % |
| | | | SMI | — | more rod-like | — |
| *Clin Exp Rheumatol* HR-pQCT MCP/PIP study ([link](https://www.clinexprheumatol.org/abstract.asp?a=6068)) | 2nd MCP | 30 RA, 30 matched controls | Tb.N (1/mm) | 2.31 ± 0.15 | 2.44 ± 0.15 | +5.6 % ⚠️ |
| | | | Tb.Th (mm) | 0.273 ± 0.006 | 0.284 ± 0.034 | +4.0 % |
| | | | Tb.Sp (mm) | 0.367 ± 0.032 | 0.338 ± 0.032 | −7.9 % |
| Burghardt et al. 2013, *Ann Biomed Eng* | radius (⚠️ confirm) | RA vs controls | Tb.N (1/mm) | 2.11 | 1.63 | −22.7 % |
| | radius / tibia | | Tb.BMD (mg/cm³) | 150.3 / 166.2 | 114.8 / 129.3 | −24 % / −22 % |
| Zhu et al. 2013, *JBMR* ([doi](https://doi.org/10.1002/jbmr.1793)) | distal radius | women, RA vs age-matched controls | microstructure indices | — | 5.7 % to 23.1 % worse | significant for BV/TV, Tb.Sp, inhomogeneity |
| Kocijan et al. 2014, *JBMR* 29:1005 ([PubMed 24123099](https://pubmed.ncbi.nlm.nih.gov/24123099/)) | distal and ultradistal radius | 70 HC, 90 RA | BV/TV | — | lower | via lower Tb.N (women) and lower Tb.Th (men) |

⚠️ = site, subgroup or direction to verify in the original paper. The *Clin Exp Rheumatol* cohort reports *higher* Tb.N in RA at the 2nd MCP, opposite to the other studies.

## 2. What the numbers say

* **Typical cohort-level loss is moderate:** BV/TV −12 % to −14 %, Tb.N −4 % to −23 %, Tb.Sp +16 % to +22 %, Tb.Th about −5 %.
* **Loss is mostly by number, not thickness.** Tb.N and Tb.Sp change more than Tb.Th, i.e. trabeculae are removed rather than thinned. This is the regime the framework models (strut removal).
* **Shift towards rod-like architecture** (higher SMI, Watanabe 2024) is consistent with loss of plate connectivity.

## 3. Mapping to the model

In the Voronoi framework, strut removal fraction $p$ reduces Tb.N and BV/TV roughly in proportion. A cohort-average loss of 10–20 % therefore corresponds to $p \approx 0.10$–$0.20$, well below the transition ($p_c \approx 0.47$–$0.52$, see [`machine_learning.md`](machine_learning.md)). That is, **the average RA patient is far from collapse**, and the clinically relevant group is the tail of the distribution, which is exactly what an early-warning model must identify.

Suggested calibration procedure:

1. Choose generator parameters (`n_seeds`, `mean_thickness`) so that healthy synthetic networks match control Tb.N, Tb.Th and BV/TV at the target site, using standard morphometry of the voxelized network.
2. Choose the erosion depth $p$ so that the mean eroded network matches the RA values.
3. Use the SDs to set the spread of individual parameters (`GenerationRanges`).

## 4. Gaps

* No study found provides open image data for RA trabecular bone; the values above are the usable public evidence.
* Sites differ (metacarpal head vs radius vs tibia) and are not interchangeable; periarticular (MCP) values are the most relevant for RA-specific erosion.
