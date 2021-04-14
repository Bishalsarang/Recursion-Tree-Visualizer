
class Node:
    def __init__(self, name, label='', **attrs):
        # TODO: Add support for initialization of attributes from attribute dict
        self._name =  name
        self._attrs = attrs

        if len(label) == 0:
            self._label = name
        else:
            self._label = label

    def __repr__(self):
        return f"Node('{self.name}')"

    def __eq__(self, other):
        return self.to_string() == other.to_string()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name):
        self._name = _name

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, _label):
        self._label = _label

    def get_attribute(self, key):
        return self._attrs.get(key)

    def set_attribute(self, key, value):
        self._attrs[key] = value

    def remove_attribute(self, key):
        del self._attrs[key]

    def get_attributes_string(self):
        return '[' + f'label="{self._label}", ' + ', '.join(
            [f'{key}="{value}"' for key, value in self._attrs.items()]) + '];'

    def to_string(self):
        return f'{self.name} {self.get_attributes_string()}'
