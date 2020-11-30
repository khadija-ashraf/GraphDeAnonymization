import networkx as nx


G1_directed = nx.read_edgelist('input/unseed_G1_mainCopy.edgelist', comments='#', delimiter =' ',
                               create_using=nx.DiGraph(), nodetype=int)



G2_directed = nx.read_edgelist('input/unseed_G2_mainCopy.edgelist', comments='#', delimiter =' ',
                               create_using=nx.DiGraph(), nodetype=int)

#UtilsSeedFree.analysing_degree(G1_directed, G2_directed)

G1 = G1_directed.to_undirected()
G2 = G2_directed.to_undirected()

nx.write_edgelist(G1, "unseed_G1_undirected.edgelist", data=False)
nx.write_edgelist(G2, "unseed_G2_undirected.edgelist", data=False)