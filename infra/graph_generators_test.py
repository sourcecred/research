#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 17:17:54 2019

@author: Zargham
"""
import networkx as nx
import unittest
from graph_generators import lineGraphGen, starGraphGen, treeGraphGen


class GraphGenerators_LineGraph(unittest.TestCase):
    def test_lineGraphGen_sanity(self):
        g = lineGraphGen(4)
        self.assertEqual(list(g.edges()), [(0, 1), (1, 2), (2, 3)])

    def test_lineGraphGen_bidir(self):
        g = lineGraphGen(4, bidir=True)
        # (node, neighbor)
        self.assertEqual(
            list(g.edges()), [(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)]
        )


class GraphGenerators_StarGraph(unittest.TestCase):

    # how to validate that 'kind' is either 'source', 'sink', or 'bidir' ??

    def test_starGraph_sink(self):
        g = starGraphGen(4)
        self.assertEqual(list(g.edges()), [(1, 0), (2, 0), (3, 0), (4, 0)])

    def test_starGraph_source(self):
        g = starGraphGen(4, kind="source")
        self.assertEqual(list(g.edges()), [(0, 1), (0, 2), (0, 3), (0, 4)])

    def test_starGraph_bidir(self):
        g = starGraphGen(4, kind="bidir")
        self.assertEqual(
            list(g.edges()),
            [(0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 0), (4, 0)],
        )


class GraphGenerators_TreeGraph(unittest.TestCase):
    # note: our default is diff from networkx's default in this case (sink vs source)
    def test_treeGraph_source_sink(self):
        g = treeGraphGen(2, 2)
        self.assertEqual(
            list(g.edges()), [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 2)]
        )

    def test_treeGraph_source(self):
        g = treeGraphGen(2, 2, kind="source")
        self.assertEqual(
            list(g.edges()), [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        )

    def test_treeGraph_bidir(self):
        g = treeGraphGen(2, 2, kind="bidir")
        self.assertEqual(
            list(g.edges()),
            [
                (1, 0),
                (1, 3),
                (1, 4),
                (0, 1),
                (0, 2),
                (2, 0),
                (2, 5),
                (2, 6),
                (3, 1),
                (4, 1),
                (5, 2),
                (6, 2),
            ],
        )


# this is the way I might test that the types assigned in Z's functions are correct
# I think it would be a good idea to abstract out that logic into a helper function
# so that the code isn't duplicated in every generator


class GraphGenerators_SetType(unittest.TestCase):
    def test_lineGraphGen_setType(self):
        g = lineGraphGen(4, nodeTypeName="foo", edgeTypeName="bar")

        # each node and edge should have the correct 'type' value
        for k, v in nx.get_node_attributes(g, "type").items():
            self.assertEqual(v, "foo")

        for k, v in nx.get_edge_attributes(g, "type").items():
            self.assertEqual(v, "bar")
