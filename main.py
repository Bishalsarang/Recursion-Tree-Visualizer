import inspect

import sys
from functools import wraps
from collections import OrderedDict
import pydot


graph = pydot.Dot(graph_type="digraph")
node_count = 0

class TraceCalls(object):
    def __init__(self, stream=sys.stdout, indent_step=2, show_ret=False):
        self.stream = stream
        self.indent_step = indent_step
        self.show_ret = show_ret



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

            caller_func_args = sys._getframe(1).f_locals
            caller_func_args = OrderedDict(sorted(caller_func_args.items()))

            caller_func_args = ', '.join(
                [f"{key}={value}" for key, value in caller_func_args.items() if key in caller_func_arg_names])
            caller_func_signature = f"{caller_func_name}({caller_func_args})"


            # # Child Node
            child_label = current_func_signature
            child_name = current_func_signature
            v = pydot.Node(name=child_name, label=child_label)
            graph.add_node(v)

            # Parent Node
            u = None

            if caller_func_name == '<module>':
                print("Start Call")
                print(f"Drawing for {current_func_signature}")
            else:
                print(f"Called {current_func_signature} by {caller_func_signature}")
                u = pydot.Node(name=caller_func_signature, label=caller_func_signature)
                graph.add_node(u)
                edge = pydot.Edge(u, v)
                graph.add_edge(edge)

            result = fn(*args, **kwargs)
            return result

        return wrapper

@TraceCalls()
def fib(n, node_num):
    global node_count
    if n <= 1:
        return n
    node_count += 1
    left = fib(n=n - 1, node_num=node_count)
    node_count += 1
    right = fib(n=n - 2, node_num=node_count)
    return  left +right

@TraceCalls()
def fact(n, node_num):
    global node_count
    if n == 1:
        return 1

    node_count += 1
    return n * fact(n=n - 1, node_num=node_count)

print(fib(n=4, node_num=0))
graph.write_png('hawa.png')