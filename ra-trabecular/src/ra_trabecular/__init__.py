"""
RA-Trabecular: A percolation-based framework for modeling trabecular bone
degradation in rheumatoid arthritis using Voronoi tessellation and the
Index of Effective Mechanical Connectivity (IRCE).

Author: Verónica Zumpano Blumenfeld
ORCID:  0009-0006-2030-1849
License: Apache-2.0
"""

__version__ = "0.1.0"
__author__ = "Verónica Zumpano Blumenfeld"
__orcid__ = "0009-0006-2030-1849"
__license__ = "Apache-2.0"

from .voronoi import generate_voronoi_network, TrabecularNetwork
from .erosion import progressive_erosion, ErosionRegime
from .connectivity import largest_connected_component, connectivity_ratio
from .anisotropy import compute_local_anisotropy
from .irce import compute_irce, compute_irce_multiplicative, IRCEResult

__all__ = [
    "generate_voronoi_network",
    "TrabecularNetwork",
    "progressive_erosion",
    "ErosionRegime",
    "largest_connected_component",
    "connectivity_ratio",
    "compute_local_anisotropy",
    "compute_irce",
    "compute_irce_multiplicative",
    "IRCEResult",
]
