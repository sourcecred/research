#!/usr/bin/env python3
"""
This Module provides unit tests for functions for generating simple networks
"""

import networkx as nx
import unittest
from graph_generators import (
    line_graph_gen,
    circle_graph_gen,
    star_graph_gen,
    tree_graph_gen,
    bidirectional,
    reverse,
    set_types,
)


class GraphTest(unittest.TestCase):
    def assertIsopmorphic(self, g1, g2):
        self.assertTrue(nx.is_isomorphic(g1, g2))

    def assertIsomorphicEdges(self, g1, edges):
        g2 = nx.MultiDiGraph()
        g2.add_edges_from(edges)
        self.assertIsopmorphic(g1, g2)


class BidirectionalTest(GraphTest):
    def test_empty_graph(self):
        g = nx.MultiDiGraph()
        bidir = bidirectional(g)
        self.assertIsopmorphic(g, bidir)

    def test_simple_graph(self):
        g = nx.MultiDiGraph()
        g.add_edge(1, 2)
        bidir_expected = nx.MultiDiGraph()
        bidir_expected.add_edge(1, 2)
        bidir_expected.add_edge(2, 1)
        bidir_actual = bidirectional(g)
        self.assertIsopmorphic(bidir_expected, bidir_actual)

    def test_bidirectional_graph(self):
        g = nx.MultiDiGraph()
        g.add_edge(1, 2)
        g.add_edge(2, 1)
        # Since it's a multidigraph, every edge gets doubled
        expected_bidir = nx.MultiDiGraph()
        expected_bidir.add_edges_from([(1, 2), (2, 1), (2, 1), (1, 2)])
        self.assertIsopmorphic(expected_bidir, bidirectional(g))

    def test_non_mutating(self):
        g = nx.MultiDiGraph()
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g_copy = g.copy()
        bidirectional(g)
        self.assertIsopmorphic(g, g_copy)

    def test_path(self):
        g = bidirectional(nx.path_graph(3, create_using=nx.MultiDiGraph))
        self.assertIsomorphicEdges(g, [(0, 1), (1, 0), (1, 2), (2, 1)])


class ReversedTest(GraphTest):
    def test_empty_graph(self):
        g = nx.MultiDiGraph()
        r = reverse(g)
        self.assertIsopmorphic(g, r)

    def test_simple_graph(self):
        g = nx.MultiDiGraph()
        # Putting in 3 nodes so the reversed graph and the input aren't isomorphic
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        reversed_expected = nx.MultiDiGraph()
        reversed_expected.add_edge(2, 1)
        reversed_expected.add_edge(3, 1)
        reversed_actual = reverse(g)
        self.assertIsopmorphic(reversed_expected, reversed_actual)

    def test_path(self):
        g = nx.path_graph(4, create_using=nx.MultiDiGraph)
        g = reverse(g)
        self.assertIsomorphicEdges(g, [(1, 0), (2, 1), (3, 2)])

    def test_bidirectional_graph(self):
        g = nx.MultiDiGraph()
        g.add_edge(1, 2)
        g.add_edge(2, 1)
        self.assertIsopmorphic(g, reverse(g))

    def test_non_mutating(self):
        g = nx.MultiDiGraph()
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g_copy = g.copy()
        reverse(g)
        self.assertIsopmorphic(g, g_copy)


class Graph_Generators_Line_Graph(GraphTest):
    def test_line_graph_gen_sanity(self):
        g = line_graph_gen(4)
        self.assertIsomorphicEdges(g, [(0, 1), (1, 2), (2, 3)])

    def test_line_graph_gen_bidir(self):
        g = line_graph_gen(4, bidir=True)
        self.assertIsomorphicEdges(g, [(0, 1), (1, 2), (1, 0), (2, 3), (2, 1), (3, 2)])

    def test_line_graph_gen_bogus_bidir(self):
        with self.assertRaises(ValueError):
            line_graph_gen(4, bidir="troll")


class Graph_Generators_Circle_Graph(GraphTest):
    def test_circle_graph_gen_sanity(self):
        g = circle_graph_gen(4)
        self.assertIsomorphicEdges(g, [(0, 1), (1, 2), (2, 3), (3, 0)])

    def test_circle_graph_gen_bidir(self):
        g = circle_graph_gen(4, bidir=True)
        # (node, neighbor)
        self.assertIsomorphicEdges(
            g, [(0, 1), (0, 3), (1, 2), (1, 0), (2, 3), (2, 1), (3, 0), (3, 2)]
        )

    def test_circle_graph_gen_bogus_bidir(self):
        with self.assertRaises(ValueError):
            circle_graph_gen(4, bidir="troll")


class Graph_Generators_Star_Graph(GraphTest):

    # how to validate that 'kind' is either 'source', 'sink', or 'bidir' ??

    def test_star_graph_sink(self):
        g = star_graph_gen(4)
        self.assertIsomorphicEdges(g, [(1, 0), (2, 0), (3, 0)])

    def test_star_graph_source(self):
        g = star_graph_gen(4, kind="source")
        self.assertIsomorphicEdges(g, [(0, 1), (0, 2), (0, 3)])

    def test_star_graph_bidir(self):
        g = star_graph_gen(4, kind="bidir")
        self.assertIsomorphicEdges(g, [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)])

    def test_star_graph_gen_bogus(self):
        with self.assertRaises(ValueError):
            star_graph_gen(4, kind="troll")


class Graph_Generators_Tree_Graph(GraphTest):
    # note: our default is diff from networkx's default in this case (sink vs source)
    def test_tree_graph_source_sink(self):
        g = tree_graph_gen(2, 2)
        self.assertIsomorphicEdges(g, [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 2)])

    def test_treeGraph_source(self):
        g = tree_graph_gen(2, 2, kind="source")
        self.assertIsomorphicEdges(g, ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)))

    def test_tree_graph_bidir(self):
        g = tree_graph_gen(2, 2, kind="bidir")
        self.assertIsomorphicEdges(
            g,
            [
                (0, 1),
                (0, 2),
                (1, 3),
                (1, 4),
                (1, 0),
                (2, 5),
                (2, 6),
                (2, 0),
                (3, 1),
                (4, 1),
                (5, 2),
                (6, 2),
            ],
        )

    def test_tree_graph_gen_bogus(self):
        with self.assertRaises(ValueError):
            tree_graph_gen(2, 2, kind="troll")


class Graph_Generators_Set_Types(GraphTest):
    def test_set_types_str(self):
        g = nx.path_graph(3, create_using=nx.MultiDiGraph)

        g = set_types(g, node_types="foo", edge_types="bar")

        # each node and edge should have the correct 'type' value
        for k, v in nx.get_node_attributes(g, "type").items():
            self.assertEqual(v, "foo")

        for k, v in nx.get_edge_attributes(g, "type").items():
            self.assertEqual(v, "bar")

    def test_set_types_dict(self):
        g = nx.path_graph(3, create_using=nx.MultiDiGraph)

        node_dict = {0: "foo0", 1: "foo1", 2: "foo2"}
        edge_dict = {(0, 1, 0): "bar0", (1, 2, 0): "bar1"}

        g = set_types(g, node_types=node_dict, edge_types=edge_dict)

        # each node and edge should have the correct 'type' value
        for k, v in nx.get_node_attributes(g, "type").items():
            self.assertEqual(v, node_dict[k])

        for k, v in nx.get_edge_attributes(g, "type").items():
            self.assertEqual(v, edge_dict[k])

    def test_set_types_bogus_node_type(self):
        g = nx.path_graph(3, create_using=nx.MultiDiGraph)

        node_input = 0
        edge_dict = {(0, 1, 0): "bar0", (1, 2, 0): "bar1"}

        with self.assertRaises(ValueError):
            set_types(g, node_types=node_input, edge_types=edge_dict)

    def test_set_types_bogus_edge_type(self):
        g = nx.path_graph(3, create_using=nx.MultiDiGraph)

        node_dict = {0: "foo0", 1: "foo1", 2: "foo2"}
        edge_input = 0

        with self.assertRaises(ValueError):
            set_types(g, node_types=node_dict, edge_types=edge_input)


if __name__ == "__main__":
    unittest.main()
