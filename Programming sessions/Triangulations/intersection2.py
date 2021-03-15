### PART 3 ###

from shapely.geometry import LineString, Point

def does_intersect2(A, B, C, D):
    """
    Returns the intersection of line segments with endpoint A, B and C, D intersect.
    Points are given as (x, y).
    """
    line1 = LineString([A, B])
    line2 = LineString([C, D])

    intersection = line1.intersection(line2)
    intersection_bool = line1.intersects(line2)
    if intersection_bool == True:
        return print(intersection) 
    else:
        return print("Does not intersect")
