from visualiser import Edge, Node

"""
    Test case class for nodes 
"""


class TestEdge:
    def test_create_new_edge(self):
        # Create Node
        A = Node('A', color='red', style='filled')
        B = Node('B', label='B label', color='red', style='filled')

        # Create Edge
        edge = Edge(A, B, label='Test Label')

        assert edge.label == 'Test Label'
        assert edge.source_node.label == 'A'
        assert edge.source_node == A
