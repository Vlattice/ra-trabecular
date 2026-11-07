"""
Graph-theoretic connectivity metrics for trabecular networks.

Provides functions to identify the largest connected component (LCC) of the
load-bearing subnetwork and to compute the connectivity ratio used in the
IRCE definition.
"""

from __future__ import annotations
import networkx as nx

from .voronoi import TrabecularNetwork


def largest_connected_component(network: TrabecularNetwork) -> nx.Graph:
    """
    Return the largest connected component of the network as a subgraph.

    Parameters
    ----------
    network : TrabecularNetwork
        Trabecular network.

    Returns
    -------
    networkx.Graph
        Subgraph containing only the LCC (empty graph if input is empty).
    """
    G = network.graph
    if G.number_of_edges() == 0:
        return G.__class__()
    # Use the subgraph of nodes with degree >= 1, then find components
    active = G.subgraph([n for n, d in G.degree() if d >= 1]).copy()
    if active.number_of_edges() == 0:
        return active.__class__()
    components = list(nx.connected_components(active))
    largest = max(components, key=len)
    return active.subgraph(largest).copy()


def connectivity_ratio(
    network: TrabecularNetwork, initial_n_edges: int
) -> float:
    """
    Compute N_LCC / N_total, the topological connectivity ratio used in IRCE.

    Parameters
    ----------
    network : TrabecularNetwork
        Current (possibly eroded) network.
    initial_n_edges : int
        Number of edges in the pristine reference network.

    Returns
    -------
    float
        Ratio in [0, 1] of edges contained in the LCC to the initial edge count.
    """
    if initial_n_edges == 0:
        return 0.0
    lcc = largest_connected_component(network)
    n_lcc_edges = lcc.number_of_edges()
    return n_lcc_edges / initial_n_edges


def percolation_order_parameter(
    network: TrabecularNetwork, total_active_nodes: int
) -> float:
    """
    Fraction of nodes in the largest connected component, the classical
    percolation order parameter P_infinity.

    Parameters
    ----------
    network : TrabecularNetwork
        Current network.
    total_active_nodes : int
        Total number of nodes in the pristine network.

    Returns
    -------
    float
        P_infinity in [0, 1].
    """
    if total_active_nodes == 0:
        return 0.0
    lcc = largest_connected_component(network)
    return lcc.number_of_nodes() / total_active_nodes
