 
class BinaryIndexedTree(object):

    def __init__(self, lst): # build a zero BIT
        if type(lst) is int:
            self.tree = [0] * (lst + 1)  # 0 is not used
            self.size = len(self.tree) - 1
        else:
            self.tree = [0] * (len(lst) + 1)  # 0 is not used
            self.size = len(self.tree) - 1
            self.init(lst)


    def init(self, iterator): # O(n log n) init
        assert(len(iterator)==self.size),"size mismatch"
        for i, it in enumerate(iterator):
            self[i] = it

    def _get_sum(self, idx):
        sum = 0
        while idx > 0:
            sum += self.tree[idx]
            idx -= idx & -idx # get rid of last-1-bit
        return sum

    def _range_sum(self, begin, end):
        return self._get_sum(end) - self._get_sum(begin)

    def __setitem__(self, idx, val): # O(log n)
        assert(0<=idx<self.size),("index out of range",idx)
        diff = val - self[idx]
        idx+=1 # convert idx, start from
        while idx <= self.size:
            self.tree[idx] += diff
            idx += idx & -idx

    def __getitem__(self, key): #O(log n)
        if isinstance(key, slice):
            assert(key.step is None), "does not support slicing"
            start = 0 if key.start is None else key.start
            stop = self.size if key.stop is None else key.stop
            if stop < 0: stop+=self.size
            return self._range_sum(start, stop)
        return self._range_sum(key, key+1)

    def __repr__(self): # O(n log n)
        return str([self[i] for i in range(self.size)])

if __name__=="__main__":
    lst = [1,2,3,4,5,6,7,8]
    bit =BinaryIndexedTree(8)
    print(bit)
    bit.init(lst)
    print(bit)
    print(bit[2:4])
    bit[2]=-5
    print(bit[2])
    bit[7]=2
    print(bit)
    print(bit[2:-1])