
class Hungarian(object):
    # reference: https://comzyh.com/blog/archives/148/
    @staticmethod
    def isMatched(left, rights, edges, searched, matching):
        for right in rights:
            if right not in searched and (left,right) in edges:
                searched.add(right)
                if right not in matching or Hungarian.isMatched(matching[right], rights, edges, searched, matching):
                    matching[right] = left
                    return True
        return False

    @staticmethod
    def maximumPartition(lefts, rights, edges):
        # return the matching pattern. use len to get size.
        # edges: (left, right) from left to right
        # O(V*E)
        assert(type(edges) is set)
        matching = {}
        for left in lefts: Hungarian.isMatched(left, rights, edges, set(), matching) # don't care about output
        return matching

    # reference: https://www.slideshare.net/binnasser2007/kuhn-munkres-algorithm
    def maximumWeightPerfectMatching(cost_matrix):
        assert(False),"not implemented"
        # seems complicated and prone to bugs. Should use munkres library instead of implementing myself in real life

if __name__=="__main__":
    print("===== Testing maximum Partition =====")
    lefts = ["A","B","C","D","E"]
    rights = [1,2,3,4,5]
    edges = set([("A",2),("A",5),("B",2),("B",3),("B",4),("C",1),("C",5),("D",1),("D",2),("D",5),("E",2)])
    print(Hungarian.maximumPartition(lefts,rights,edges))

