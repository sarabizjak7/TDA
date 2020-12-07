from delauney import *
from linesweeptriangulation import *

S = [(random.uniform(0, 20), random.uniform(0, 20), random.uniform(0, 20)) for _ in range(100)]

_, T = triangulate(S)
optimize(T)
