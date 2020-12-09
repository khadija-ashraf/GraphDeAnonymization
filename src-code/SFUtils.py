import math
import traceback

class SFUtils:

    @staticmethod
    def derive_structural_features(G, node, degree_seq_G, BETA, TOP_K, nx, da_nodes):
        ####### find fd_i, Degree
        fd_i = SFUtils.get_degree(G, node)
        ####### find fn_i, Neighborhood
        fn_i = SFUtils.get_neighborhood(G, node, BETA)
        ####### find fK_i, Top-K reference distance
        fK_i = SFUtils.get_top_k_reference_dist(G, node, degree_seq_G, TOP_K, nx)
        ####### find fl_i, Landmark reference distance
        fl_i = SFUtils.get_landmark_dist(node, G, da_nodes, nx)
        return fd_i, fn_i, fK_i, fl_i

    ####### find fd_i, Degree
    @staticmethod
    def get_degree(G, i):
        fd_i = []
        if math.isnan(G.degree()(i)) or math.isinf(G.degree()(i)): return 0
        fd_i.append(G.degree()(i))
        return fd_i

    @staticmethod
    def get_top_k_reference_dist(G, i, degree_sequence, TOP_K, nx):
        # find all the nodes upto ALPHA-th largest degree,
        # if we set K = ALPHA, then Aa is ideally the set of nodes we are looking for in here
        # for each k in ALPHA from [0, ALPHA] find node group with same k-th largest degree in G1
        # 999 here is to define a very large path distance between i and any k.
        # the idea is, 999 will never be picked up as its a large path distance
        fK_i = dict.fromkeys(range(TOP_K), 999)
        for k in range(TOP_K):
            k_th_largest_deg_val = degree_sequence[k]
            k_largest_degree_nodes = []
            for n, d in G.degree():
                if i != n and G.degree()(n) == k_th_largest_deg_val:
                    k_largest_degree_nodes.append(n)

            # find the shortest path length between 'i' and every 'k_largest_degree_nodes'
            intermediate_dist = []
            for node in k_largest_degree_nodes:
                try:
                    intermediate_dist.append(nx.dijkstra_path_length(G, i, node))
                except nx.exception.NetworkXNoPath:
                    print("K: no path between ", i, " to ", node)

            # the shortest path among mutiple kth largest degree nodes
            if not intermediate_dist: continue
            fK_i[k] = min(intermediate_dist)
        return fK_i


    @staticmethod
    def get_landmark_dist(i, G, da_nodes, nx):
        #fl_i = dict.fromkeys(da_nodes, 0)
        fl_i = [0 for i in range(len(da_nodes))]
        for node in da_nodes:
            try:
                fl_i.append(nx.dijkstra_path_length(G, i, node))
                # fl_i[node] = nx.dijkstra_path_length(G, i, node)
            except nx.exception.NetworkXNoPath:
                fl_i.append(-1) # no path exists between two nodes
                #print("L: no path between ",i, " to ", node)
        return fl_i


    @staticmethod
    def get_neighborhood(G, i, BETA):
        # initialise BETA-dimensional vector
        fn_i = [BETA for i in range(BETA)]
        try:
            # find all neighbors of 'i' along with their degree
            neighbrs_i = G.adj[i]
            neighbrs_degrees = []
            for neighbr in neighbrs_i:
                neighbrs_degrees.append(len(G.adj[neighbr]))  # degree of neighbors
            neighbrs_degrees = sorted(neighbrs_degrees, reverse=True)
            fn_i[0: len(neighbrs_degrees)] = neighbrs_degrees
        except KeyError as e:
            traceback.print_exc()
        return fn_i

    @staticmethod
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

    @staticmethod
    def get_neighbrs(G, node):
        return G.adj[node]


    # @staticmethod
    # def get_cos_simi(a, b):
    #     return np.inner(a, b) / (norm(a) * norm(b))

    @staticmethod
    def get_cos_simi(v1, v2):
        #compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(v1)):
            x = v1[i]
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        return sumxy / math.sqrt(sumxx * sumyy)

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

