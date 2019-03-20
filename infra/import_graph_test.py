import unittest
import json
import os
from collections import Counter

import import_graph


class TestTypeMatching(unittest.TestCase):
    def test_node_type_matching(self):
        # Testing the basic functionality. Cases don't need to be exhaustive;
        # missing types will be caught during the whole-graph import tests.
        example_issue = [
            "sourcecred",
            "github",
            "ISSUE",
            "sourcecred",
            "sourcecred",
            "34",
        ]
        example_repo = ["sourcecred", "github", "REPO", "sourcecred", "sourcecred"]
        self.assertEqual(import_graph.node_type(example_issue), "github/issue")
        self.assertEqual(import_graph.node_type(example_repo), "github/repo")
        with (self.assertRaises(ValueError)):
            import_graph.node_type(["non", "existent", "node"])

    def test_edge_type_matching(self):
        # Testing the basic functionality. Cases don't need to be exhaustive;
        # missing types will be caught during the whole-graph import tests.
        example_has_parent = [
            "sourcecred",
            "github",
            "HAS_PARENT",
            "6",
            "sourcecred",
            "github",
            "ISSUE",
            "sourcecred",
            "pm",
            "1",
        ]

        example_authors = [
            "sourcecred",
            "github",
            "AUTHORS",
            "5",
            "sourcecred",
            "github",
            "USERLIKE",
            "USER",
            "BrianLitwin",
            "4",
            "sourcecred",
            "git",
            "COMMIT",
            "0cae9fa77c1d7d8b8fe3fe2d316a6782757862e4",
        ]
        self.assertEqual(import_graph.edge_type(example_has_parent), "github/hasParent")
        self.assertEqual(import_graph.edge_type(example_authors), "github/authors")
        with (self.assertRaises(ValueError)):
            import_graph.edge_type(["non", "existent", "edge"])


def sample_graphs_directory():
    wd = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(wd, os.pardir, "sample-graphs")


class TestImportGraph(unittest.TestCase):
    def test_for_sourcecred_sourcecred(self):
        sourcecred_sourcecred = os.path.join(
            sample_graphs_directory(), "sourcecred_sourcecred.json"
        )

        with open(sourcecred_sourcecred, "r") as f:
            sourcecred_graph_data = json.load(f)
        graph = import_graph.json_to_graph(sourcecred_graph_data)

        # Some sanity checks on the loaded graph, based on node type counts
        # We don't expect exact counts because the expectation is that these graphs are
        # regularly re-generated.
        # Under normal circumstances the counts of these entities only increases,
        # so this test should be reasonably robust.
        node_count = Counter()
        for n in graph.nodes(data=True):
            node_count[n[1]["type"]] += 1

        self.assertEqual(node_count["github/repo"], 1)
        self.assertGreater(node_count["github/user"], 10)
        self.assertGreater(node_count["github/issue"], 100)
        self.assertGreater(node_count["github/pull"], 800)
        self.assertGreater(node_count["github/review"], 200)
        self.assertGreater(node_count["github/comment"], 500)
        self.assertGreater(node_count["git/commit"], 800)

        # Some sanity checks on the loaded graph, based on edge type counts.
        # Same reasoning as the tests above.
        edge_count = Counter()
        for e in graph.edges(data=True):
            edge_count[e[2]["type"]] += 1

        self.assertGreater(edge_count["github/authors"], 1000)
        self.assertGreater(edge_count["github/references"], 100)
        self.assertGreater(edge_count["github/hasParent"], 1000)
        self.assertGreater(edge_count["github/mergedAs"], 800)
        self.assertGreater(edge_count["github/reactsThumbsUp"], 20)
        self.assertGreater(edge_count["github/reactsHooray"], 5)
        self.assertGreater(edge_count["github/reactsHeart"], 10)
        self.assertGreater(edge_count["github/reactsRocket"], 1)
        self.assertGreater(edge_count["git/hasParent"], 800)

    def test_all_graphs_load(self):
        files = os.listdir(sample_graphs_directory())
        graph_files = [
            os.path.join(sample_graphs_directory(), f)
            for f in files
            if f.endswith(".json")
        ]
        self.assertGreater(len(graph_files), 3)
        for g in graph_files:
            if g.endswith("sourcecred_sourcecred.json"):
                continue  # This one is loaded in a separate test case.
            with open(g, "r") as f:
                data = json.load(f)
            # Just verify it doesn't throw an error.
            import_graph.json_to_graph(data)


if __name__ == "__main__":
    unittest.main()
