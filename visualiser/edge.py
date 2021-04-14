import copy


from visualiser import  Node
class Edge:

    def __init__(self, source_node: Node, destination_node: Node, label: str = '',
                 **attrs: str) -> None:
        # TODO: Remove copy after finding a better way to do this.
        self._source_node = copy.deepcopy(source_node)
        self._destination_node = copy.deepcopy(destination_node)

        self._label = label
        self._attrs = attrs

    @property
    def label(self) -> str:
        """
        Get label for edge.
        :return: str
        """
        return self._label

    @label.setter
    def label(self, _label: str) -> None:
        """
        Set label for edge.
        :param _label: str
        """
        self._label = _label

    @property
    def source_node(self) -> Node:
        """
        Get source node
        :return: Node
        """
        return self._source_node

    @source_node.setter
    def source_node(self, _source_node: Node) -> None:
        """
        Set source node.
        :param _source_node: Node
        """
        self._source_node = _source_node

    @property
    def destination_node(self) -> Node:
        """
        Get destination node.
        :return: Node
        """
        return self._destination_node

    @destination_node.setter
    def destination_node(self, _destination_node: Node) -> None:
        """
        Sets destination node.
        :param _destination_node: Node
        """
        self._destination_node = _destination_node

    def get_attribute(self, key: str) -> str:
        """
        Get attribute for edge.
        :param key: str
        :return: The value of attribute with key
        """
        return self._attrs.get(key)

    def set_attribute(self, key: str, value: str) -> None:
        """
        Set attribute for edge
        :param key: str
        :param value: str
        """
        self._attrs[key] = value

    def remove_attribute(self, key: str) -> None:
        """
        Remove attribute from edge.
        :param key: str
        """
        del self._attrs[key]

    def get_attributes_string(self) -> str:
        """
        Get attributes string enclosed in []
        :return:
        """
        if len(self._label) == 0:
            return '[' + ', '.join([f'{key}="{value}"' for key, value in self._attrs.items()]) + ']'

        return '[' + f'label="{self._label}", ' + ', '.join(
            [f'{key}="{value}"' for key, value in self._attrs.items()]) + ']'

    def to_string(self) -> str:
        """
        Converts dot string equivalent of the current edge.
        :return: Str
        """
        return f'{self._source_node.name} -> {self._destination_node.name}  {self.get_attributes_string()}'
