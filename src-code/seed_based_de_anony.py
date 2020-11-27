import networkx as nx
from Utils import *
import numpy as np
import time

THETA = 1.0
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
seeds = nx.read_edgelist('input/seed_node_pairs.txt', comments='#', delimiter = ' ',
                      create_using=nx.DiGraph(), nodetype=int)

lgraph = G1
rgraph = G2

utils = Utils(lgraph, rgraph, seeds)


# Propagation:
# Input: lgraph: left graph, rgraph: right graph
# Note: we are implementing the propagationStep including all the heuristics
# (Edge directionality, Node degrees, Revisiting nodes, Reverse match)
# mentioned by the authors of the paper "De-anonymizing Social Networks by Arvind N. and Vitaly S."

# Revisiting nodes: Following the authors approach we are iterating for all nodes
# in lgraph to find best mapping among all rgraph nodes.
for lnode in lgraph.nodes:
    similarity_scores = dict()
    for rnode in rgraph.nodes:
        similarity_scores[rnode] = utils.get_matched_neigbr_count(lnode, rnode)

    if Utils.eccentricity(similarity_scores) < THETA: continue
    max_score = max(similarity_scores.values())  # maximum score
    max_scoring_nodes = [k for k, v in similarity_scores.items() if v == max_score]  # getting all keys containing the `maximum`

    print('%d is max score, and %d number of nodes scored max ' %(max_score,len(max_scoring_nodes)))
    picked_max_score_rnode = max_scoring_nodes[0] # the first node
    print("Picked max rnode: ", picked_max_score_rnode)
    break
'''
#seeds.add_edge(lnode, new_mapping_rnode)
'''

print("--- Total Execution time : %s seconds ---" % (time.time() - START_TIME))
