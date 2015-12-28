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
