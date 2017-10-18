class KMP(object):
    @staticmethod
    def findFirst(pattern, text):  # return the first index of pattern found in text ,else -1
        p_idx = 0
        t_idx = 0
        lps = KMP._LPS(pattern)
        while t_idx < len(text):
            if pattern[p_idx] == text[t_idx]:
                p_idx += 1
                t_idx += 1
            if p_idx == len(pattern):
                return t_idx - p_idx
            elif t_idx < len(text) and pattern[p_idx] != text[t_idx]:
                if p_idx != 0:
                    p_idx = lps[p_idx - 1]
                else:
                    t_idx += 1
        return -1

    @staticmethod
    def findAll(pattern, text):  # return the indexs of pattern found in text
        ret = []
        p_idx = 0
        t_idx = 0
        lps = KMP._LPS(pattern)
        while t_idx < len(text):
            if pattern[p_idx] == text[t_idx]:
                p_idx += 1
                t_idx += 1
            if p_idx == len(pattern):
                ret.append(t_idx - p_idx)
                p_idx = lps[p_idx - 1]
            elif t_idx < len(text) and pattern[p_idx] != text[t_idx]:
                if p_idx != 0:
                    p_idx = lps[p_idx - 1]
                else:
                    t_idx += 1
        return ret

    @staticmethod
    def _LPS(pattern):
        # lps[i] = the longest proper prefix of pat[0..i] which is also a suffix of pat[0..i].
        prev_len = 0  # length of previous longest prefix suffix
        ret = [0] * len(pattern)
        idx = 1  # lps[0] is 0
        while idx < len(pattern):
            if pattern[idx] == pattern[prev_len]:
                prev_len += 1
                ret[idx] = prev_len
                idx += 1
            else:
                if prev_len != 0:
                    prev_len = ret[prev_len - 1]
                else:
                    ret[idx] = 0
                    idx += 1
        return ret


if __name__ == "__main__":
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    print(KMP._LPS(pattern))
    print(KMP.findAll(pattern, text))
