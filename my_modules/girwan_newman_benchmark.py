import networkx as nx
import numpy as np

def create_GN_benchmark_graph(k_in):
    k_out=16-k_in
    
    p=k_in/31.0
    q=k_out/96.0

    g=nx.Graph()
    partitions=[]
    for j in xrange(1,5):
        nodes=[j*100+i for i in xrange(32)]
        partitions.append(nodes)
        g.add_nodes_from(nodes)

    for k in xrange(1,5):
        for i in xrange(32):
            for j in xrange(32):
                if i!=j:
                    if np.random.random() < p:
                        g.add_edge(k*100+i,k*100+j)

    for k1 in xrange(1,5):
        for k2 in xrange(1,5):
            if (k1!=k2):
                for i in xrange(32):
                    for j in xrange(32):
                        if i!=j:
                            if np.random.random() < q:
                                g.add_edge(k1*100+i,k2*100+j)

    return g,partitions

