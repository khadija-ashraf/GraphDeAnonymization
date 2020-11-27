import math
import statistics

class Utils:

    def __init__(self, lgraph = None, rgraph = None, mapping = None):
        self.lgraph = lgraph  #left graph, typically the target graph, here its G1
        self.rgraph = rgraph  #right graph, typically the auxiliary graph, here its G2
        self.mapping = mapping  # given seed node pairs

    @staticmethod
    def match_score(lgraph, rgraph, mapping, lnode):
        scores = [0 for rnode in rgraph.nodes]
        for (lnbr, lnode) in lgraph.edges:
            if lnbr not in mapping: continue
            rnbr = mapping[lnbr]
            for (rnbr, rnode) in rgraph.edges:
                if rnode in mapping.image: continue
                scores[rnode] += 1 / math.sqrt(rnode.in_degree)
        return scores

    def get_matched_neigbr_count(self, lnode, rnode):
        matched_neighbr_count = 0
        lnode_neighbrs = self.lgraph.adj[lnode] # fetching neighbors of lnode from lgraph
        rnode_neighbrs = self.rgraph.adj[rnode] # fetching neighbors of rnode from rgraph
        for lnode_neighbr in lnode_neighbrs:
            if lnode_neighbr not in self.mapping: continue
            mapped_rseed_node = self.mapping[lnode_neighbr]
            if mapped_rseed_node and list(mapped_rseed_node)[0] in rnode_neighbrs: continue
            matched_neighbr_count = matched_neighbr_count + 1

        return matched_neighbr_count

    @staticmethod
    def eccentricity(similarity_scores):

        if len(similarity_scores) < 2:
           # print(" Invalid Input ")
            return 0
        arr_size = len(similarity_scores)
        largest = second = -2454635434

        # Find the largest element
        largest = max(similarity_scores.values())

        # Find the second largest element
        for value in similarity_scores.values():
            if value != largest:
                second = max(second, value)

        standard_dev = statistics.stdev(similarity_scores.values())
        print('Standard Deviation: {0:.2f}'.format(standard_dev))
        if second == -2454635434 or (largest - second) == 0 or standard_dev == 0:
            return 0
        return (largest - second) / standard_dev
