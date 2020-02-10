# Author: Bishal Sarang
import sys
from functools import wraps
from collections import OrderedDict
import pydot
import imageio
import glob
import os
import shutil

# Dot Language for graph
dot_str_start = "digraph G {\n"
dot_str_body = ""
dot_str_end = "}"

class Visualiser(object):
    # Total number of nodes
    node_count = 0
    graph = pydot.Dot(graph_type="digraph", bgcolor="#fff3af")
    # To track function call numbers
    stack = []
    edges = []
    nodes = []

    def __init__(self, ignore_args=None, show_argument_name=True, show_return_value=True, node_properties_kwargs={}):
        #If enabled shows keyword arguments ordered by keys
        self.show_argument_name = show_argument_name
        # If enables shows the return value at every nodes
        self.show_return_value = show_return_value

        self.node_properties_kwargs = node_properties_kwargs

        # Argument string that are to be ignored in diagram
        if ignore_args is None:
            self.ignore_args = ['node_num']
        else:
            self.ignore_args = ['node_num'] + ignore_args



    @classmethod
    def write_image(cls, filename="out.png"):
        try:
            cls.graph.write_png(f"{filename}")
            print(f"File {filename} successfully written")
        except Exception:
            print(f"Writing {filename} failed")

    @classmethod
    def make_frames(cls):
        """
        Make frame for each steps
        """
        # If frame directory doesn't exist
        if not os.path.exists("frames"):
            os.makedirs("frames")

        Edges = cls.edges[::]
        Nodes = cls.nodes[::]
        print("Writing frames....")
        for i in range(len(Edges)):
            nodes = Nodes[::]
            edges = Edges[::]

            for j in range(0, i + 1):
                nodes[j] += '];'

            for j in range(i + 1, len(Edges)):
                nodes[j] += ' , style=invis];'
                edges[j] += ' [style=invis];'

            dot_str_body = "\n".join(nodes) + "\n"
            dot_str_body += "\n".join(edges)
            dot_str = dot_str_start + dot_str_body + dot_str_end
            g = pydot.graph_from_dot_data(dot_str)
            g[0].write_png(f"frames/temp_{i}.png")

    @classmethod
    def write_gif(cls, name="out.gif", delay=3):
        images = []
        imgs = glob.glob("frames/*.png")
        for filename in sorted(imgs, key=lambda fn: int(fn.split("_")[1].split(".")[0])):
            images.append(imageio.imread(filename))
        print("Writing gif...")
        imageio.mimsave(name, images, duration=delay)
        print(f"Saved gif {name} successfully")
        # Delete temporary directory
        shutil.rmtree("frames")

    @classmethod
    def make_animation(cls, filename="out.gif", delay=3):
        print("Starting to make animation")
        # Save final tree image as png
        try:
            cls.write_image(f"{filename.split('.')[0]}.png")
        except:
            print("Error saving image.")

        # Make animation as gif
        try:
            cls.make_frames()
        except:
            print("Error writing frames")

        try:
            cls.write_gif(filename, delay=delay)
        except:
            print("Error saving gif.")


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
            global dot_str_body
            # Increment total number of nodes when a call is made
            self.node_count += 1

            # Update kwargs by adding dummy keyword node_num which helps to uniquely identify each node
            kwargs.update({'node_num': self.node_count})
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

            # If the nodes has parent node get node_num from parent node
            if self.stack:
                caller_function_kwargs.update({'node_num': self.stack[-1]})
            caller_function_kwargs = OrderedDict(sorted(caller_function_kwargs.items()))

            caller_function_argument_string, caller_function_label_argument_string = self.extract_signature_label_arg_string(**caller_function_kwargs)

            # Caller Function
            caller_function_name = caller_function_frame.f_code.co_name

            # Extract the names of arguments only
            caller_func_signature = f"{caller_function_name}({caller_function_argument_string})"
            caller_func_label = f"{caller_function_name}({caller_function_label_argument_string})"
            """"""

            if caller_function_name == '<module>':
                print(f"Drawing for {current_function_signature}")

            # Push node_count to stack
            self.stack.append(self.node_count)
            # Before actual function call delete keyword 'node_num' from kwargs
            del kwargs['node_num']

            self.edges.append(f'"{caller_func_signature}" -> "{current_function_signature}"')

            # Construct node string to be rendered in graphviz
            node_string = f'"{current_function_signature}" [label="{current_function_label}"'

            if self.node_properties_kwargs:
                node_string += ", " + ", ".join([f'{key}="{value}"' for key, value in self.node_properties_kwargs.items()])

            # current_function_label = current_function_label + ", ".join([f"{key}={value}" for key, value in self.node_properties_kwargs.items()])
            self.nodes.append(node_string)

            # Return after function call
            result = fn(*args, **kwargs)


            # Pop from tha stack after returning
            self.stack.pop()

            # If show_return_value flag is set, display the result
            if self.show_return_value:
                # If shape is set to record
                # Then separate function label and return value by a row
                if "record" in self.node_properties_kwargs.values():
                    current_function_label = "{" + current_function_label + f"|{result} }}"
                else:
                    current_function_label += f"\n => {result}"

            child_node = pydot.Node(name=current_function_signature, label=current_function_label, **self.node_properties_kwargs)
            self.graph.add_node(child_node)

            # If the function is called by another function
            if caller_function_name not in ['<module>', 'main']:
                parent_node = pydot.Node(name=caller_func_signature, label=caller_func_label, **self.node_properties_kwargs)
                self.graph.add_node(parent_node)
                edge = pydot.Edge(parent_node, child_node)
                self.graph.add_edge(edge)


            return result
        return wrapper