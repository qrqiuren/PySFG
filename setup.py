# -*- coding: utf-8 -*-

# Symbolic Transfer Function Solver for Signal Flow Graphs
#
# Author: 秋纫

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysfg",
    version="0.0.2",
    author="秋纫",
    author_email="qrqiuren@users.noreply.github.com",
    description="A Python package for symbolic signal flow graph analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qrqiuren/PySFG",
    packages=setuptools.find_namespace_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ],
    python_requires='>=3.6',
)
