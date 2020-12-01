import time
import networkx as nx
from SFUtils import *
import os
import psutil
import sys
import gc


START_TIME = time.time()
ALPHA = 10 # [10, 30], means getting 10 to degree nodes form Va and Vu
GAMMA = 2 # [1, 4]
BETA = 0 # will be assigned later with the largest dergee value among G1, G2 nodes
TOP_K = ALPHA
THETA = 0.1 # similarity Threshold
#c1, c2 ∈ [0.1, 0.3], c3 ∈ [0.4, 0.8], c4 = 0 || Note, c1,2,3,4 ∈ [0, 1], must be c1 + c2 + c3 + c4 = 1
c1 = 0.1
c2 = 0.1
c3 = 0.8
c4 = 0


'''
G1_directed = nx.read_edgelist('input/unseed_G1_mainCopy.edgelist', \
                               comments='#', delimiter =' ',
                               create_using=nx.DiGraph(), nodetype=int)



G2_directed = nx.read_edgelist('input/unseed_G2_mainCopy.edgelist', \
                               comments='#', delimiter =' ',
                               create_using=nx.DiGraph(), nodetype=int)

#UtilsSeedFree.analysing_degree(G1_directed, G2_directed)

G1 = G1_directed.to_undirected()
G2 = G2_directed.to_undirected()
'''
G1 = nx.read_edgelist('input/unseed_G1_undirected.edgelist', \
                               comments='#', delimiter =' ',
                               nodetype=int)



G2 = nx.read_edgelist('input/unseed_G2_undirected.edgelist', \
                               comments='#', delimiter =' ',
                               nodetype=int)

#UtilsSeedFree.analysing_degree(G1, G2)

mapping = nx.Graph()

Aa = Au = []

degree_list_G1 = G1.degree()
degree_list_G2 = G2.degree()

degree_sequence_G1 = sorted([d for n, d in degree_list_G1], reverse=True)
degree_sequence_G2 = sorted([d for n, d in degree_list_G2], reverse=True)

Aa = SFUtils.get_top_degree(degree_list_G1, degree_sequence_G1, ALPHA)
Au = SFUtils.get_top_degree(degree_list_G2, degree_sequence_G2, ALPHA)

max_degree_val_G1 = degree_sequence_G1[0]
max_degree_val_G2 = degree_sequence_G2[0]

if max_degree_val_G1 > max_degree_val_G2:
    BETA = max_degree_val_G1
else:
    BETA = max_degree_val_G2


j_features = dict()
for j in Au:
    j_features[j] = SFUtils.derive_structural_features(G2, j, degree_sequence_G2, BETA, TOP_K, nx)

iteration = 0
da_scheme = dict()
struct_simi = dict()
candidate_visit_map = dict.fromkeys(Au, False)

for i in Aa:
    da_scheme[i] = dict() # initializing
    struct_simi[i] = dict.fromkeys(Au, 0)

    fd_i, fn_i, fK_i, fl_i = SFUtils.derive_structural_features(G1, i, degree_sequence_G1, BETA, TOP_K, nx)

    for j in Au:
        fd_j, fn_j, fK_j, fl_j = j_features[j]

        # calculate the structural similarity 'phi(i,j)'
        '''
        K_i = list(fK_i.values())
        K_j = list(fK_j.values())
        struct_simi[i][j] = SFUtils.get_structural_similarity(fd_i, fd_j, fn_i, fn_j, K_i, fK_j, fl_i, fl_j, c1, c2, c3, c4)
        '''
        degree_similarity = 1 - spatial.distance.cosine(fd_i, fd_j)
        if math.isnan(degree_similarity): continue
        struct_simi[i][j] += c1 * degree_similarity

        neighborhood_similarity = 1 - spatial.distance.cosine(fn_i, fn_j)
        if math.isnan(neighborhood_similarity): continue
        struct_simi[i][j] += c2 * neighborhood_similarity

        top_k_similarity = 1 - spatial.distance.cosine(list(fK_i.values()), list(fK_j.values()))
        if math.isnan(top_k_similarity): continue
        struct_simi[i][j] += c3 * top_k_similarity

        # landmark_ref_similarity = 1 - spatial.distance.cosine(fl_i, fl_j)
        # if math.isnan(landmark_ref_similarity): continue
        # structural_similarities[j] += c4 * landmark_ref_similarity

    # sort the similarity score dict in decreasing order
    sorted_simi = sorted(struct_simi[i].items(), key=lambda x: x[1], reverse=True)
    candidate_set = []
    pruned_simi = sorted_simi[0: GAMMA]
    for index, tuple in enumerate(pruned_simi):
        candidate_set.append(tuple[0])

    # for node, score in pruned_simi:
    #     candidate_set.append(node)

    # get top similarity: get the GAMMA no. of highest scoring j nodes
    #candidate_set_i = UtilsSeedFree.get_top_similarity(i, Au, GAMMA, sorted_simi)
    print(candidate_set)

    # create set of DA scheme (i,j): basically a list of high probable mappings of (i, j)
    da_error = 0

    min_da_error = sys.float_info.max
    min_error_j = None
    for c in candidate_set:
        if candidate_visit_map[c]:continue  # Consistent Rule: this 'j' has already been mapped to an 'i'
        i_neighbr = SFUtils.get_neighbrs(G1, i)
        j_neighbr = SFUtils.get_neighbrs(G2, c)

        #i_neig_substruct_j_neig = [x for x in i_neighbr if x not in j_neighbr]
        #j_neig_substruct_i_neig = [x for x in j_neighbr if x not in i_neighbr]

        da_error = len([x for x in i_neighbr if x not in j_neighbr]) \
                   + len([x for x in j_neighbr if x not in i_neighbr])

        if da_error < min_da_error:
            min_da_error = da_error
            min_error_j = c

    if min_error_j is None: continue
    da_scheme[i][min_error_j] = min_da_error
    candidate_visit_map[min_error_j] = True

    # iteration = iteration + 1
    # if iteration == 3:
    #     break

mapping_cnt = 0
for i in da_scheme.keys():
    for j in da_scheme[i].keys():
        if struct_simi[i][j] >= THETA:
            mapping.add_edge(i, j)
            mapping_cnt = mapping_cnt + 1
            G1.remove_node(i)
            G2.remove_node(j)

    # if mapping_cnt == 0
#     break


nx.write_edgelist(mapping, "output/AshrafSeedFree.edgelist", data=False)

process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes

collected = gc.collect()
print("Garbage collector: collected", "%d objects." % collected)
print("--- Total Execution time : %s seconds ---" % (time.time() - START_TIME))