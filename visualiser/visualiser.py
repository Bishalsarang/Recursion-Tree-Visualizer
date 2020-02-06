# Author: Bishal Sarang

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
    def write_image(cls, filename="out.png"):
        try:
            cls.graph.write_png(f"{filename}")
            print(f"File {filename} successfully written")
        except Exception:
            print(f"Writing {filename} failed")

    def extract_signature_label_arg_string(self, *args, **kwargs):
        """
        Returns function signature arguments as string and function label arguments as string.
            label_argument string contains only the arguments that are not in ignore_args
            signature_argument_string contains all the arguments available for the function
        """
        # If show_argument flag is True(default)
        # Then argument_string is:
        # a=1, b=31, c=0
        signature_argument_string = ', '.join([repr(a) for a in args] +
                                    [f"{key}={repr(value)}" for key, value in kwargs.items()])

        label_argument_string = ', '.join([repr(a) for a in args] +
                                                           [f"{key}={repr(value)}"
                                                            for key, value in kwargs.items()
                                                            if key not in self.ignore_args])

        # If show_argument flag is False
        # Then argument_string is:
        # 1, 31, 0
        if not self.show_argument_name:
            signature_argument_string = ', '.join([repr(value) for value in args] +
                                                 [f"{repr(value)}" for key, value in kwargs.items()])

            label_argument_string = ', '.join([repr(a) for a in args] +
                                              [f"{repr(value)}"
                                               for key, value in kwargs.items()
                                               if key not in self.ignore_args])

        return signature_argument_string, label_argument_string

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Order all the keyword arguments
            kwargs = OrderedDict(sorted(kwargs.items()))

            """Details about current Function"""
            # Get signature and label arguments strings for current function
            current_function_argument_string, current_function_label_argument_string = self.extract_signature_label_arg_string(*args, **kwargs)

            # Details about current function
            current_function_name = fn.__name__

            # Current function signature looks as follows:
            # foo(1, 31, 0) or foo(a=1, b=31, c=0)
            current_function_signature = f"{current_function_name}(" \
                                         f"{current_function_argument_string})"
            current_function_label = f"{current_function_name}({current_function_label_argument_string})"
            """"""

            """Details about caller function"""
            caller_function_frame = sys._getframe(1)
            # All the argument names in caller/parent function
            caller_function_argument_names = caller_function_frame.f_code.co_varnames[
                                             :fn.__code__.co_argcount]
            caller_function_locals = caller_function_frame.f_locals
            # Sort all the locals of caller function
            caller_function_locals = OrderedDict(sorted(caller_function_locals.items()))
            # Extract only those locals that are in arguments
            caller_function_kwargs = {key: value for key, value in caller_function_locals.items() if key in caller_function_argument_names}

            caller_function_argument_string, caller_function_label_argument_string = self.extract_signature_label_arg_string(**caller_function_kwargs)

            # Caller Function
            caller_function_name = caller_function_frame.f_code.co_name

            # Extract the names of arguments only
            caller_func_signature = f"{caller_function_name}({caller_function_argument_string})"
            caller_func_label = f"{caller_function_name}({caller_function_label_argument_string})"
            """"""

            if caller_function_name == '<module>':
                print(f"Drawing for {current_function_signature}")

            result = fn(*args, **kwargs)

            # If show_return_value flag is set, display the result
            if self.show_return_value:
                current_function_label += f" => {result}"

            child_node = pydot.Node(name=current_function_signature, label=current_function_label)
            self.graph.add_node(child_node)

            # If the function is called by another function
            if caller_function_name not in ['<module>', 'main']:
                print(f"Called {current_function_label} by {caller_func_label}")

                parent_node = pydot.Node(name=caller_func_signature, label=caller_func_label)
                self.graph.add_node(parent_node)
                edge = pydot.Edge(parent_node, child_node)
                self.graph.add_edge(edge)
            return result
        return wrapper

@Visualiser(ignore_args=["node_num"])
def fib(n, node_num):
    if n <= 1:
        return n
    Visualiser.node_count += 1
    left = fib(n=n - 1, node_num=Visualiser.node_count)

    Visualiser.node_count += 1
    right = fib(n=n - 2, node_num=Visualiser.node_count)
    return left + right

def main():
    # Call function
    print(fib(n=6, node_num=0))

    # Save recursion tree to a file
    Visualiser.write_image("fibonacci.png")


if __name__ == "__main__":
    main()