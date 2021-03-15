### PART 2 ###

from shapely.geometry import LineString

def does_intersect1(A, B, C, D):
    """
    Returns wether line segments with endpoint A, B and C, D intersect.
    Points are given as (x, y).
    """
    line1 = LineString([A, B])
    line2 = LineString([C, D])
    return line1.intersects(line2)
