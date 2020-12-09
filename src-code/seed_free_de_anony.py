import time
import networkx as nx
from SFUtils import *
import sys
import gc
import traceback


START_TIME = time.time()
ALPHA = 10 # [10, 30], means getting 10th top largest degree nodes form Va and Vu
GAMMA = 2 # [1, 4]
BETA = 0 # will be assigned later with the largest dergee value among G1, G2 nodes
TOP_K = ALPHA
THETA = 0.1 # similarity Threshold
#c1, c2 element of [0.1, 0.3], c3 element of [0.4, 0.8], c4 = 0 || Note, c1,2,3,4 element of [0, 1], must be c1 + c2 + c3 + c4 = 1
c1 = 0.1
c2 = 0.1
c3 = 0.8
c4 = 0

G1_directed = None
G2_directed = None
mapping = None
G1 = None
G2 = None
mapping = None
try:
    G1 = nx.read_edgelist('input/leftoff_G1.edgelist', \
                                   comments='#', delimiter =' ',
                                   nodetype=int)

except Exception  as e:
    print("Loading G1")

    G1_directed = nx.read_edgelist('input/unseed_G1.edgelist', \
                                   comments='#', delimiter =' ',
                                   create_using=nx.DiGraph(), nodetype=int)
    G1 = G1_directed.to_undirected()
try:
    G2 = nx.read_edgelist('input/leftoff_G2.edgelist', \
                                   comments='#', delimiter =' ',
                                   nodetype=int)

except Exception  as e:
    print("Loading G2")
    G2_directed = nx.read_edgelist('input/unseed_G2.edgelist', \
                                   comments='#', delimiter =' ',
                                   create_using=nx.DiGraph(), nodetype=int)
    G2 = G2_directed.to_undirected()

#UtilsSeedFree.analysing_degree(G1, G2)

G1_mapped_nodes = []
G2_mapped_nodes = []
iteration = 0
mapping = nx.Graph()

try:
    while True:
        START_TIME = time.time()
        degree_list_G1 = G1.degree()
        degree_list_G2 = G2.degree()

        degree_sequence_G1 = sorted([d for n, d in degree_list_G1], reverse=True)
        degree_sequence_G2 = sorted([d for n, d in degree_list_G2], reverse=True)

        max_degree_val_G1 = degree_sequence_G1[0]
        max_degree_val_G2 = degree_sequence_G2[0]

        if max_degree_val_G1 > max_degree_val_G2:
            BETA = max_degree_val_G1
        else:
            BETA = max_degree_val_G2

        Aa = Au = []
        Aa = SFUtils.get_top_degree(degree_list_G1, degree_sequence_G1, ALPHA)
        Au = SFUtils.get_top_degree(degree_list_G2, degree_sequence_G2, ALPHA)

        j_features = dict()
        for j in Au:
            j_features[j] = SFUtils.derive_structural_features(G2,
                                                               j,
                                                               degree_sequence_G2,
                                                               BETA, TOP_K,
                                                               nx, G2_mapped_nodes)
        da_scheme = dict()
        struct_simi = dict()
        candidate_visit_map = dict.fromkeys(Au, False)

        for i in Aa:
            da_scheme[i] = dict() # initializing
            struct_simi[i] = dict.fromkeys(Au, 0)
            fd_i, fn_i, fK_i, fl_i = SFUtils.derive_structural_features(G1,
                                                                        i,
                                                                        degree_sequence_G1,
                                                                        BETA, TOP_K,
                                                                        nx, G1_mapped_nodes)

            for j in Au:
                fd_j, fn_j, fK_j, fl_j = j_features[j]

                # calculate the structural similarity 'phi(i,j)'
                if fd_i and fd_j:
                    try:

                        degree_similarity = SFUtils.get_cos_simi(fd_i, fd_j)
                        if ~math.isnan(degree_similarity):
                            struct_simi[i][j] += c1 * degree_similarity
                    except Exception as e:
                        print("degree_similarity i, j", i,j)


                if fn_i and fn_j:
                    try:
                        neighborhood_similarity = SFUtils.get_cos_simi(fn_i, fn_j)
                        if ~math.isnan(neighborhood_similarity):
                            struct_simi[i][j] += c2 * neighborhood_similarity
                    except Exception as e:
                        print("neighborhood_similarity i, j", i,j)

                if fK_i and fK_j:
                    try:
                        top_k_similarity = SFUtils.get_cos_simi(list(fK_i.values()), list(fK_j.values()))
                        if ~math.isnan(top_k_similarity):
                            struct_simi[i][j] += c3 * top_k_similarity
                    except Exception as e:
                        print("top_k_similarity i, j", i,j)

                if fl_i and fl_j:
                    try:
                        landmark_ref_similarity = SFUtils.get_cos_simi(fl_i, fl_j)
                        if ~math.isnan(landmark_ref_similarity):
                            struct_simi[i][j] += c4 * landmark_ref_similarity
                    except Exception as e:
                        print("landmark_ref_similarity i, j", i,j)

            # sort the similarity score dict in decreasing order
            sorted_simi = sorted(struct_simi[i].items(), key=lambda x: x[1], reverse=True)
            candidate_set = []
            pruned_simi = sorted_simi[0: GAMMA]
            for index, tuple in enumerate(pruned_simi):
                candidate_set.append(tuple[0])

            # create set of DA scheme (i,j): basically a list of high probable mappings of (i, j)
            da_error = 0

            min_da_error = sys.float_info.max
            min_error_j = None
            for c in candidate_set:
                if candidate_visit_map[c]:continue  # Consistent Rule: this 'j' has already been mapped to an 'i'
                i_neighbr = SFUtils.get_neighbrs(G1, i)
                j_neighbr = SFUtils.get_neighbrs(G2, c)

                da_error = len([x for x in i_neighbr if x not in j_neighbr]) \
                           + len([x for x in j_neighbr if x not in i_neighbr])

                if da_error < min_da_error:
                    min_da_error = da_error
                    min_error_j = c

            if min_error_j is None: continue
            da_scheme[i][min_error_j] = min_da_error
            candidate_visit_map[min_error_j] = True

        mapping_cnt = 0
        for i in da_scheme.keys():
            for j in da_scheme[i].keys():
                if struct_simi[i][j] >= THETA:
                    mapping.add_edge(i, j)
                    G1_mapped_nodes.append(i)
                    G2_mapped_nodes.append(j)
                    mapping_cnt = mapping_cnt + 1
                    G1.remove_node(i)
                    G2.remove_node(j)

        print("Mapped edge count:", len(mapping.edges))
        collected = gc.collect()
        print("Garbage collector: collected", "%d objects." % collected)

        if mapping_cnt == 0:
            print("no mapping found: ",mapping_cnt)
            break

except Exception as e:
    traceback.print_exc()
finally:
    # sorted_seed_pairs = sorted(mapping.edges, key=lambda x: x[0])

    leftoff_g1_file = "input/leftoff_G1.edgelist"
    leftoff_g2_file = "input/leftoff_G2.edgelist"
    nx.write_edgelist(G1, leftoff_g1_file, data=False)
    nx.write_edgelist(G2, leftoff_g2_file, data=False)

    leftoff_seed_pair = "".join(("output/AshrafSeedFree_",str(THETA),".txt"))
    with open(leftoff_seed_pair, 'a') as fp:
        fp.write('\n')
        fp.write('\n'.join('%s %s' % x for x in mapping.edges))

    print("Mapped edge count:",len(mapping.edges))
    collected = gc.collect()
    print("Garbage collector: collected", "%d objects." % collected)
    print("--- Total Execution time : %s seconds ---" % (time.time() - START_TIME))

