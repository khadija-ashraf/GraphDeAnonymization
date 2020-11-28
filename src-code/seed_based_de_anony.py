import networkx as nx
from Utils import *
import numpy as np
import time
import gc


THETA = 0.1
START_TIME = time.time()

G1 = nx.read_edgelist('input/G1.edgelist', comments='#', delimiter = ' ',
                      create_using=nx.DiGraph(), nodetype=int)

directed_G1 = G1.is_directed()


G2 = nx.read_edgelist('input/G2.edgelist', comments='#', delimiter = ' ',
                      create_using=nx.DiGraph(), nodetype=int)

directed_G2 = G2.is_directed()

# Note: we load the seed mapping file as a directed graph. We assume that the
# mapping between G1 and G2 nodes are also some kind of edges. This idea will help us make
# many operations (i.e., finding a node, finding neighbors, finding corresponding overlapping node,
# adding new mappings, etc.) on nodes easier
mapping = nx.read_edgelist('input/seed_node_pairs.txt', comments='#', delimiter =' ',
                           create_using=nx.DiGraph(), nodetype=int)

mapping_image = nx.DiGraph.reverse(mapping, copy=True)

# Reading the seeds separately into different mapping lists
left_seeds = np.loadtxt('input/seed_node_pairs.txt').astype(int)[:, 0]
right_seeds = np.loadtxt('input/seed_node_pairs.txt').astype(int)[:, 1]



# Propagation:
# Input: lgraph: left graph, rgraph: right graph
# Note: we are implementing the propagationStep including all the heuristics
# (Edge directionality, Node degrees, Revisiting nodes, Reverse match)
# mentioned by the authors of the paper "De-anonymizing Social Networks by Arvind N. and Vitaly S."

# Revisiting nodes: Following the authors approach we are iterating for all nodes
# in lgraph to find best mapping among all rgraph nodes.
i = 0
#target_to_aux = Utils(G1, G2, seeds)
lgraph = G1
rgraph = G2

i = 0
lgraph_visit_dict = dict()
rgraph_visit_dict = dict()

# We assume all left nodes in the seed_node_pairs.txt are from G1 and all
# right nodes are from G2

Utils.populate_visit_dict(lgraph_visit_dict, lgraph, left_seeds)
Utils.populate_visit_dict(rgraph_visit_dict, rgraph, right_seeds)

for lnode in lgraph.nodes:
    if lgraph_visit_dict[lnode]: continue  #lnode is already mapped
    similarity_scores = Utils.matchScores(lgraph, rgraph,
                                          lgraph_visit_dict, rgraph_visit_dict, \
                                          mapping, lnode)

    if Utils.eccentricity(similarity_scores) < THETA: continue
    max_score = max(similarity_scores.values())  # maximum score
    max_scoring_nodes = [k for k, v in similarity_scores.items() if v == max_score]  # getting all keys containing the `maximum`

    if len(max_scoring_nodes) < 0: continue
    picked_max_score_rnode = max_scoring_nodes[0] # the first node
    mapping.add_edge(lnode, picked_max_score_rnode)
    lgraph_visit_dict[lnode] = True
    rgraph_visit_dict[picked_max_score_rnode] = True

    i = i + 1
    if i == 3:
        break


# writing final mapped seed edgelist

sorted_seed_pairs = sorted(mapping.edges, key=lambda x: x[0])
with open('output/AshrafSeedBased.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in sorted_seed_pairs))

collected = gc.collect()
print("Garbage collector: collected", "%d objects." % collected)
print("--- Total Execution time : %s seconds ---" % (time.time() - START_TIME))
