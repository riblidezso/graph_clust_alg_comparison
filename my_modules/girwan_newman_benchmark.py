import networkx as nx
import numpy as np
from collections import Counter

def create_GN_benchmark_graph(k_in):
    """create GN benchmark graph with given expected value of intra-partition edges"""
    #calculate edge probabilities
    k_out=16-k_in
    p=k_in/31.0
    q=k_out/96.0

    #create graph/partitions with nodes
    g=nx.Graph()
    for j in xrange(1,5):
        nodes=[j*100+i for i in xrange(32)]
        g.add_nodes_from(nodes)

    #add intra partition edges
    #loop over partitions
    for k in xrange(1,5):
        # loop over nodes
        for i in xrange(32):
            # loop over nodes higher than i
            # to avoid revisiting an edge
            # note: xrange gives different result than range here
            for j in range(i+1,32):
                if np.random.random() < p:
                    g.add_edge(k*100+i,k*100+j)

    #add cross partition edges
    #loop over partitions
    for k1 in xrange(1,5):
        #loop over partitions higher than k1
        # to avoid revisiting an edge
        for k2 in range(k1+1,5):
            if (k1!=k2):
                #no need to worry about revisiting now
                for i in xrange(32):
                    for j in xrange(32):
                        if np.random.random() < q:
                            g.add_edge(k1*100+i,k2*100+j)

    return g


def fraction_of_vertices_correctly_classified(partition):
    """
    Evaluate a partition of GN synthetic test graph, return fvcc score.
    
    From Newman's article: (Fast algorithm for detecting community structure in networks)
    
        The criterion for deciding correct classification is as follows.
        We find the largest set of vertices that are grouped together by 
        the algorithm in each of the four known communities. If the algorithm
        puts two or more of these sets in the same group, then all vertices 
        in those sets are considered incorrectly classi- fied. Otherwise, 
        they are considered correctly classified. All other vertices not in
        the largest sets are considered incorrectly classified.
    """

    #generate true partititon
    real_part=[]
    for i in xrange(4):
        for j in xrange(32):
            real_part.append(i)
            
    #compare partition to true partition
    fvcc=general_fvcc(partition,real_part)
    return fvcc


def general_fvcc(partition,real_partition):
    """ 
    Evaluate a clustering partition scheme in regard to a true scheme with the fvcc metric.
   
    From Newman's article: (Fast algorithm for detecting community structure in networks)
    
        The criterion for deciding correct classification is as follows.
        We find the largest set of vertices that are grouped together by 
        the algorithm in each of the four known communities. If the algorithm
        puts two or more of these sets in the same group, then all vertices 
        in those sets are considered incorrectly classi- fied. Otherwise, 
        they are considered correctly classified. All other vertices not in
        the largest sets are considered incorrectly classified.
        
    """
    #get groups in the original clusters
    real_clusters=dict()
    for cluster,i in zip(real_partition,xrange(len(real_partition))):
        if real_clusters.has_key(cluster):
            real_clusters[cluster].append(i)
        else:
            real_clusters[cluster]=[i]    
    
    #get largest groups for each original group
    groups=dict()
    for cluster,nodes in real_clusters.iteritems():
        groups[cluster]=get_largest_group([partition[i] for i in nodes])
        
    #add up sizes and check overlapping
    correct_count=0
    for i in real_clusters.keys():
        #check for overlapping
        correct=True
        for j in real_clusters.keys():
            if i!=j and groups[i][0]==groups[j][0] :
                correct=False
        
        #sum if correct
        if correct:
            correct_count+=groups[i][1]
            
    fvcc=float(correct_count)/len(partition)
    return fvcc


def get_largest_group(input_list):
    """ Calculate largest group and its count in a list."""
    group_counts=Counter(input_list)
    max_group_count=max(group_counts.values())
    group=group_counts.keys()[argmax(group_counts.values())]
    return group,max_group_count


def argmax(in_list):
    """ Return argmax of a list."""
    return in_list.index(max(in_list)) 
    
from seaborn.apionly import color_palette
#plotting
import matplotlib.pyplot as plt        
def plot_example_graph(k_in):
    """Plot an example GN benchmark graph."""
    #import sns palette for nice colors

    #set nice colors for graph
    cols=color_palette('husl',4)
    node_colors=[]
    for i in xrange(4):
        c=cols[i]
        for j in xrange(32):
            node_colors.append(c)

    #create graph
    test_g=create_GN_benchmark_graph(k_in=k_in)
    
    #plot it
    fig=plt.figure(figsize=(16,9))
    plt.axis('off')
    #get layout
    pos = nx.spring_layout(test_g)
    #plot nodes
    nodes=nx.draw_networkx_nodes(test_g,pos,node_color=node_colors,node_size=400)
    # delete node edges
    nodes.set_edgecolor('none')
    #draw edges
    nx.draw_networkx_edges(test_g,pos,edge_color='lightgrey')
    #add title
    dump=plt.title(r'Example synthetic benchmark graph $k_{in}=$'+str(k_in),fontsize=18)
    #return fig
    