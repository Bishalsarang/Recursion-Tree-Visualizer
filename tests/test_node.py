from visualiser import *

"""
    Test case class for nodes 
"""


class TestNode:
    def test_create_new_node(self):
        node = Node('bishal', 'Bishal label', color='red', style='filled')

        assert node.label == 'Bishal label'
        assert node.name == 'bishal'
        assert node.get_attribute('color') == 'red'
        assert node.get_attribute('style') == 'filled'
        assert node.to_string() == 'bishal [label="Bishal label", color="red", style="filled"];'

    def test_set_attributes(self):
        node = Node('bishal', 'Bishal label', color='red', style='filled')
        assert node.get_attribute('color') == 'red'
        node.set_attribute('color', 'green')
        assert node.get_attribute('color') == 'green'
        node.set_attribute('background', 'grey')
        assert node.get_attribute('background') == 'grey'
        assert node.to_string() == 'bishal [label="Bishal label", color="green", style="filled", background="grey"];'

    def test_rename_name_label(self):
        node = Node('bishal', 'Bishal label', color='red', style='filled')

        node.set_attribute('color', 'green')

        assert node.label == 'Bishal label'
        node.label = 'Bishal renamed label'
        assert node.label == 'Bishal renamed label'

        assert node.name == 'bishal'
        node.name = 'Bishal renamed'
        assert node.name == 'Bishal renamed'

        assert node.to_string() == 'Bishal renamed [label="Bishal renamed label", color="green", style="filled"];'
