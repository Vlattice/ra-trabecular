"""
Voronoi tessellation module for trabecular bone network generation.

Generates 3D Voronoi tessellations from seed point distributions and extracts
the edge network as a statistically faithful generative model of trabecular
bone microarchitecture.

References
----------
Gibson, L. J., & Ashby, M. F. (1997). Cellular Solids: Structure and Properties.
Roberts, A. P., & Garboczi, E. J. (2002). J. Mech. Phys. Solids, 50(1), 33-55.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import numpy as np
from scipy.spatial import Voronoi
import networkx as nx


@dataclass
class TrabecularNetwork:
    """
    Represents a trabecular bone network as a graph extracted from a
    3D Voronoi tessellation.

    Attributes
    ----------
    nodes : np.ndarray, shape (N, 3)
        3D coordinates of network nodes (Voronoi vertices).
    edges : list of tuple
        List of (i, j) tuples representing edges between nodes.
    graph : networkx.Graph
        NetworkX graph object for topological computations.
    edge_thickness : np.ndarray, shape (M,)
        Per-edge thickness (trabecular strut diameter).
    edge_modulus : np.ndarray, shape (M,)
        Per-edge elastic modulus (mineralized matrix modulus).
    domain_size : float
        Edge length of the cubic generation domain.
    metadata : dict
        Additional metadata (seed, generation parameters).
    """
    nodes: np.ndarray
    edges: list
    graph: nx.Graph
    edge_thickness: np.ndarray
    edge_modulus: np.ndarray
    domain_size: float
    metadata: dict = field(default_factory=dict)

    @property
    def n_nodes(self) -> int:
        return len(self.nodes)

    @property
    def n_edges(self) -> int:
        return len(self.edges)

    @property
    def mean_coordination(self) -> float:
        """Average node coordination number z."""
        degrees = [d for _, d in self.graph.degree()]
        return float(np.mean(degrees)) if degrees else 0.0


def generate_voronoi_network(
    n_seeds: int = 200,
    domain_size: float = 10.0,
    seed_distribution: str = "uniform",
    anisotropy_factor: float = 1.0,
    mean_thickness: float = 0.15,
    thickness_std: float = 0.03,
    matrix_modulus: float = 20e3,
    rng_seed: Optional[int] = None,
) -> TrabecularNetwork:
    """
    Generate a 3D Voronoi-based trabecular network.

    Parameters
    ----------
    n_seeds : int
        Number of Voronoi seed points.
    domain_size : float
        Edge length of the cubic generation domain (arbitrary units, e.g. mm).
    seed_distribution : {"uniform", "perturbed_lattice"}
        How to distribute seed points.
    anisotropy_factor : float
        Stretch factor applied to the z-axis (>1 elongates along z).
        Used to model trabecular alignment with principal stress trajectories.
    mean_thickness : float
        Mean trabecular thickness (same units as domain_size).
    thickness_std : float
        Standard deviation of trabecular thickness distribution.
    matrix_modulus : float
        Elastic modulus of the bone matrix (MPa).
    rng_seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    TrabecularNetwork
        The generated network.
    """
    rng = np.random.default_rng(rng_seed)

    # Generate seed points
    if seed_distribution == "uniform":
        seeds = rng.uniform(0, domain_size, size=(n_seeds, 3))
    elif seed_distribution == "perturbed_lattice":
        n_per_axis = int(np.ceil(n_seeds ** (1 / 3)))
        lattice = np.linspace(0, domain_size, n_per_axis + 2)[1:-1]
        xx, yy, zz = np.meshgrid(lattice, lattice, lattice)
        seeds = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])
        perturbation = rng.normal(0, domain_size / (4 * n_per_axis), size=seeds.shape)
        seeds = seeds + perturbation
        seeds = seeds[:n_seeds]
    else:
        raise ValueError(f"Unknown seed_distribution: {seed_distribution}")

    # Apply anisotropy along z
    if anisotropy_factor != 1.0:
        seeds[:, 2] *= anisotropy_factor

    # Compute Voronoi tessellation
    vor = Voronoi(seeds)

    # Extract finite vertices and ridges
    vertices = vor.vertices
    ridges = vor.ridge_vertices

    # Build edge set, filtering infinite vertices and out-of-domain nodes
    edges = set()
    bounds_min = -0.1 * domain_size
    bounds_max = 1.1 * domain_size * max(1.0, anisotropy_factor)

    valid_node_mask = np.all(
        (vertices >= bounds_min) & (vertices <= bounds_max), axis=1
    )

    for ridge in ridges:
        if -1 in ridge:
            continue
        for i in range(len(ridge)):
            a, b = ridge[i], ridge[(i + 1) % len(ridge)]
            if valid_node_mask[a] and valid_node_mask[b]:
                edges.add(tuple(sorted([a, b])))

    edges = list(edges)

    # Build graph
    G = nx.Graph()
    G.add_nodes_from(range(len(vertices)))
    G.add_edges_from(edges)

    # Remove isolated nodes (not part of any retained edge)
    isolated = [n for n, d in G.degree() if d == 0]
    G.remove_nodes_from(isolated)

    # Assign per-edge properties
    n_edges = len(edges)
    edge_thickness = rng.normal(mean_thickness, thickness_std, size=n_edges)
    edge_thickness = np.clip(edge_thickness, 0.05 * mean_thickness, None)
    edge_modulus = np.full(n_edges, matrix_modulus, dtype=float)

    return TrabecularNetwork(
        nodes=vertices,
        edges=edges,
        graph=G,
        edge_thickness=edge_thickness,
        edge_modulus=edge_modulus,
        domain_size=domain_size,
        metadata={
            "n_seeds": n_seeds,
            "seed_distribution": seed_distribution,
            "anisotropy_factor": anisotropy_factor,
            "rng_seed": rng_seed,
        },
    )
