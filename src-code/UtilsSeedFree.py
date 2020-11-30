import math
from scipy import spatial

class UtilsSeedFree:
    # GetTopSimilarity(i, Λu, GAMMA) is a function to return 'GAMMA' no. of users
    @staticmethod
    # def get_top_similarity(i, Au, GAMMA, similarities):
    #     top_similar_auxilary_nodes = []
    #     # sort the similarity score dict in decreasing order
    #     sorted_simi = sorted(similarities, key=similarities.__getitem__, reverse=True)
    #     # get the GAMMA no. of highest scoring j nodes


    @staticmethod
    def get_structural_similarity(fd_i, fd_j, fn_i, fn_j, fK_i, fK_j, \
                                  fl_i, fl_j, c1, c2, c3, c4):
        degree_similarity = 1 - spatial.distance.cosine(fd_i, fd_j)
        neighborhood_similarity = 1 - spatial.distance.cosine(fn_i, fn_j)
        top_k_similarity = 1 - spatial.distance.cosine(fK_i, fK_j)
        landmark_ref_similarity = 1 - spatial.distance.cosine(fl_i, fl_j)
        return c1 * degree_similarity \
               + c2 * neighborhood_similarity \
               + c3 * top_k_similarity \
               + c4 * landmark_ref_similarity

    def get_top_similarity(i, Au, GAMMA):
        return 0

    ####### find fd_i, Degree
    @staticmethod
    def get_degree(G, i):
        return G.degree()(i)

    @staticmethod
    def get_top_k_reference_dist(G, i, degree_sequence, TOP_K, nx):
        # find all the nodes upto ALPHA-th largest degree,
        # if we set K = ALPHA, then Aa is ideally the set of nodes we are looking for in here
        # for each k in ALPHA from [0, ALPHA] find node group with same k-th largest degree in G1
        fK_i = dict()
        for k in range(TOP_K):
            k_th_largest_deg_val = degree_sequence[k]
            k_largest_degree_nodes = []
            for n, d in G.degree():
                if G.degree()(n) == k_th_largest_deg_val:
                    k_largest_degree_nodes.append(n)

            # find the shortest path length between 'i' and every 'k_largest_degree_nodes'
            intermediate_dist = []
            for node in k_largest_degree_nodes:
                intermediate_dist.append(nx.dijkstra_path_length(G, i, node))

            # the shortest path among mutiple kth largest degree nodes
            fK_i[k] = min(intermediate_dist)
        return fK_i


    @staticmethod
    def get_neighborhood(G, i, BETA):
        # initialise BETA-dimensional vector
        fn_i = [BETA for i in range(BETA)]
        # find all neighbors of 'i' along with their degree
        neighbrs_i = G.adj[i]
        neighbrs_degrees = []
        for neighbr in neighbrs_i:
            neighbrs_degrees.append(len(G.adj[neighbr]))  # degree of neighbors
        neighbrs_degrees = sorted(neighbrs_degrees, reverse=True)
        fn_i[0: len(neighbrs_degrees)] = neighbrs_degrees
        return fn_i

    def get_top_degree(degree_list, degree_sequence, ALPHA):
        A = []
        # descending ordered degree list of G, to find the Alpha-th largest degree value
        # the Alpha-th largest degree value defines the lower bound of degree value
        # to get selected into the 'Aa' or 'Au' node set

        lower_bound_deg_rng = degree_sequence[ALPHA - 1]

        # populate Aa or Au
        for n, d in degree_list:
            if degree_list(n) >= lower_bound_deg_rng:
                A.append(n)
        return A

    def set_alpha(G1, G2):
        alpha = 0
        avg_node_numbers = (G1.edges() + G2.edges()) / 2
        # now find log(node_number)
        alpha = math.log(avg_node_numbers, 2)
        return alpha

    @staticmethod
    def get_neighbrs(G, node):
        return G.adj[node]

    @staticmethod
    def analysing_degree(G1, G2):

        directed_G1 = G1.is_directed()
        directed_G2 = G2.is_directed()
        if directed_G1:
            print("G1 is directed")
        else:
            print("G1 is Undirected")

        if directed_G2:
            print("G2 is directed")
        else:
            print("G2 is Undirected")

        N, K = G1.order(), G1.size()
        avg_deg = float(K) / N
        print("G1 nodes: ", N)
        print("Average degree G1: ", avg_deg)
        degree_sequence = sorted([d for n, d in G1.degree()], reverse=True)
        highest_deg_G1 = degree_sequence[0]
        print("max degree G1: ", highest_deg_G1)

        N, K = G2.order(), G2.size()
        avg_deg = float(K) / N
        print("G2 nodes: ", N)
        print("Average degree G2: ", avg_deg)
        degree_sequence = sorted([d for n, d in G2.degree()], reverse=True)
        highest_deg_G2 = degree_sequence[0]
        print("max degree G2: ", highest_deg_G2)

        lgraph = G1.to_undirected()
        rgraph = G2.to_undirected()

        N, K = lgraph.order(), lgraph.size()
        avg_deg = float(K) / N
        print("lgraph nodes: ", N)
        print("Average degree lgraph: ", avg_deg)
        degree_sequence = sorted([d for n, d in lgraph.degree()], reverse=True)
        highest_deg_G1 = degree_sequence[0]
        print("max degree lgraph: ", highest_deg_G1)

        N, K = rgraph.order(), rgraph.size()
        avg_deg = float(K) / N
        print("rgraph nodes: ", N)
        print("Average degree rgraph: ", avg_deg)
        degree_sequence = sorted([d for n, d in rgraph.degree()], reverse=True)
        highest_deg_G2 = degree_sequence[0]
        print("max degree rgraph: ", highest_deg_G2)