import random
from math import sin, cos, pi, asin, sqrt, pow


class geo:
    @staticmethod
    def polyhedron(r, n):
        from math import cos, sin, pi

        vertices = []
        for i in range(n, 0, -1):
            random.seed(n * random.random() * 10000)
            r_new = r + random.random() * 4
            vertices.append((r_new * sin(2 * i * pi / n), r_new * cos(2 * i * pi / n)))
        return vertices

    @staticmethod
    def center(pt1, pt2):
        return (max((pt1[0], pt2[0])) - min((pt1[0], pt2[0]))) / 2 + min((pt1[0], pt2[0])), \
               (max((pt1[1], pt2[1])) - min((pt1[1], pt2[1]))) / 2 + min((pt1[1], pt2[1]))

    @staticmethod
    def additive(alpha, pt, add):
        dx = pt[0] + cos(2 * pi - alpha) * add[0] + sin(2 * pi - alpha) * add[1]
        dy = pt[1] + cos(2 * pi - alpha) * add[1] - sin(2 * pi - alpha) * add[0]
        return dx, dy

    @staticmethod
    def alpha(pt, A):
        if A == (0.0, 0.0):
            return 0
        else:
            A = (A[0] - pt[0], A[1] - pt[1])
            return asin(geo.length((0, A[1]), A) / geo.length(A, (0, 0)))

    @staticmethod
    def length(pt1, pt2):
        return sqrt(pow(pt2[0] - pt1[0], 2) + pow(pt2[1] - pt1[1], 2))

    @staticmethod
    def angle_to_centre(centre, q, pt):
        _alpha = geo.alpha(centre, pt)
        if q == 1:
            return pi + _alpha
        elif q == 2:
            return 2 * pi - _alpha
        elif q == 3:
            return _alpha
        elif q == 4:
            return pi - _alpha

    @staticmethod
    def to_centre(centre, pt):
        c = geo.length((0, 0), pt)
        _alpha = geo.alpha(centre, pt)
        _betha = pi / 2 - _alpha
        return c * sin(_alpha), c * sin(_betha)

    @staticmethod
    def quarter(centre, pt):
        pt = (pt[0] - centre[0], pt[1] - centre[1])
        if pt[0] > 0:
            if pt[1] > 0:
                return 1
            else:
                return 2
        else:
            if pt[1] > 0:
                return 4
            else:
                return 3

    @staticmethod
    def quarter_direction(pt1, pt2):
        q = geo.quarter(pt1, pt2)
        if q == 1:
            return 1, 1
        elif q == 2:
            return 1, -1
        elif q == 3:
            return -1, -1
        elif q == 4:
            return -1, 1