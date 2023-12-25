import copy

import pydot
import glob
import os
import shutil
import imageio

from visualiser import Node, Edge, Graph


class Animation:
    def __init__(self):
        self.frames = []
        self._frame_id = 0

    def next_step(self, frame):
        self.frames.append(copy.deepcopy(frame))
        self._frame_id += 1

    @staticmethod
    def make_directory():
        if not os.path.exists("frames"):
            os.makedirs("frames")

    def next_frame(self):
        pass

    def previous_frame(self):
        pass

    def get_frame(self, frame_id):
        return self.frames[frame_id]

    def get_frames(self):
        return self.frames[::]

    def write_frame(self, frame_id):
        frame = self.get_frame(frame_id)

        dot_graph, *rest = pydot.graph_from_dot_data(frame)
        dot_graph.write_png(f"frames/temp_{frame_id}.png")

    def write_file(self):
        self.make_directory()

        for frame_id in range(len(self.get_frames())):
            self.write_frame(frame_id)

    def write_gif(self, name="out.gif", delay=3):
        self.write_file()

        images = []

        # sort frames images in ascending order to number in image filename
        # image filename: frames/temp_1.png
        sorted_images = sorted(
            glob.glob("frames/*.png"),
            key=lambda fn: int(fn.split("_")[1].split(".")[0])
        )

        for filename in sorted_images:
            images.append(imageio.imread(filename))

        imageio.mimsave(name, images, duration=delay)
        # Delete temporary directory
        shutil.rmtree("frames")

