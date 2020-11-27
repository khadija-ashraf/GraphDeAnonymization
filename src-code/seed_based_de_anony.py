import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
from Utils import *

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

# Propagation:
# Input: lgraph, rgraph
# Note: we are implementing the propagationStep including all the heuristics
# (Edge directionality, Node degrees, Revisiting nodes, Reverse match)
# mentioned by the authors of the paper "De-anonymizing Social Networks by Arvind N. and Vitaly S."

for lnode in lgraph.nodes:
    scores = [0 for rnode in rgraph.nodes]

    scores[lnode] = Utils.match_score(lgraph, rgraph, seeds, lnode)
    break


