# Version of the recursion-visualiser
__version__ = "1.0.1"

# Maintain this order to avoid circular import
# because we are using Node inside Edge for type annotations.
from .node import Node
from .edge import Edge
from .graph import Graph
from visualiser import *
