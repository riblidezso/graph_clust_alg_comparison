"""Functions to work with igraph methods"""

import igraph
import networkx as nx
import numpy as np
import time
import matplotlib.pyplot as plt

from girwan_newman_benchmark import create_GN_benchmark_graph
from girwan_newman_benchmark import fraction_of_vertices_correctly_classified


def best_modularity_level_w_igraph_method(graph,igraph_method):
    """
    Run an igraph clustering method on the graph, return best clustering.
    
    Run the method, and select the best level of the dendogram.
        igraph select the best level based on hint from the algorithm
        (fastgreedy calculates modularities for each level on the fly ) or 
        if there is no hint recalculates modularity for each level, and selects the best one.
    Do workaround to avoid bug with initally disconnected graphs.
    """
    
    #run clustering
    dendrogram=igraph_method(graph)
    
    """
    Workaround:
        usually you would call dedrogram.as_clustering() it should return the best
        level of the dendrogram.
        BUT! there is a bug for an initially  unconnected graph, where this causes this method to fail.
            https://github.com/igraph/igraph/issues/675
    The workaround is to try to get the best cut, but if fails, get a lower one which at least exists.
    """
    
    #get best cut:
    n_best_clusters=dendrogram.optimal_count
    
    #get best cluster membership
    while( n_best_clusters <= len(graph.vs) ):
        #try with the best, if it fails increment level
        try:
            best_clusters=dendrogram.as_clustering(n_best_clusters).membership
            break
        except:
            n_best_clusters+=1
    
    return best_clusters


def nx_2_ig(nx_g):
    """
    Covert networkx graph to igraph graph.
    
    I started to work in networkx because i have already worked with that
    but later i started to use igraph because it has the fastgreedy
    algorithm implemented, and it is also supposed to be faster.
    """
    
    ig_g=igraph.Graph()
    #igraph docs say, you can add edges by name
    # but you actually cannot ...
    # so i maintain a name - id mapping
    id_name,name_id=dict(),dict()
    for node,i in zip(nx_g.nodes(),xrange(nx_g.number_of_nodes())):
        ig_g.add_vertex(name=node)
        id_name[i],name_id[node]=node,i
    
    #add edges in a list, because one by one is very slow
    ig_g.add_edges([(name_id[edge[0]],name_id[edge[1]]) for edge in nx_g.edges()])
        
    return ig_g,id_name,name_id


"""Functions to test on synthetic benchmark."""

def test_igraph_method(k_in,igraph_method):
    """
    Test an igraph community detection method on a random synthetic GN benchmark graph, return fvcc score.
    
    fvcc score is the fraction_of vertices correctly classified defined by Newman.
    """
    
    #create graph
    graph = create_GN_benchmark_graph(k_in=k_in)
    #turn it into an igraph graph
    ig_g,id_name,name_id = nx_2_ig(graph)
    
    # run the method with best level
    membership =  best_modularity_level_w_igraph_method(ig_g,igraph_method)
    
    #calculate quality of clustering
    fvcc=fraction_of_vertices_correctly_classified(membership)
    
    return fvcc


def repeat_test_igraph_method(k_in,igraph_method,M):
    """Repeat test_igraph_method M times."""
    corr_fracs=[test_igraph_method(k_in,igraph_method)  for x in xrange(M) ] 
    return corr_fracs


def scan_k_in_vals(igraph_method,N,M,k_in_min=4,k_in_max=16):
    """ Repeat repeat_test_igraph_method on a range of k_in value"""
    k_in_range=np.linspace(k_in_min,k_in_max,N)
    res = np.array([ repeat_test_igraph_method(k_in,igraph_method,M)  for k_in in k_in_range ])
    return res,k_in_range


"""Functions for testing on real data"""

def load_nx_from_edges_file(filename):
    """ Load networkx graph from a txt file containing edges."""
    g=nx.Graph()
    with open(filename) as file_h:
        for line in file_h:
            g.add_edge(line.split()[0],line.split()[1])
    return g

def load_ig_from_edges_file(filename):
    """ Load igraph graph from a txt file containing edges."""
    ig_g,id_name,name_id=nx_2_ig(load_nx_from_edges_file(filename))
    return ig_g,id_name,name_id

def test_igraph_method_on_real_graph(filename,igraph_method):
    """Test igraph community detection method on a real graph."""
    #load graph from edges
    graph,id_name,name_id=load_ig_from_edges_file(filename)
    
    #bechmark method
    start=time.time()
    membership=best_modularity_level_w_igraph_method(graph,igraph_method)
    modularity=graph.modularity(membership)
    exec_time=time.time()-start
    
    return membership,modularity,exec_time


def plot_real_graph(filename,membership,title,ax):
    """Plot a real graph with cluter membership colored."""
    #define pretty node colors
    from seaborn.apionly import color_palette
    cols=color_palette('husl',max(membership))
    node_cols=[]
    for i in membership:
        node_cols.append(cols[i-1])
        
    #load graph to plot
    nx_g=load_nx_from_edges_file(filename)
    
    #no frame
    plt.axis('off')
    
    #get layout
    pos = nx.spring_layout(nx_g)
    #plot nodes
    nodes=nx.draw_networkx_nodes(nx_g,pos,node_color=node_cols,node_size=50,ax=ax)
    # delete node edges
    nodes.set_edgecolor('none')
    #draw edges
    nx.draw_networkx_edges(nx_g,pos,edge_color='lightgrey',ax=ax)
    #add title
    dump=plt.title(title,fontsize=18)
