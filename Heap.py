class MinHeap(object):
    # reference: http://www.cse.hut.fi/en/research/SVG/TRAKLA2/tutorials/heap_tutorial/index.html
    def __init__(self, lst=None):
        self.heap = []
        if lst is not None:
            self.buildHeap(lst)

    def fromList(self,
                   lst):  # O(n) as a tighter bound. See http://www.cs.umd.edu/~meesh/351/mount/lectures/lect14-heapsort-analysis-part.pdf
        self.heap = lst
        for i in range(len(self) // 2 - 1, -1, -1):
            self._heapify(i)

    def push(self, key):  # O(log n)
        self.heap.append(None)
        i = len(self.heap) - 1
        while i > 0 and self.heap[i // 2] > key:
            self.heap[i] = self.heap[i // 2]
            i //= 2
        self.heap[i] = key

    def pop(self):  # O(log n)
        assert (len(self) > 0)
        ret = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify()
        return ret

    def peak(self):  # O(1)
        return self.heap[0]

    def _heapify(self, idx=0):  # Quite obviously O(log n)
        i = idx
        while True:
            l = 2 * i
            r = 2 * i + 1
            smallest = l if l < len(self) and self.heap[l] < self.heap[i] else i
            smallest = r if r < len(self) and self.heap[r] < self.heap[smallest] else smallest
            if smallest == i:
                break
            else:
                self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
                i = smallest

    def __repr__(self):
        return str(self.heap)

    def __len__(self):  # O(1)
        return len(self.heap)

    @staticmethod
    def heapSort(lst):
        h = MinHeap(lst)
        ret = []
        while len(h) > 0: ret.append(h.pop())
        return ret

if __name__ == "__main__":
    print("===== Test heap =====")
    h = MinHeap([7, 8, 8, 123, 2, 34, 4, 3, 5, 2, 1, 6])

    print(h)
    while len(h) > 0:
        print(h.pop())
        print(h)

    print(MinHeap.heapSort([7, 8, 8, 123, 2, 34, 4, 3, 5, 2, 1, 6]))
