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

    
    graph = nx.MultiDiGraph(nx.star_graph(num_nodes-1))

    for n in range(1,num_nodes):
        if kind == "sink":
            graph.remove_edge(0,n)
        elif kind == "source":
            graph.remove_edge(n,0)

    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph


def circle_graph_gen(num_nodes, bidir=False, node_type_name="vanilla", edge_type_name="vanilla"):

    graph = nx.cycle_graph(num_nodes, create_using=nx.MultiDiGraph)
    
    if bidir:
        graph = make_bidir(graph)
    
    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph


def tree_graph_gen(rate, height, kind="sink", node_type_name="vanilla", edge_type_name="vanilla"):

    graph = nx.balanced_tree(rate, height, create_using=nx.MultiDiGraph)
    
    if kind == "sink":
        graph = reverse_dir(graph)
    elif kind == "bidir":
        graph = make_bidir(graph)

    nx.set_node_attributes(graph, node_type_name, "type")
    nx.set_edge_attributes(graph, edge_type_name, "type")

    return graph
