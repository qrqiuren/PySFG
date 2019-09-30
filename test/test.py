# -*- coding: utf-8 -*-

# Unit Tests for Signal Flow Graphs designed with pytest
#
# Author: 秋纫

from sympy import S

import pytest

from pysfg.pysfg import SignalFlowGraph

graph_path = 'test_sfgs/'


class TestSignalFlowGraph:
    """
    Unit Test for class `SignalFlowGraph`.

    Example graphs are given from the following references.

    Reference
    ---------
    [Mason'56] S. J. Mason, "Further Properties of Signal Flow Graphs",
               Proceedings of the IRE, p.p. 920-926, July 1956.
    """

    def test_mason56fig5a(self):
        """Test Fig. 5(a) of [Mason'56]."""
        sfg = SignalFlowGraph(graph_path + 'mason56fig5a.yml')
        gain_sfg = sfg.find_graph_gain('1', '6')
        gain_paper = S('(a*b*c + d*(1-b*f))/(1-a*e-b*f-c*g-d*g*f*e+a*e*c*g)')
        assert gain_sfg == gain_paper

