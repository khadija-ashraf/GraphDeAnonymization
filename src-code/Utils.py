import math
import statistics
from collections import defaultdict

class Utils:

    def __init__(self, lgraph = None, rgraph = None, mapping = None):
        self.lgraph = lgraph  #left graph, typically the target graph, here its G1
        self.rgraph = rgraph  #right graph, typically the auxiliary graph, here its G2
        self.mapping = mapping  # given seed node pairs

    @staticmethod
    def matchScores(lgraph, rgraph,
                    lgraph_visit_dict, rgraph_visit_dict, \
                    mapping, lnode):
        scores = defaultdict(lambda: 0)

        # find all out-degree neighbors of lnode
        lnode_out_neighbrs = list(lgraph.successors(lnode))

        # find all in-degree neighbors of lnode
        lnode_in_neighbrs = list(lgraph.predecessors(lnode))

        # filterout all mapped neighbors among 'lnode_out_neighbrs'
        l_mapped_out_neighbr = Utils.filterMappedNeighbrs(lnode_out_neighbrs, lgraph_visit_dict)

        # filterout all mapped neighbors among 'lnode_in_neighbrs'
        l_mapped_in_neighbr = Utils.filterMappedNeighbrs(lnode_in_neighbrs, lgraph_visit_dict)

        for rnode in rgraph.nodes:
            # iterate for all unmapped rnodes
            if rgraph_visit_dict[rnode]: continue  # rnode is already mapped

            ### Implementing Out-degree
            # find out-degree neighbors of each rnode
            rnode_out_neighbrs = list(rgraph.successors(rnode))
            # filterout all mapped neighbors among 'rnode_out_neighbrs'
            r_mapped_out_neighbr = Utils.filterMappedNeighbrs(rnode_out_neighbrs, rgraph_visit_dict)
            # for every 'l_mapped_out_neighbr' node check if it can be found as a pair with
            # any one of the 'r_mapped_out_neighbr' in the seeds_node_pairs
            match_count = 0
            for lneighbr in l_mapped_out_neighbr:
                for rneighbr in r_mapped_out_neighbr:
                    if mapping.has_edge(lneighbr, rneighbr):
                        match_count = match_count + 1

            rnode_out_degree = len(rnode_out_neighbrs)
            match_cnt_normalized = 0;
            if rnode_out_degree > 0:
                match_cnt_normalized = match_count / math.sqrt(rnode_out_degree)
            scores[rnode] = scores[rnode] + match_cnt_normalized

            ### Implementing In-degree
            # find in-degree neighbors of each rnode
            rnode_in_neighbrs = list(rgraph.predecessors(rnode))
            # filterout all mapped neighbors among 'rnode_in_neighbrs'
            r_mapped_in_neighbr = Utils.filterMappedNeighbrs(rnode_in_neighbrs, rgraph_visit_dict)
            # for every 'l_mapped_in_neighbr' node check if it can be found as a pair with
            # any one of the 'r_mapped_in_neighbr' in the seeds_node_pairs
            match_count = 0
            for lneighbr in l_mapped_in_neighbr:
                for rneighbr in r_mapped_in_neighbr:
                    if mapping.has_edge(lneighbr, rneighbr):
                        match_count = match_count + 1

            rnode_in_degree = len(rnode_in_neighbrs)
            match_cnt_normalized = 0;
            if rnode_in_degree > 0:
                match_cnt_normalized = match_count / math.sqrt(rnode_in_degree)
            scores[rnode] = scores[rnode] + match_cnt_normalized

        return scores

    @staticmethod
    def get_similarity_score(lgraph, rgraph, mapping, lnode):
        score = defaultdict(lambda: 0)
        lnode_outgoing_neighbrs = list(lgraph.successors(lnode))
        lnode_incoming_neighbrs = list(lgraph.predecessors(lnode))

        out_neighbr_match_count = 0
        for rnode in rgraph.nodes:
            rnode_outgoing_neighbrs = list(rgraph.successors(rnode))
            for lnode_out_neighbr in lnode_outgoing_neighbrs:
                if lnode_out_neighbr not in mapping: continue
                mapped_rseed_node = mapping[lnode_out_neighbr]
                if mapped_rseed_node and list(mapped_rseed_node)[0] in rnode_outgoing_neighbrs:
                    out_neighbr_match_count = out_neighbr_match_count + 1

            rnode_out_degree = len(rnode_outgoing_neighbrs)
            matching_cnt_normalized = 0;
            if rnode_out_degree > 0:
                matching_cnt_normalized = out_neighbr_match_count / math.sqrt(rnode_out_degree)
            score[rnode] = score[rnode] + matching_cnt_normalized

            rnode_incoming_neighbrs = list(rgraph.predecessors(rnode))

            in_neighbr_match_count = 0
            for lnode_in_neighbr in lnode_incoming_neighbrs:
                if lnode_in_neighbr not in mapping: continue
                mapped_rseed_node = mapping[lnode_in_neighbr]
                if mapped_rseed_node and list(mapped_rseed_node)[0] in rnode_incoming_neighbrs:
                    in_neighbr_match_count = in_neighbr_match_count + 1

            rnode_in_degree = len(rnode_incoming_neighbrs)
            matching_cnt_normalized = 0;
            if rnode_in_degree > 0:
                matching_cnt_normalized = in_neighbr_match_count / math.sqrt(rnode_in_degree)
            score[rnode] = score[rnode] + matching_cnt_normalized
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

    @staticmethod
    def populate_visit_dict(visit_dict, graph, mapping):
        if graph is None or graph.nodes is None: return
        for node in graph.nodes:
            if node in mapping:
                visit_dict[node] = True;
            else:
                visit_dict[node] = False;

    @staticmethod
    def filterMappedNeighbrs(neighbrs, visit_dict):
        filtered_neighbrs = []
        for n in neighbrs:
            if visit_dict[n]:
                filtered_neighbrs.append(n)
        return filtered_neighbrs