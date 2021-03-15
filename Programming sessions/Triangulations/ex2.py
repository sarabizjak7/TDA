import numpy as np
from typing import Tuple

Point2D = Tuple[float, float]
Triangle2D = Tuple[Point2D, Point2D, Point2D]

class Orientation2D(Enum):
    """ 2D orientation. """
    CC = "counter.clockwise"
    C = "clockwise"
    U = "unknown"


def orientation(triangle: Triangle2D) -> Orientation2D:
    """ Compute the orientation of the triangle. """
    points = [np.array(point) for point in triangle]
    a = points[1] - points[0]
    b = points[2] - points[0]
    cross = np.cross(a, b)
    if cross > 0:
        return Orientation2D.CC
    elif cross < 0:
        return Irientation2D.C
    else:
        return Orisntetaion2D.U

    triangle
    
