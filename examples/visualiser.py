import sys
from functools import wraps
from collections import OrderedDict
import pydot


class Visualiser(object):
    node_count = 0
    graph = pydot.Dot(graph_type="digraph")

    def __init__(self, ignore_args, show_argument_name=True, show_return_value=True):
        self.show_argument_name = show_argument_name
        self.show_return_value = show_return_value
        self.ignore_args = ignore_args

    @classmethod
    def write_image(self, filename="out.png"):
        self.graph.write_png(f"{filename}")

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Order all the keyword arguments
            kwargs = OrderedDict(sorted(kwargs.items()))

            # If show_argument flag is True(default)
            # Then argument_string is:
            # a=1, b=31, c=0
            argument_string = ', '.join(
                [repr(a) for a in args] +
                [f"{key}={repr(value)}" for key, value in kwargs.items()])

            current_function_label_argument_string = ', '.join(
                [repr(a) for a in args] +
                [f"{key}={repr(value)}" for key, value in kwargs.items() if key not in self.ignore_args])

            # If show_argument flag is False
            # Then argument_string is:
            # 1, 31, 0
            if self.show_argument_name == False:
                argument_string = ', '.join(
                    [repr(value) for value in args] +
                    [f"{repr(value)}" for key, value in kwargs.items()])

                current_function_label_argument_string = ', '.join(
                    [repr(a) for a in args] +
                    [f"{repr(value)}" for key, value in kwargs.items() if key not in self.ignore_args])

            # Details about current function
            current_function_name = fn.__name__
            current_function_argument_string = argument_string
            # Current function signature looks as follows:
            # foo(1, 31, 0) or foo(a=1, b=31, c=0)
            current_function_signature = f"{current_function_name}({current_function_argument_string})"
            current_function_label = f"{current_function_name}({current_function_label_argument_string})"

            # Caller Function
            caller_function_name = sys._getframe(1).f_code.co_name
            # Extract the names of arguments only
            caller_function_argument_names = sys._getframe(1).f_code.co_varnames[:fn.__code__.co_argcount]
            caller_function_locals = sys._getframe(1).f_locals

            # Sort all the locals of caller function
            caller_function_locals = OrderedDict(sorted(caller_function_locals.items()))


            # Extract only those locals which are in function signature
            caller_function_argument_string = ', '.join(
                [f"{key}={value}" for key, value in caller_function_locals.items() if (key in caller_function_argument_names)])
            caller_function_label_argument_string = ', '.join(
                [f"{key}={value}" for key, value in caller_function_locals.items() if
                 (key in caller_function_argument_names and key not in self.ignore_args)])

            if self.show_argument_name == False:
                caller_function_argument_string = ', '.join(
                    [f"{value}" for key, value in caller_function_locals.items() if
                     (key in caller_function_argument_names)])
                caller_function_label_argument_string = ', '.join(
                    [f"{value}" for key, value in caller_function_locals.items() if
                     (key in caller_function_argument_names and key not in self.ignore_args)])

            caller_func_signature = f"{caller_function_name}({caller_function_argument_string})"
            caller_func_label = f"{caller_function_name}({caller_function_label_argument_string})"

            if caller_function_name == '<module>':
                print(f"Drawing for {current_function_signature}")

            result = fn(*args, **kwargs)

            # #Child Node
            child_label = current_function_label
            if self.show_return_value:
                child_label += f" => {result}"
            child_name = current_function_signature
            v = pydot.Node(name=child_name, label=child_label)
            self.graph.add_node(v)

            # Parent Node
            u = None

            if caller_function_name != '<module>':
                print(f"Called {current_function_label} by {caller_func_label}")
                u = pydot.Node(name=caller_func_signature, label=caller_func_label)
                self.graph.add_node(u)
                edge = pydot.Edge(u, v)
                self.graph.add_edge(edge)

            return result
        return wrapper
