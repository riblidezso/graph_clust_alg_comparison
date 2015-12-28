import networkx as nx
import numpy as np

#function to create GN benchmark graph with given expected value in-partition edges
def create_GN_benchmark_graph(k_in):
    #calculate edge probabilities
    k_out=16-k_in
    p=k_in/31.0
    q=k_out/96.0

    #create graph/partitions with nodes
    g=nx.Graph()
    partitions=[]
    for j in xrange(1,5):
        nodes=[j*100+i for i in xrange(32)]
        partitions.append(nodes)
        g.add_nodes_from(nodes)

    #add intra partition edges
    for k in xrange(1,5):
        for i in xrange(32):
            for j in xrange(32):
                if i!=j:
                    if np.random.random() < p:
                        g.add_edge(k*100+i,k*100+j)

    #add cross partition edges
    for k1 in xrange(1,5):
        for k2 in xrange(1,5):
            if (k1!=k2):
                for i in xrange(32):
                    for j in xrange(32):
                        if i!=j:
                            if np.random.random() < q:
                                g.add_edge(k1*100+i,k2*100+j)

    return g,partitions

#function to evaluate a given partition
#Note: partitions should be ordered as originally!!!
def evaluate_partition(partition):
    
    #check partition size
    if len(partition)!=4:
        print "Error, there should be 4 partitions"
        return -1
    
    #calculate correctly assigned nodes
    correct=0
    for part,j in zip(partition,xrange(1,5)):
        for node in part:
            if int(node)/100 == j:
                correct+=1
                
    return correct/128.0