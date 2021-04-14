from visualiser import Node, Edge, Graph


class TestGraph:
    def test_normal_graph_flow(self):
        graph = Graph('hello')

        # Create Node
        A = Node('A', color='red')
        B = Node('B', color='green')
        C = Node('C', color='yellow')

        # Add node
        graph.add_node(A)
        graph.add_node(B)
        graph.add_node(C)

        # Make edge
        edge1 = Edge(A, B)
        edge2 = Edge(A, C)

        # Add node and graph to edge
        graph.add_edge(edge1)
        graph.add_edge(edge2)

        assert graph.to_string() == 'digraph G {\nA [label="A", color="red"];\nB [label="B", color="green"];\nC [label="C", color="yellow"];\nA -> B  [];\nA -> C  [];\n}'

    def test_node_methods(self):
        pass

    def test_edge_methods(self):
        pass

    def test_mutations(self):
        pass
