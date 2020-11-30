import time
import networkx as nx
from UtilsSeedFree import *
import os
import psutil

START_TIME = time.time()
ALPHA = 10 # [10, 30], means getting 10 to degree nodes form Va and Vu
GAMMA = 1 # [1, 4]
BETA = 0 # will be assigned later with the largest dergee value among G1, G2 nodes
TOP_K = ALPHA
#c1, c2 ∈ [0.1, 0.3], c3 ∈ [0.4, 0.8], c4 = 0 || Note, c1,2,3,4 ∈ [0, 1], must be c1 + c2 + c3 + c4 = 1
c1 = 0.1
c2 = 0.1
c3 = 0.8
c4 = 0



G1_directed = nx.read_edgelist('input/unseed_G1_mainCopy.edgelist', \
                               comments='#', delimiter =' ',
                               create_using=nx.DiGraph(), nodetype=int)



G2_directed = nx.read_edgelist('input/unseed_G2_mainCopy.edgelist', \
                               comments='#', delimiter =' ',
                               create_using=nx.DiGraph(), nodetype=int)

#UtilsSeedFree.analysing_degree(G1_directed, G2_directed)

G1 = G1_directed.to_undirected()
G2 = G2_directed.to_undirected()
Aa = Au = []

degree_list_G1 = G1.degree()
degree_list_G2 = G2.degree()

degree_sequence_G1 = sorted([d for n, d in degree_list_G1], reverse=True)
degree_sequence_G2 = sorted([d for n, d in degree_list_G2], reverse=True)

Aa = UtilsSeedFree.get_top_degree(degree_list_G1, degree_sequence_G1, ALPHA)
Au = UtilsSeedFree.get_top_degree(degree_list_G2, degree_sequence_G2, ALPHA)

max_degree_val_G1 = degree_sequence_G1[0]
max_degree_val_G2 = degree_sequence_G2[0]

if max_degree_val_G1 > max_degree_val_G2:
    BETA = max_degree_val_G1
else:
    BETA = max_degree_val_G2

iteration = 0
for i in Aa:
    ####### find fd_i, Degree
    fd_i = UtilsSeedFree.get_degree(G1, i)
    ####### find fn_i, Neighborhood
    fn_i  = UtilsSeedFree.get_neighborhood(G1, i, BETA)
    ####### find fK_i, Top-K reference distance
    fK_i = UtilsSeedFree.get_top_k_reference_dist(G1, i, degree_sequence_G1, TOP_K, nx)
    ####### find fl_i, Landmark reference distance
    fl_i = []

    structural_similarities = dict()

    for j in Au:
        ####### find fd_j, Degree
        fd_j = UtilsSeedFree.get_degree(G2, j)
        ####### find fn_j, Neighborhood
        fn_j = UtilsSeedFree.get_neighborhood(G2, j, BETA)
        ####### find fK_j, Top-K reference distance
        fK_j = UtilsSeedFree.get_top_k_reference_dist(G2, j, degree_sequence_G2, TOP_K, nx)
        ####### find fl_i, Landmark reference distance
        fl_j = []

        # calculate the structural similarity 'phi(i,j)'
        structural_similarities[j] = UtilsSeedFree.get_structural_similarity(\
                                            fd_i, fd_j, fn_i, fn_j, fK_i, fK_j, \
                                            fl_i, fl_j, c1, c2, c3, c4)

        # get top similarity
        candidate_set_i = UtilsSeedFree.get_top_similarity(i, Au, GAMMA, structural_similarities)

    iteration = iteration + 1
    if iteration == 3:
        break



#Va = [x for x in Va if x not in Aa]
#Aa = [n for n in degree_list if degree_list[n] >= lower_bound_deg_rng]


process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes

print("--- Total Execution time : %s seconds ---" % (time.time() - START_TIME))