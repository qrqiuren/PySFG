# -*- coding: utf-8 -*-

# Symbolic Transfer Function Solver for Signal Flow Graphs
#
# Author: 秋纫

from itertools import combinations
from functools import reduce

import strictyaml as yml
import networkx as nx
from sympy import S
from sympy.abc import _clash


class SignalFlowGraph:
    """
    The signal flow graph class.

    Usage
    -----
    TODO
    """
    def __init__(self, filename):
        """
        Initializes a signal flow graph.

        Args:
            filename - YAML file name of the SFG.
        """

        # Read YAML file
        with open(filename, encoding='utf-8') as f:
            yaml_data = yml.load(f.read()).data

        # Parse the YAML file
        self.graph = nx.DiGraph()
        self.sources = set(yaml_data['sources'])
        self.sinks = set(yaml_data['sinks'])
        self.nodes = set(yaml_data['nodes'])
        all_nodes = self.sources | self.sinks | self.nodes
        for direction, tf in yaml_data['edges'].items():
            from_node, to_node = direction.split('~>')
            from_node, to_node = from_node.strip(), to_node.strip()
            if from_node not in all_nodes:
                print('Error: Node ' + from_node + ' is not in the node list!')
                exit(1)
            if to_node not in all_nodes:
                print('Error: Node ' + to_node + ' is not in the node list!')
                exit(1)
            if from_node == to_node:
                print('Error: Selfloop detected at node ' + from_node)
                exit(1)
            self.graph.add_edge(from_node, to_node, expr=S(tf, _clash))

        # Find cycles and their gains in the graph
        self.cycles = list(map(lambda x: tuple(x),
                               nx.simple_cycles(self.graph)))
        self.cycle_gain = dict()
        for cycle in self.cycles:
            gain = self.graph.edges[cycle[-1], cycle[0]]['expr']
            for i in range(len(cycle) - 1):
                gain *= self.graph.edges[cycle[i], cycle[i+1]]['expr']
            self.cycle_gain[tuple(cycle)] = gain

        # Find determinant Δ of the graph
        self.Δ = self._find_cofactor(self.cycles)
        # print(self.Δ)

    def find_graph_gain(self, from_node: str, to_node: str):
        """
        Find the graph gain between two nodes.
        """

        def is_nontouching(path1, path2):
            """Check if two paths/cycles are nontouching to each other."""
            return set(path1).isdisjoint(set(path2))

        paths = nx.all_simple_paths(self.graph, from_node, to_node)

        gain = 0
        for path in paths:
            # Calculate the path gain
            path_gain = 1
            for i in range(len(path) - 1):
                path_gain *= self.graph.edges[path[i], path[i+1]]['expr']

            # Calculate the path's cofactor
            nontouching_cycles = []
            for cycle in self.cycles:
                if is_nontouching(path, cycle):
                    nontouching_cycles.append(cycle)
            cofactor = self._find_cofactor(nontouching_cycles)

            # Add to graph gain
            gain += path_gain * cofactor

        return gain / self.Δ

    def find_graph_gain_to(self, to_node: str):
        """
        Find the graph gain from all source nodes to a sink node.
        """
        gain = reduce(lambda g, s: g + self.find_graph_gain(s, to_node) * S(s),
                      self.sources, 0)
        return gain

    def _find_cofactor(self, cycles: list):
        """
        Give a set of cycles and find the gain in the graph.
        """
        cofactor = 1
        sign = 1
        for i in range(len(cycles)):
            sign *= -1
            for subcycles in combinations(cycles, i+1):
                # Check if the combinations are not touchable
                full_len = len(reduce(lambda x, y: x | set(y),
                                      subcycles, set()))
                if full_len == reduce(lambda x, y: x + len(y), subcycles, 0):
                    # If the combination doesn't have cycles that are touchable
                    # to each other, then add the gain to cofactor
                    cofactor += \
                        reduce(lambda x, y: x * self.cycle_gain[y],
                               subcycles, sign)
        return cofactor


if __name__ == '__main__':
    sfg = SignalFlowGraph('example_sfg/pll_single.yml')
    print(sfg.find_graph_gain('φ_ref', 'φ_out'))
    print(sfg.find_graph_gain_to('φ_out'))
    # import doctest
    # doctest.testmod()
