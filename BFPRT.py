class BFPRT(object):
    @staticmethod
    def getKthSmallest(lst, k, c=5, min_size=16):  # O(n) in space/time
        assert (0 <= k < len(lst)), ("out of bound", k, len(lst))
        while True:  # O(n)+O(n/2)+O(n/4)+...=O(n)
            if len(lst) <= min_size:
                return sorted(lst)[k]
            median = BFPRT._roughMedian(lst, c)
            median_idx = sum(1 for e in lst if e < median)
            # print("median_value {}, median index is {}, percentile {}".format(median, median_idx, median_idx/len(lst)))
            if k == median_idx:
                return median
            elif k < median_idx:
                lst = [e for e in lst if e < median]
                continue
            else:  # k > median_idx:
                lst = [e for e in lst if median < e]
                k -= (median_idx + 1)
                continue

    @staticmethod
    def _roughMedian(lst, c=5):  # O(n) in time/space, assert return value between 30%-70% of data under c = 5, so we have linearity
        while True:
            if len(lst) < c * c:  # to avoid dealing with corner case(like when len(lst)==2) that may break the assertion
                return sorted(lst)[len(lst) // 2]
            new_lst = []
            for begin in range(0, len(lst), c):
                end = min(begin + c, len(lst))
                new_lst.append(sorted(lst[begin:end])[(end - begin) // 2])
            lst = new_lst

if __name__ == "__main__":
    import random
    random.seed(42)
    inp = list(range(10000))
    random.shuffle(inp)
    print(BFPRT.getKthSmallest(inp, 3332))
