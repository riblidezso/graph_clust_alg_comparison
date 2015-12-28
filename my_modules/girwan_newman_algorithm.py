import networkx as nx

######################################################
# for GN benchmark
######################################################

def argmax(in_list):
    return in_list.index(max(in_list)) 
    
def my_gn_algorithm_4_benchmark(input_g):
    #create a local copy, the graph will be changed
    g=nx.Graph(input_g)
    
    #check for number of components
    if(nx.number_connected_components(g) > 4 ):
        print "Too many components "
        raise Exception
        
    #do the algorithm
    while(nx.number_connected_components(g) < 4 ):
        #get betweenness centralities
        bc=nx.edge_betweenness_centrality(g)
        #remove highest
        g.remove_edge( *bc.keys()[ argmax(bc.values())])
        
    return [list(nodes) for nodes in nx.connected_component_subgraphs(g)]


######################################################
# for real data
######################################################

from networkx.algorithms.community import girvan_newman
from community import modularity

def gn_best_partition(graph):
    #do all the cuts
    all_levels=girvan_newman(graph)
    
    #calculate modularity for all levels
    level_mods=[nx_gn_output_level_modularity(level,graph) for level in all_levels]
    
    #return the level with the highest modularity
    return all_levels[level_mods.index(max(level_mods))]


def nx_gn_output_level_modularity(nx_gn_output_level,test_g):
    # create partition accepted by modularity function
        partition=dict()
        for partitions,i in zip(nx_gn_output_level,range(len(nx_gn_output_level))):
            for node in partitions:
                partition[node]=i

    #calculate and retun modularity
        return modularity(partition,test_g)
