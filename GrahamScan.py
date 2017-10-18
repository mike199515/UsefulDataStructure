import math


class GranhamScan(object):
    @staticmethod
    def _toPolar(x, y):  # get r, theta from x, y
        return math.sqrt(x * x + y * y), math.atan2(y, x)

    @staticmethod
    def _isNoneLeftTurn(p0, p1, p2):
        x0, y0 = p0
        x1, y1 = p1
        x2, y2 = p2
        cross_prod = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        return cross_prod <= 0

    @staticmethod
    def convexHull(points):  # tuple-like 2d points, O(n log n) for points
        if len(points) == 0: return []
        p0 = min(points, key=lambda t: (t[1], t[0]))
        new_points = []
        for i, p in enumerate(points):
            if p == p0:
                stack = [(i, p)]
            else:
                r, theta = GranhamScan._toPolar(p[0] - p0[0], p[1] - p0[1])
                new_points.append(((theta, r), i, p))
        new_points.sort()
        for c, (_, i, p) in enumerate(new_points):
            while len(stack) >= 2 and GranhamScan._isNoneLeftTurn(stack[-2][1], stack[-1][1], p):
                x = stack.pop()
                # print("pop {}".format(x))
            stack.append((i, p))
            # print("append {}".format(stack[-1]))
        return [points[i] for i, _ in stack]

    @staticmethod
    def convexHullWithEdges(points):  # some naive O(n^2) implementation, including all points on edges
        hulls = GranhamScan.convexHull(points)
        equations = []
        for i in range(len(hulls)):
            x0, y0 = hulls[i]
            x1, y1 = hulls[(i + 1) % len(hulls)]
            equations.append((x0, x1, y0, y1))
        return [p for p in points if
                any(abs((y1 - y0) * (p[0] - x0) - (x1 - x0) * (p[1] - y0)) < 1e-12 for x0, x1, y0, y1 in equations)]


if __name__ == "__main__":
    points = [[3, 0], [4, 0], [5, 0], [6, 1], [7, 2], [7, 3], [7, 4], [6, 5], [5, 5], [4, 5], [3, 5], [2, 5], [1, 4],
              [1, 3], [1, 2], [2, 1], [4, 2], [0, 3]]
    print(GranhamScan.convexHull(points))
    print(GranhamScan.convexHullWithEdges(points))
    points = [[1, 2], [2, 2], [4, 2]]
    print(GranhamScan.convexHull(points))
    print(GranhamScan.convexHullWithEdges(points))