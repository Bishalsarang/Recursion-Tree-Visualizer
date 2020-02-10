from visualiser.visualiser import Visualiser as vs

"""
Problem Link: https://stackoverflow.com/questions/33808653/recursion-tree-with-fibonacci-python/60126306#60126306
"""

@vs(node_properties_kwargs={"shape":"record", "color":"#f57542", "style":"filled", "fillcolor":"grey"})
def binary(length, outstr=""):
    if len(outstr) == length:
        print(outstr)
    else:
        for i in ["0", "1"]:
            binary(length=length, outstr=outstr + i)

binary(length=3,outstr="")
vs.make_animation("binary_string.gif", delay=2)