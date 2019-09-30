# -*- coding: utf-8 -*-

# Unit Tests for Signal Flow Graphs designed with pytest
#
# Author: 秋纫

from sympy import S

from pysfg import SignalFlowGraph

graph_path = 'test/test_sfgs/'


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

    def test_mason56fig6a(self):
        """Test Fig. 6(a) of [Mason'56]."""
        sfg = SignalFlowGraph(graph_path + 'mason56fig6a.yml')
        gain_sfg = sfg.find_graph_gain('1', '4')
        gain_paper = S('(d*(1 - b*e) + a*b*c)/(1 - b*e)')
        assert gain_sfg == gain_paper

    def test_mason56fig6e(self):
        """Test Fig. 6(e) of [Mason'56]."""
        sfg = SignalFlowGraph(graph_path + 'mason56fig6e.yml')
        gain_sfg = sfg.find_graph_gain('x1', 'y1')
        gain_paper = S('(g*(1-h*i-j*c-h*b*c*d+h*i*j*c)+a*i*e*(1-j*c)+a*b*c*d*e)/(1-f*g-h*i-j*c-f*a*i*e-h*b*c*d-f*a*b*c*d*e+f*g*h*i+f*g*j*c+h*i*j*c+f*a*i*e*j*c+f*g*h*b*c*d-f*g*h*i*j*c)')
        assert gain_sfg == gain_paper
