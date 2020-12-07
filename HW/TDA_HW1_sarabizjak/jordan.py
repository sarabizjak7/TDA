
from shapely.geometry import Point, Polygon

def insideQ(P, T):
    """
    Returns True if the point T lies inside the polygonal curve P and False orherwise.
    """
    T = Point(T)
    P = Polygon(P)

    return T.within(P)
 



def inside(P, T):
    # https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    
    n = len(P)
    inside = False

    p1x, p1y = P[0]
    for i in range(n + 1):
        p2x, p2y = P[i % n]
        if T[1] > min(p1y, p2y):
            if T[1] <= max(p1y, p2y):
                if T[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (T[1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or T[0] <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside



