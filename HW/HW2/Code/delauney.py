import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random
from shapely.geometry import Point, Polygon, MultiPoint, LineString
from shapely.ops import triangulate
from matplotlib import pyplot
from descartes.patch import PolygonPatch
from scipy.spatial import Delaunay
import shapely.wkt
#from linesweeptriangulation import generify


def optimize(T):
    """
    Input: any triangulation T
    Output: Delauney triangulation of points
    """

    points = []

    for triangle in T:
        for point in triangle:
            if point not in points:
                points.append(point)

    #points = generify(points)
    P = MultiPoint(points)
    triangles = triangulate(P)

    # output:
    output = []
    for t in triangles:
        k = shapely.wkt.loads(t.wkt)
        triang = list(zip(*k.exterior.coords.xy))
        unique = set()
        for point in triang:
            if point not in unique:
                unique.add(point)
        output.append(tuple(unique))

    # Uncomment for plotting

    """
    fig = pyplot.figure(1, figsize=(10, 10), dpi= 90)
    ax = fig.add_subplot(111)

    for triangle in triangles:
        #patch = PolygonPatch(triangle, alpha = 0.5, zorder = 2, linewidth = 1.0, color = "y")
        ax.add_patch(patch)

    for point in P:
        pyplot.plot(point.x, point.y, '.', markersize = 5, color = "k")


    pyplot.show()
    """
    
    return output
    

