import math

class SegmentTree(object):
    # immutable segment tree for range search. Implemented by light weighted list

    # support [0, size) index
    # node 0 is root. for left, *2, for right *2+1. for parent, //2.
    def __init__(self, size, reducer = None, init_val = 0):
        if reducer is None: reducer = lambda x,y: x+y
        self.size=size
        self.reducer = reducer
        self.depth =int(math.ceil(math.log(size)/math.log(2))) + 1
        self.vals = [init_val] * (1<<self.depth)
        self.ranges = [None] * (1<<self.depth)
        self._gen_range(1,(0, len(self.vals)//2))

    def __len__(self):
        return self.size

    def _gen_range(self, node, range):
        self.ranges[node]=range
        if node * 2 < len(self.vals):
            mid = (range[0] + range[1]) // 2
            self._gen_range(node * 2, (range[0], mid))
            self._gen_range(node * 2+1, (mid, range[1]))

    def _get_node(self, idx):
        # O(1)
        assert(0<= idx < self.size)
        return idx + len(self.vals)//2

    def __setitem__(self, idx, value): # O(log n)
        node_id = self._get_node(idx)
        self.vals[node_id] = value
        while True:
            if node_id == 1: break
            node_id //= 2
            self.vals[node_id] = self.reducer(self.vals[node_id*2], self.vals[node_id*2+1])

    def __getitem__(self, idx): # O(1)
        node_id = self._get_node(idx)
        return self.vals[node_id]

    def reduce_range(self, begin, end):
        assert (0 <= begin < end <= self.size)
        return self._reduce_range(begin, end, 1)

    def _reduce_range(self, begin, end, node):
        # get ranged result with certain op, O(log n) time/space
        r_begin, r_end = self.ranges[node]
        #print("@get_range[{},{}) in [{},{})".format(begin, end, r_begin,r_end))
        assert(r_begin <= begin < end <= r_end)
        # speed-up case , if it is full
        if r_begin == begin and r_end ==end: return self.vals[node]
        r_mid = ( r_begin + r_end ) // 2
        # one sided_case
        if end <= r_mid: return self._reduce_range(begin, end, node*2)
        if begin >= r_mid: return self._reduce_range(begin, end, node*2+1)
        # we have begin < r_mid < end
        return self.reducer(self._reduce_range(begin,r_mid,node*2), self._reduce_range(r_mid,end,node*2+1))

    def __repr__(self):
        return str(list(zip(self.vals,self.ranges)))

if __name__=="__main__":
    tree=SegmentTree(20, reducer = max)
    for i in range(20):
        tree[i]=i
    tree[0]=20
    print(tree, len(tree))
    print(tree.reduce_range(6,15))