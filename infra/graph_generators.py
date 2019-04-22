#!/usr/bin/env python3
'''
This Module provides functions for generating simple networks
'''
import networkx as nx


#this function adds an edge with opposite direction for each edge present
def make_bidir(graph):
    edges = graph.copy().edges
    for e in edges:
        graph.add_edge(e[1], e[0])
    
    return graph
    

#this function adds an edge with opposite direction for each edge present
#and removed the original edge
def reverse_dir(graph):
    edges = graph.copy().edges
    for e in edges:
        graph.add_edge(e[1], e[0])
        graph.remove_edge(e[0], e[1])
    
    return graph


#todo add error handling

def line_graph_gen(num_nodes, bidir=False, node_type_name="vanilla", edge_type_name="vanilla"):

    graph = nx.path_graph(num_nodes, create_using=nx.MultiDiGraph)
    if bidir:
        graph = make_bidir(graph)

    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph


def star_graph_gen(num_nodes, kind="sink", node_type_name="vanilla", edge_type_name="vanilla"):

    star = nx.star_graph(num_nodes)
    graph = nx.MultiDiGraph()

    for e in star.edges:
        if (kind == "source") or (kind == "bidir"):
            graph.add_edge(e[0], e[1])
        if (kind == "sink") or (kind == "bidir"):
            graph.add_edge(e[1], e[0])

    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph


def circle_graph_gen(num_nodes, bidir=False, node_type_name="vanilla", edge_type_name="vanilla"):

    circle = nx.cycle_graph(num_nodes, create_using=nx.MultiDiGraph)
    if not (bidir):
        graph = circle
    else:
        edges = circle.edges
        graph = nx.MultiDiGraph()
        for e in edges:
            graph.add_edge(e[0], e[1])
            graph.add_edge(e[1], e[0])

    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph


def tree_graph_gen(r, h, kind="sink", node_type_name="vanilla", edge_type_name="vanilla"):

    tree = nx.balanced_tree(r, h, create_using=nx.MultiDiGraph)

    if kind == "source":
        graph = tree
    elif kind == "sink":
        graph = nx.MultiDiGraph()
        for e in tree.edges:
            graph.add_edge(e[1], e[0])
    elif kind == "bidir":
        graph = nx.MultiDiGraph()
        for e in tree.edges:
            graph.add_edge(e[1], e[0])
            graph.add_edge(e[0], e[1])

    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph
