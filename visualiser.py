import inspect

import sys
from functools import wraps
from collections import OrderedDict
import pydot


class Visualiser(object):
    node_count = 0
    graph = pydot.Dot(graph_type="digraph")
    def __init__(self, ignore_args):
        self.ignore_args = ignore_args

    @classmethod
    def write_image(self, filename="out"):
        self.graph.write_png(f"{filename}.png")



    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            kwargs = OrderedDict(sorted(kwargs.items()))
            argstr = ', '.join(
                [repr(a) for a in args] +
                ["%s=%s" % (a, repr(b)) for a, b in kwargs.items()])

            # Current Function
            current_func_name = fn.__name__
            current_func_args = argstr
            current_func_signature = f"{current_func_name}({current_func_args})"

            # Caller Function
            caller_func_name = sys._getframe(1).f_code.co_name
            caller_func_arg_names = sys._getframe(1).f_code.co_varnames[:fn.__code__.co_argcount]

            caller_func_locals = sys._getframe(1).f_locals
            caller_func_locals = OrderedDict(sorted(caller_func_locals.items()))

            caller_func_args = ', '.join(
                [f"{key}={value}" for key, value in caller_func_locals.items() if (key in caller_func_arg_names)])
            caller_func_signature = f"{caller_func_name}({caller_func_args})"

            caller_func_args = ', '.join(
                [f"{key}={value}" for key, value in caller_func_locals.items() if
                 (key in caller_func_arg_names and key not in self.ignore_args)])
            caller_func_node_label = f"{caller_func_name}({caller_func_args})"

            if caller_func_name == '<module>':
                print(f"Drawing for {current_func_signature}")

            result = fn(*args, **kwargs)

            argstr = ', '.join(
                [repr(a) for a in args] +
                ["%s=%s" % (a, repr(b)) for a, b in kwargs.items() if a not in self.ignore_args])
            current_node_label = f"{current_func_name}({argstr})"

            # # Child Node
            child_label = current_node_label
            child_name = current_func_signature
            v = pydot.Node(name=child_name, label=child_label)
            self.graph.add_node(v)

            # Parent Node
            u = None

            if caller_func_name != '<module>':
                print(f"Called {current_func_signature} by {caller_func_signature}")
                u = pydot.Node(name=caller_func_signature, label=caller_func_node_label)
                self.graph.add_node(u)
                edge = pydot.Edge(u, v)
                self.graph.add_edge(edge)

            return result
        return wrapper




@Visualiser(ignore_args=['node_num'])
def fact(n, node_num):
    if n == 1:
        Visualiser.node_count += 1
        return 1

    Visualiser.node_count += 1
    return n * fact(n=n - 1, node_num=Visualiser.node_count)

