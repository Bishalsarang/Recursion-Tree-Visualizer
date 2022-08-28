import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recursion-visualiser",
    version="1.0.3",
    author="Bishal Sarangkoti",
    author_email="sarangbishal@gmail.com",
    description="A small python package to visualise recursive function on Python. It draws recursion tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bishalsarang/Recursion-Tree-Visualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pydot", "imageio"],
    python_requires='>=3.6',
)