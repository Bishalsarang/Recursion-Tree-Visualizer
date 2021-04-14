import copy

from visualiser import Node, Edge


class Graph:
    def __init__(self, name='', **attrs):
        self._name = name
        self._attrs = attrs

        self._nodes = []
        self._edges = []

    def get_node(self, name):
        filtered_nodes = list(filter(lambda node: node.name == name, self._nodes))

        return filtered_nodes[0] if len(filtered_nodes) else None

    def remove_node(self, _node):
        if isinstance(_node, Node):
            self._nodes = list(filter(lambda node: node.name != _node.name, self._nodes))
            return

        self._nodes = list(filter(lambda node: node.name != _node, self._nodes))

    def add_node(self, node):
        if self.get_node(node.name) is not None:
            self.remove_node(node)

        self._nodes.append(copy.deepcopy(node))

    def set_node_attributes(self, node, **attrs):
        for key, value in attrs.items():
            self.set_node_attribute(node, key, value)

    def set_node_attribute(self, _node, key, value):
        def _set_attribute(name):
            node = self.get_node(name)
            if node:
                node.set_attribute(key, value)

        if isinstance(_node, Node):
            _set_attribute(_node.name)
            return

        _set_attribute(_node)

    def remove_node_attribute(self, _node, key):
        def _remove_attribute(name):
            node = self.get_node(name)
            if node:
                node.remove_attribute(key)

        if isinstance(_node, Node):
            _remove_attribute(_node.name)
            return

        _remove_attribute(_node)

    def add_edge(self, edge):
        if self.get_edge(edge.name) is not None:
            self.remove_edge(edge)

        # TODO: Check if node used in node exist in graph. If not create one
        self._edges.append(copy.deepcopy(edge))

    def get_edge(self, name):
        filtered_edges =  list(filter(lambda edge: edge.name == name, self._edges))

        return filtered_edges[0] if len(filtered_edges) else None

    def remove_edge(self, _edge):
        if isinstance(_edge, Edge):
            self._edges = list(filter(lambda edge: edge.name != _edge.name, self._edges))
            return

        self._edges = list(filter(lambda edge: edge.name != _edge, self._edges))

    def set_edge_label(self, name, value):
        edge = self.get_edge(name)
        if edge:
            edge.label = value

    def highlight_node(self, name, color):
        self.set_node_attribute(name, 'color', color)

    def highlight_edge(self, name, color):
        edge = self.get_edge(name)
        if edge:
            edge.set_attribute('color', color)

    def reverse_edge_orientation(self, name):
        pass

    def get_nodes_string(self):
        return "\n".join(list(map(lambda node: node.to_string(), self._nodes)))

    def get_edges_string(self):
        return "\n".join(list(map(lambda edge: edge.to_string(), self._edges)))

    def to_string(self):
        return "digraph G {\n" + f"{self.get_nodes_string()}\n" + f"{self.get_edges_string()}\n" + "}"
