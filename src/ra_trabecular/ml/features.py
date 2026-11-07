"""
Reference-free structural features of a trabecular network.

Every feature here is computed from a *single snapshot* of the network,
without access to the healthy reference. This mirrors the clinical setting:
an HR-pQCT or micro-CT scan of a patient shows the current architecture,
not the architecture the patient had before the disease.

Features are grouped so that models restricted to one group can be compared:

``DENSITY_FEATURES``
    Mass-based descriptors analogous to standard morphometry
    (BV/TV, mean trabecular thickness, strut length density).

``TOPOLOGY_FEATURES``
    Connectivity descriptors from graph and percolation theory
    (connectivity density, mean degree, dangling-end and bridge fractions,
    cluster statistics, mean finite-cluster size, Molloy–Reed ratio).

``ANISOTROPY_FEATURES``
    Shape of the fabric tensor (normalized eigenvalues and A_local).
"""

from __future__ import annotations
from typing import Dict
import numpy as np
import networkx as nx

from ..voronoi import TrabecularNetwork
from ..anisotropy import fabric_tensor


DENSITY_FEATURES = [
    "bv_tv",
    "mean_thickness",
    "strut_length_density",
]

TOPOLOGY_FEATURES = [
    "conn_density",
    "mean_degree",
    "frac_dangling",
    "frac_bridges_lcc",
    "lcc_edge_fraction",
    "n_clusters_density",
    "mean_finite_cluster_size",
    "lcc_cycle_rank_per_edge",
    "molloy_reed",
]

ANISOTROPY_FEATURES = [
    "fabric_l1",
    "fabric_l3",
    "a_local",
]

ALL_FEATURES = DENSITY_FEATURES + TOPOLOGY_FEATURES + ANISOTROPY_FEATURES


def _edge_lengths(network: TrabecularNetwork) -> np.ndarray:
    if network.n_edges == 0:
        return np.zeros(0)
    e = np.array(network.edges)
    return np.linalg.norm(network.nodes[e[:, 1]] - network.nodes[e[:, 0]], axis=1)


def structural_features(network: TrabecularNetwork) -> Dict[str, float]:
    """
    Compute reference-free structural features of ``network``.

    Parameters
    ----------
    network : TrabecularNetwork
        A (possibly eroded) network snapshot.

    Returns
    -------
    dict
        Feature name -> value, with keys :data:`ALL_FEATURES`.
    """
    volume = network.domain_volume
    lengths = _edge_lengths(network)
    radii = network.edge_thickness / 2.0 if network.n_edges else np.zeros(0)

    # --- density ---------------------------------------------------------
    bv_tv = float(np.sum(np.pi * radii ** 2 * lengths) / volume)
    mean_thickness = float(np.mean(network.edge_thickness)) if network.n_edges else 0.0
    strut_length_density = float(np.sum(lengths) / volume)

    # --- topology --------------------------------------------------------
    G = network.graph.subgraph([n for n, d in network.graph.degree() if d >= 1])
    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()

    if n_edges == 0:
        topo = dict.fromkeys(TOPOLOGY_FEATURES, 0.0)
    else:
        components = list(nx.connected_components(G))
        sizes = np.array([len(c) for c in components], dtype=float)
        n_comp = len(components)
        lcc_nodes = components[int(np.argmax(sizes))]
        lcc = G.subgraph(lcc_nodes)
        lcc_e = lcc.number_of_edges()

        degrees = np.array([d for _, d in G.degree()], dtype=float)
        n_bridges = sum(1 for _ in nx.bridges(lcc)) if lcc_e else 0

        # Mean finite-cluster size (percolation "susceptibility"): second
        # moment of the cluster-size distribution excluding the LCC. It
        # peaks near the percolation threshold.
        finite = np.delete(sizes, int(np.argmax(sizes)))
        mfcs = float(np.sum(finite ** 2) / np.sum(finite)) if finite.size else 0.0

        topo = {
            # Cycle rank (Euler number analogue): independent loops per volume,
            # the graph counterpart of morphometric connectivity density Conn.D
            "conn_density": (n_edges - n_nodes + n_comp) / volume,
            "mean_degree": float(degrees.mean()),
            "frac_dangling": float(np.mean(degrees == 1)),
            "frac_bridges_lcc": n_bridges / lcc_e if lcc_e else 0.0,
            "lcc_edge_fraction": lcc_e / n_edges,
            "n_clusters_density": n_comp / volume,
            "mean_finite_cluster_size": mfcs,
            "lcc_cycle_rank_per_edge": (lcc_e - lcc.number_of_nodes() + 1) / lcc_e
            if lcc_e else 0.0,
            # Molloy–Reed ratio <k^2>/<k>: a random graph with this degree
            # distribution has a giant component iff the ratio exceeds 2.
            "molloy_reed": float(np.mean(degrees ** 2) / np.mean(degrees)),
        }

    # --- anisotropy ------------------------------------------------------
    F = fabric_tensor(network, normalize=True)
    eig = np.sort(np.linalg.eigvalsh(F))[::-1]
    l1, l3 = float(eig[0]), float(eig[-1])
    aniso = {
        "fabric_l1": l1,
        "fabric_l3": l3,
        "a_local": (l1 - l3) / (l1 + l3) if (l1 + l3) > 0 else 0.0,
    }

    feats = {
        "bv_tv": bv_tv,
        "mean_thickness": mean_thickness,
        "strut_length_density": strut_length_density,
        **{k: float(v) for k, v in topo.items()},
        **aniso,
    }
    return {k: feats[k] for k in ALL_FEATURES}
