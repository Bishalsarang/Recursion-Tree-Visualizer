import copy
from typing import Union

from visualiser import Node


class Edge:

    def __init__(self, source_node: Union[Node, str], destination_node: Union[Node, str], label: str = '',
                 **attrs: str) -> None:
        self._source_node = Node(source_node) if isinstance(source_node, str) else copy.deepcopy(source_node)
        self._destination_node = Node(destination_node) if isinstance(destination_node, str) else copy.deepcopy(
            destination_node)

        self._name = f"{self._source_node.name} -> {self._destination_node.name}"
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
    def name(self) -> str:
        """
        Get name for edge.
        :return: str
        """
        return self._name

    @name.setter
    def name(self, _name: str) -> None:
        """
        Set label for edge.
        :param _name: str
        """
        self._name = _name

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
        if self._attrs.get(key):
            del self._attrs[key]

    def get_attributes_string(self) -> str:
        """
        Get attributes string enclosed in []
        :return:
        """
        if len(self._label) == 0:
            return '[' + ', '.join([f'{key}="{value}"' for key, value in self._attrs.items()]) + '];'

        return '[' + f'label="{self._label}", ' + ', '.join(
            [f'{key}="{value}"' for key, value in self._attrs.items()]) + '];'

    def to_string(self) -> str:
        """
        Converts dot string equivalent of the current edge.
        :return: Str
        """
        return f'{self._source_node.name} -> {self._destination_node.name}  {self.get_attributes_string()}'
