# PySFG

[![Build Status](https://travis-ci.com/qrqiuren/PySFG.svg?branch=master)](https://travis-ci.com/qrqiuren/PySFG)

A package for symbolic signal flow graph analysis.

The input reads a text file in a human-friendly coding format to describe the
signal flow graph. The program is able to calculate the transfer function
between two nodes.
The resulting symbolic expressions are easily interoperatable with
[Sympy](https://www.sympy.org/) and other scientific packages.

Requires Python >= 3.6.

## Installation

### For Users

```bash
$ pip install pysfg
```

### For Hackers

```bash
$ git checkout https://github.com/qrqiuren/PySFG.git
$ cd PySFG
$ python setup.py develop
```

## Tutorial

The signal flow graph is a good tool for various fields of engineers. Various
kinds of systems in real world engineering would be easily converted to signal
flow graphs.

Let's take an example. Suppose we have the following signal flow graph from an
electronic system.

![Electronic system](https://upload.wikimedia.org/wikipedia/commons/a/a1/Circuit_with_two_port_and_equivalent_signal_flow_graph.png)

Then, we can convert the graph into the following code `twoport.yml`:

```yml
# The `#` symbol starts a line of comment

# Define source nodes, sink nodes and other nodes
sources:
    - Vin
sinks:
    - V2    # We can use V2 directly as the sink node
nodes:
    - V1
    - I1
    - V2
    - I2

# Define edges
# Each edge has a format of `u ~> v: f`, where the edge points from node `u`
# to node `v`, with a transfer function of `f`. `f` is convertible to a
# SymPy expression.
# Fire Code is recommended to render `~>` symbol prettier.
edges:
    Vin ~> V1: 1    # Constants are acceptable

    # Admittance matrix
    V1 ~> I1: y11   # Symbols are acceptable
    V2 ~> I1: y12
    V1 ~> I2: y21
    V2 ~> I2: y22

    # Impedances
    I1 ~> V1: -Rin  # Expressions are acceptable
    I2 ~> V2: -RL
```

The code format is a subset of YAML (or "StrictYAML"). It avoids some
ambiguous syntax in YAML by default, while reserves the human-friendly
coding style.

Run the following Python commands to load and solve the transfer function
from node `Vin` to node `V2`:

```python
>>> from pysfg import SignalFlowGraph
>>> sfg = SignalFlowGraph('twoport.yml')
>>> tf = sfg.find_graph_gain('Vin', 'V2')
>>> print(tf)
-RL*y21/(RL*Rin*y11*y22 - RL*Rin*y12*y21 + RL*y22 + Rin*y11 + 1)
```

The result is a SymPy expression. It can be further used for calculation
in other programs.

# Task List

- [ ] Implement hierarchichal signal flow graph
