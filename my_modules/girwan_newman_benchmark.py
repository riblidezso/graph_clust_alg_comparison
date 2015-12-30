import networkx as nx
import numpy as np

from collections import Counter

#function to create GN benchmark graph with given expected value in-partition edges
def create_GN_benchmark_graph(k_in):
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
    '''
    function to evaluate a partition
    
    input is the igraph output
    
    From Newman's article: (Fast algorithm for detecting community structure in networks)
    
        The criterion for deciding correct classification is as follows.
        We find the largest set of vertices that are grouped together by 
        the algorithm in each of the four known communities. If the algorithm
        puts two or more of these sets in the same group, then all vertices 
        in those sets are considered incorrectly classi- fied. Otherwise, 
        they are considered correctly classified. All other vertices not in
        the largest sets are considered incorrectly classified.
        
    '''
    #get largest groups fro each original group
    groups=[]
    for i in xrange(4):
        groups.append(get_largest_group(partition[i*32:(i+1)*32]))
        
    #add up sizes and check overlapping
    correct_count=0
    for i in xrange(4):
        #check for overlapping
        correct=True
        for j in xrange(4):
            if i!=j and groups[i][0]==groups[j][0] :
                correct=False
        
        #sum if correct
        if correct:
            correct_count+=groups[i][1]
            
    return correct_count/128.0


def get_largest_group(input_list):
    '''
    function to calculate largest group and its count
    '''
    group_counts=Counter(input_list)
    max_group_count=max(group_counts.values())
    group=group_counts.keys()[argmax(group_counts.values())]
    return group,max_group_count


def argmax(in_list):
    return in_list.index(max(in_list)) 