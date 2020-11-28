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

    def get_similarity_score(self, lnode, rnode):
        score = 0

        lnode_outgoing_neighbrs = list(self.lgraph.successors(lnode))
        rnode_outgoing_neighbrs = list(self.rgraph.successors(rnode))

        out_neighbr_match_count = 0
        for lnode_out_neighbr in lnode_outgoing_neighbrs:
            if lnode_out_neighbr not in self.mapping: continue
            mapped_rseed_node = self.mapping[lnode_out_neighbr]
            if mapped_rseed_node and list(mapped_rseed_node)[0] in rnode_outgoing_neighbrs:
                out_neighbr_match_count = out_neighbr_match_count + 1

        rnode_out_degree = len(rnode_outgoing_neighbrs)
        matching_cnt_normalized = 0;
        if rnode_out_degree > 0:
            matching_cnt_normalized = out_neighbr_match_count / math.sqrt(rnode_out_degree)
        score = score + matching_cnt_normalized

        lnode_incoming_neighbrs = list(self.lgraph.predecessors(lnode))
        rnode_incoming_neighbrs = list(self.rgraph.predecessors(rnode))

        in_neighbr_match_count = 0
        for lnode_in_neighbr in lnode_incoming_neighbrs:
            if lnode_in_neighbr not in self.mapping: continue
            mapped_rseed_node = self.mapping[lnode_in_neighbr]
            if mapped_rseed_node and list(mapped_rseed_node)[0] in rnode_incoming_neighbrs:
                in_neighbr_match_count = in_neighbr_match_count + 1

        rnode_in_degree = len(rnode_incoming_neighbrs)
        matching_cnt_normalized = 0;
        if rnode_in_degree > 0:
            matching_cnt_normalized = in_neighbr_match_count / math.sqrt(rnode_in_degree)
        score = score + matching_cnt_normalized
        return score

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
        #print('Standard Deviation: {0:.2f}'.format(standard_dev))
        if second == -2454635434 or (largest - second) == 0 or standard_dev == 0:
            return 0
        return (largest - second) / standard_dev
