## 1. Trabecular Bone as a Cellular Solid

Following the canonical treatment of Gibson and Ashby (1997), trabecular (cancellous) bone is mechanically modeled as an open-cell cellular solid.

The normalized effective elastic modulus is approximated by:

```text
Eeff / Esolid = C × (rhoeff / rhosolid)^n
```

where:

* **Eeff** = apparent elastic modulus of the trabecular structure.
* **Esolid** = elastic modulus of the solid bone matrix.
* **rhoeff** = apparent density of the trabecular network.
* **rhosolid** = density of solid bone tissue.
* **C** = geometric constant.
* **n** = topology-dependent exponent.

Typical values are:

* **n ≈ 2** for bending-dominated open-cell structures.
* **n ≈ 1** for stretch-dominated structures.

### Critical Limitation

The Gibson–Ashby scaling law assumes a mechanically connected network.

As trabeculae become disconnected, mechanical competence can collapse abruptly even when density remains relatively high. Density alone therefore becomes a poor predictor of structural integrity near failure.

This limitation motivates the connectivity-based approach developed in RA-Trabecular.

---

## References

See the concept paper, README.md, and associated Zenodo release for the complete bibliography.
