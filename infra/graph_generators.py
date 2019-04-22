#!/usr/bin/env python3
'''
This Module provides functions for generating simple networks
'''
import networkx as nx


def make_bidir(graph):
    """this function adds an edge with opposite direction for each edge present"""
    edges = graph.copy().edges
    for e in edges:
        graph.add_edge(e[1], e[0])
    
    return graph
    

#this function adds an edge with opposite direction for each edge present
#and removed the original edge
def reverse_dir(graph):
    """
    this function adds an edge with opposite direction for each edge present
    and removed the original edge
    """
    edges = graph.copy().edges
    for e in edges:
        graph.add_edge(e[1], e[0])
        graph.remove_edge(e[0], e[1])
    
    return graph

def set_types(graph, node_types="vanilla", edge_types="vanilla"):
    """ maps edge types and node types onto graph"""
    if type(node_types)== dict:
        for n in graph.nodes:
            try: 
                graph.nodes[n]['type']=node_types[n]
            except:
                raise ValueError('if node_types is dictionary, must be keyed to the nodes of the graph, '+str(node_types)+' provided')
    elif type(node_types) == str:
            nx.set_node_attributes(graph, node_types, "type")
    else:
        raise ValueError('node_types must be string or dictionary keyed to the nodes of the graph, '+str(node_types)+' provided')
    
    
    if type(edge_types)== dict:
        for e in graph.edges:
            try:
                graph.edges[e]['type']=edge_types[e]
            except:
                raise ValueError('edges_types must be string or dictionary keyed to the nodes of the graph, '+str(edge_types)+' provided')
    elif type(edge_types) == str:
        nx.set_edge_attributes(graph, edge_types, "type")
    else:
        raise ValueError('if edges_types is dictionary, must keyed to the edges of the graph, '+str(edge_types)+' provided')
        
        return graph

def line_graph_gen(num_nodes, bidir=False, node_type_name="vanilla", edge_type_name="vanilla"):
    """returns a line graph of length num_nodes"""
    
    if not(type(num_nodes)==int)or(num_nodes<1):
        raise ValueError('num_nodes must be positive integer, '+str(num_nodes)+' provided')
        
    if not(type(bidir)==bool):
        raise ValueError('bidir must be boolean, '+str(bidir)+' provided')
        
    
    graph = nx.path_graph(num_nodes, create_using=nx.MultiDiGraph)
    if bidir:
        graph = make_bidir(graph)

    graph = set_types(graph, edge_types=node_type_name, node_types=edge_type_name)
    
    return graph


def star_graph_gen(num_nodes, kind="sink", node_type_name="vanilla", edge_type_name="vanilla"):
    """returns a star graph of length num_nodes"""
    
    if not(type(num_nodes)==int)or(num_nodes<1):
        raise ValueError('num_nodes must be positive integer, '+str(num_nodes)+' provided')
        
    if not(kind in ["sink", "source", "bidir"]):
        raise ValueError('kind must be "sink", "source" or "bidir", '+str(kind)+' provided')
    
    graph = nx.MultiDiGraph(nx.star_graph(num_nodes-1))

    for n in range(1,num_nodes):
        if kind == "sink":
            graph.remove_edge(0,n)
        elif kind == "source":
            graph.remove_edge(n,0)

    graph = set_types(graph, edge_types=node_type_name, node_types=edge_type_name)
    
    return graph


def circle_graph_gen(num_nodes, bidir=False, node_type_name="vanilla", edge_type_name="vanilla"):
    """returns a cycle graph of length num_nodes"""
    
    if not(type(num_nodes)==int)or(num_nodes<1):
        raise ValueError('num_nodes must be positive integer, '+str(num_nodes)+' provided')
        
    if not(type(bidir)==bool):
        raise ValueError('bidir must be boolean, '+str(bidir)+' provided')
        
    graph = nx.cycle_graph(num_nodes, create_using=nx.MultiDiGraph)
    
    if bidir:
        graph = make_bidir(graph)
    
    graph = set_types(graph, edge_types=node_type_name, node_types=edge_type_name)

    return graph


def tree_graph_gen(rate, height, kind="sink", node_type_name="vanilla", edge_type_name="vanilla"):
    """returns a tree graph of depth height and splitting rate rate"""
    
    if not(type(rate)==int)or(rate<1):
        raise ValueError('rate must be positive integer, '+str(rate)+' provided')
        
    if not(type(height)==int)or(height<1):
        raise ValueError('height must be positive integer, '+str(height)+' provided')
    
    if not(kind in ["sink", "source", "bidir"]):
        raise ValueError('kind must be "sink", "source" or "bidir", '+str(kind)+' provided')
        
    graph = nx.balanced_tree(rate, height, create_using=nx.MultiDiGraph)
    
    if kind == "sink":
        graph = reverse_dir(graph)
    elif kind == "bidir":
        graph = make_bidir(graph)

    graph = set_types(graph, edge_types=node_type_name, node_types=edge_type_name)

    return graph
