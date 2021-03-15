from numpy.linalg import norm
from numpy import array
import numpy as np
import itertools
import timeit
import random
import networkx as nx
from networkx.algorithms.clique import find_cliques, enumerate_all_cliques

def cliques(VG, EG):
    """
    Finds all cliques in a graph

    Input:      VG: list of vertices
                EG: list of edges
    Output:     List with lists of edges in cliques
    """

    G = nx.Graph()
    for node in VG:
        G.add_node(node)
    for edge in EG:
        G.add_edge(*edge)
    return list(nx.enumerate_all_cliques(G))

def VR(S, epsilon):
    """
    Returns a dictionary where keys are the dimensions of simplices in the VR complex
    and values are lists of all simplices of corresponding dimension.
    """
    start_time = timeit.default_timer()

    # Index the vertices and connect the ones that are <= epsilon away -- simplexes of dim 0 and 1
    # 0:
    zero_dim = [(idx,) for idx in range(len(S))]
    indexes = [idx for idx in range(len(S))]
    #print("zero_dim: " + str(zero_dim))

    # 1:
    one_dim = []
    for idx_1, s_el_1 in enumerate(S):
        for idx_2, s_el_2 in enumerate(S):
            if idx_1 < idx_2 and norm(array([s_el_1[0], s_el_1[1]]) - array([s_el_2[0], s_el_2[1]])) <= epsilon:
                one_dim.append((idx_1, idx_2))
    #print("one_dim: " + str(one_dim))

    cliques_start = timeit.default_timer()
    # extract the simplexes with higher dimensions (which not in zero and one dimension) from function cliques
    cliqs = cliques(indexes, one_dim)
    cliques_end = timeit.default_timer()

    higher_dimensions = []
    
    #print("cliqs: " + str(cliqs))

    for element in cliqs:
        new_element = tuple(sorted(element))
        if new_element not in zero_dim:
            if new_element not in one_dim: 
                higher_dimensions.append(new_element)
    higher_dims = {}
    #print("higher dim: "  + str(higher_dimensions))

    # -- Prepare the output dictionary -- #

    # find the highest dimension of a simplex
    highest_dim = 1
    for element in higher_dimensions:
        dim = len(element) - 1
        if dim > highest_dim:
            highest_dim = dim

    VR_complex = {}
    VR_complex[0] = zero_dim
    VR_complex[1] = one_dim

    for i in range(2, highest_dim + 1):
        VR_complex[i] = []
        for element in higher_dimensions:
            if len(element) - 1 == i:
                VR_complex[i].append(element)

    end_time = timeit.default_timer()

    print("cliques: " + str(cliques_end - cliques_start))
    print("algorithm: " + str(end_time - start_time))
    print("...")
    return VR_complex


def generate_S():
    
    for s in [5, 10, 15, 20, 21, 22]:
        S = []
        for i in range(s):
            S.append((random.random()*10,random.random()*10))

        #or epsilon in range(10):
            #VR(S, epsilon)
        print("Number of vertices: " + str(s))
        VR(S, 15)

generate_S()



