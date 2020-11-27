import math

class Utils:

    def __init__(self):
        self.lgraph = []  #left graph, typically the target graph, here its G1
        self.rgraph = []  #right graph, typically the auxiliary graph, here its G2
        self.mapping = False  # given seed nodes

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

