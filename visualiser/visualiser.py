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
    def __init__(self, ignore_args=None, show_argument_name=True,
                 show_return_value=True, node_properties_kwargs={}):
        self.init_graph()
        # If enabled shows keyword arguments ordered by keys
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

        # sort frames images in ascending order to number in image filename
        # image filename: frames/temp_1.png
        sorted_images = sorted(
            glob.glob("frames/*.png"),
            key=lambda fn: int(fn.split("_")[1].split(".")[0])
        )

        for filename in sorted_images:
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

        cls.init_graph()

    def extract_arg_strings(self, *args, **kwargs):
        """
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
        @ wraps(fn)
        def wrapper(*args, **kwargs):
            global dot_str_body
            # Increment total number of nodes when a call is made
            self.node_count += 1

            # Update kwargs by adding dummy keyword node_num which helps to
            # uniquely identify each node
            kwargs.update({'node_num': self.node_count})
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
            if self.stack:
                caller_func_kwargs.update({'node_num': self.stack[-1]})

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

            if caller_func_name == '<module>':
                print(f"Drawing for {function_signature}")

            # Push node_count to stack
            self.stack.append(self.node_count)
            # Before actual function call delete keyword 'node_num' from kwargs
            del kwargs['node_num']

            self.edges.append(
                f'"{caller_func_signature}" -> "{function_signature}"')

            # Construct node string to be rendered in graphviz
            node_string = f'"{function_signature}" [label="{function_label}"'

            if self.node_properties_kwargs:
                node_string += ", " + \
                    ", ".join([f'{key}="{value}"' for key,
                               value in self.node_properties_kwargs.items()])

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
                    function_label = "{" + \
                        function_label + f"|{result} }}"
                else:
                    function_label += f"\n => {result}"

            child_node = pydot.Node(name=function_signature,
                                    label=function_label,
                                    **self.node_properties_kwargs)
            self.graph.add_node(child_node)

            # If the function is called by another function
            if caller_func_name not in ['<module>', 'main']:
                parent_node = pydot.Node(name=caller_func_signature,
                                         label=caller_func_label,
                                         **self.node_properties_kwargs)
                self.graph.add_node(parent_node)
                edge = pydot.Edge(parent_node, child_node)
                self.graph.add_edge(edge)

            return result
        return wrapper

    @classmethod
    def init_graph(cls):
        # Total number of nodes
        cls.node_count = 0
        cls.graph = pydot.Dot(graph_type="digraph", bgcolor="#fff3af")
        # To track function call numbers
        cls.stack = []
        cls.edges = []
        cls.nodes = []
