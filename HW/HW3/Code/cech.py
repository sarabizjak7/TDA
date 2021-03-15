from numpy.linalg import norm
from numpy import array
import itertools
import timeit
import random
import networkx as nx
from networkx.algorithms.clique import find_cliques
import miniball

from rips import cliques, VR

def cech(S, epsilon):
    """
    Returns a dictionary where keys are the dimensions of simplices in the Čech complex 
    and values are lists of all simplices of corresponding dimension.
    """
    VRips = VR(S, 4 * epsilon)

    C_complex = {}
    # For zero and one dim is the same as VR complex
    C_complex[0] = VRips[0]
    C_complex[1] = VRips[1]

    # Miniball:
    

    return C_complex