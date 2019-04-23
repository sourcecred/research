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
    make_bidir,
    reverse_dir,
    set_types,
)


class Graph_Generators_Line_Graph(unittest.TestCase):
    def test_line_graph_gen_sanity(self):
        g = line_graph_gen(4)
        self.assertEqual(list(g.edges()), [(0, 1), (1, 2), (2, 3)])

    def test_line_graph_gen_bidir(self):
        g = line_graph_gen(4, bidir=True)
        # (node, neighbor)
        self.assertEqual(
            list(g.edges()), [(0, 1), (1, 2), (1, 0), (2, 3), (2, 1), (3, 2)]
        )

    def test_line_graph_gen_bogus_bidir(self):
        with self.assertRaises(ValueError):
            line_graph_gen(4, bidir="troll")


class Graph_Generators_Circle_Graph(unittest.TestCase):
    def test_circle_graph_gen_sanity(self):
        g = circle_graph_gen(4)
        self.assertEqual(list(g.edges()), [(0, 1), (1, 2), (2, 3), (3, 0)])

    def test_circle_graph_gen_bidir(self):
        g = circle_graph_gen(4, bidir=True)
        # (node, neighbor)
        self.assertEqual(
            list(g.edges()),
            [(0, 1), (0, 3), (1, 2), (1, 0), (2, 3), (2, 1), (3, 0), (3, 2)],
        )

    def test_circle_graph_gen_bogus_bidir(self):
        with self.assertRaises(ValueError):
            circle_graph_gen(4, bidir="troll")


class Graph_Generators_Star_Graph(unittest.TestCase):

    # how to validate that 'kind' is either 'source', 'sink', or 'bidir' ??

    def test_star_graph_sink(self):
        g = star_graph_gen(4)
        self.assertEqual(list(g.edges()), [(1, 0), (2, 0), (3, 0)])

    def test_star_graph_source(self):
        g = star_graph_gen(4, kind="source")
        self.assertEqual(list(g.edges()), [(0, 1), (0, 2), (0, 3)])

    def test_star_graph_bidir(self):
        g = star_graph_gen(4, kind="bidir")
        self.assertEqual(
            list(g.edges()), [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)]
        )

    def test_star_graph_gen_bogus(self):
        with self.assertRaises(ValueError):
            star_graph_gen(4, kind="troll")


class Graph_Generators_Tree_Graph(unittest.TestCase):
    # note: our default is diff from networkx's default in this case (sink vs source)
    def test_tree_graph_source_sink(self):
        g = tree_graph_gen(2, 2)
        self.assertEqual(
            list(g.edges()), [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 2)]
        )

    def test_treeGraph_source(self):
        g = tree_graph_gen(2, 2, kind="source")
        self.assertEqual(
            list(g.edges()), [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        )

    def test_tree_graph_bidir(self):
        g = tree_graph_gen(2, 2, kind="bidir")
        self.assertEqual(
            list(g.edges()),
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


class Graph_Generators_Set_Types(unittest.TestCase):
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


class Graph_Generators_Reverse_Dir(unittest.TestCase):
    def test_reverse_dir(self):
        g = nx.path_graph(4, create_using=nx.MultiDiGraph)

        g = reverse_dir(g)

        self.assertEqual(list(g.edges()), [(1, 0), (2, 1), (3, 2)])


class Graph_Generators_Make_Bidir(unittest.TestCase):
    def test_make_bidir(self):
        g = nx.path_graph(3, create_using=nx.MultiDiGraph)

        g = make_bidir(g)

        self.assertEqual(list(g.edges()), [(0, 1), (1, 2), (1, 0), (2, 1)])
