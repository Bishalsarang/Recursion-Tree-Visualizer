import sys
from functools import wraps
from collections import OrderedDict
import pydot

from visualiser import Node, Edge, Graph, Animation


class VisualiserR:
    _graph = Graph('recursion')
    _animation = Animation()
    def __init__(self, ignore_args=None, show_argument_name=True,
                 show_return_value=True, node_properties_kwargs={}):
        self._node_count = 0
        self._stack = []



        # If enabled shows keyword arguments ordered by keys
        self.show_argument_name = show_argument_name
        # If enables shows the return value at every nodes
        self.show_return_value = show_return_value

        self.node_properties_kwargs = node_properties_kwargs

        # Argument string that are to be ignored in diagram
        self.ignore_args = ['node_num'] if ignore_args is None else ['node_num'] + ignore_args

    @classmethod
    def make_animation(cls, filename="out.gif", delay=3):
        # TODO call make animation from animation object
        print(cls._graph.to_string())
        cls._animation.write_gif('test.gif', 2)
        pass

    def extract_arg_strings(self, *args, **kwargs):
        """
        Returns function signature arguments function label arguments as
        Returns function signature arguments function label arguments as
        string.
        label_args_string contains only the arguments that are not in
        ignore_args.
        signature_args_string contains all the arguments available for the
        function.
        """

        def get_kwargs_strings(ignore_args=[]):
            """Returns list of kwargs in string format from given kwargs items

            Args:
                ignore_args (list, optional) : list of ignored arguments.
                Default to [].

            Returns:
                strings_list: list of kwargs in string format
            """

            strings_list = []

            for key, value in kwargs.items():
                if key not in ignore_args:
                    if not self.show_argument_name:
                        strings_list.append(f"{repr(value)}")
                    else:
                        strings_list.append(f"{key}={repr(value)}")

            return strings_list

        args_string = [repr(a) for a in args]
        signature_kwargs_string = [f"{repr(kwargs.get('node_num'))}"]
        label_kwargs_string = get_kwargs_strings(ignore_args=self.ignore_args)

        signature_args_string = ', '.join(signature_kwargs_string)
        label_args_string = ', '.join(args_string + label_kwargs_string)

        return signature_args_string, label_args_string

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Increment total number of nodes when a call is made
            self._node_count += 1

            # Update kwargs by adding dummy keyword node_num which helps to
            # uniquely identify each node
            kwargs.update({'node_num': self._node_count})
            # Order all the keyword arguments
            kwargs = OrderedDict(sorted(kwargs.items()))

            """Details about current Function"""
            # Get signature and label arguments strings for current function
            (signature_args_string,
             label_args_string) = self.extract_arg_strings(
                *args, **kwargs)

            # Details about current function
            function_name = fn.__name__

            # Current function signature looks as follows:
            # foo(1, 31, 0) or foo(a=1, b=31, c=0)
            function_signature = f"{function_name}({signature_args_string})"
            function_label = f"{function_name}({label_args_string})"
            """"""

            """Details about caller function"""
            caller_func_frame = sys._getframe(1)
            # All the argument names in caller/parent function
            caller_func_arg_names = caller_func_frame.f_code.co_varnames[
                                    : fn.__code__.co_argcount]
            caller_func_locals = caller_func_frame.f_locals
            # Sort all the locals of caller function
            caller_func_locals = OrderedDict(
                sorted(caller_func_locals.items()))

            caller_func_kwargs = dict()

            # Extract only those locals that are in arguments
            for key, value in caller_func_locals.items():
                if key in caller_func_arg_names:
                    caller_func_kwargs[key] = value

            # If the nodes has parent node get node_num from parent node
            if self._stack:
                caller_func_kwargs.update({'node_num': self._stack[-1]})

            caller_func_kwargs = OrderedDict(
                sorted(caller_func_kwargs.items()))

            (caller_func_args_string,
             caller_func_label_args_string) = self.extract_arg_strings(
                **caller_func_kwargs)

            # Caller Function
            caller_func_name = caller_func_frame.f_code.co_name

            # Extract the names of arguments only
            caller_func_signature = "{}({})".format(
                caller_func_name, caller_func_args_string)
            caller_func_label = "{}({})".format(
                caller_func_name, caller_func_label_args_string)
            """"""


            # print(f"Drawing for {function_label}")

            # Push node_count to stack
            self._stack.append(self._node_count)
            # Before actual function call delete keyword 'node_num' from kwargs
            del kwargs['node_num']

            # Construct node string to be rendered in graphviz
            node_string = f'"{function_signature}" [label="{function_label}"'

            if self.node_properties_kwargs:
                node_string += ", " + \
                               ", ".join([f'{key}="{value}"' for key,
                                                                 value in self.node_properties_kwargs.items()])

            # Return after function call
            result = fn(*args, **kwargs)

            # Pop from tha stack after returning
            self._stack.pop()

            # If show_return_value flag is set, display the result
            if self.show_return_value:
                # If shape is set to record
                # Then separate function label and return value by a row
                if "record" in self.node_properties_kwargs.values():
                    function_label = "{" + \
                                     function_label + f"|{result} }}"
                else:
                    function_label += f"\n => {result}"
            # print('Return', function_label)
            # TODO: Return garda make animation step to hihjlight and label age from this node to its parent
            child_node = Node(name=function_signature, label=function_label, **self.node_properties_kwargs)

            self._graph.add_node(child_node)

            # If the function is called by another function
            if caller_func_name not in ['<module>', 'main']:
                parent_node = Node(name=caller_func_signature, label=caller_func_label, **self.node_properties_kwargs)


                self._graph.add_node(parent_node)
                edge = Edge(parent_node, child_node)
                self._graph.add_edge(edge)
                # print(self._graph.to_string())
                self._animation.next_step(self._graph.to_string())


            return result

        return wrapper
