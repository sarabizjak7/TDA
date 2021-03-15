import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def cliques1(V, E):
    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)
    return list(map(tuple, list(nx.enumerate_all_cliques(G))))

def degrees(V,E):
    degrees_dict = {}
    for v in V:
        degrees_dict[v] = 0
    for (u,v) in E:
        degrees_dict[u] += 1
        degrees_dict[v] += 1
    return degrees_dict

def isClique(c, E):
    # preveri, če so vse povezave vozlišč iz c v E
    pairs = combinations(c, 2)
    for (u,v) in pairs:
        if (u,v) not in E and (v,u) not in E:
            return False
    return True

def cliques_k(V_k, k, E):
    # za vozlišča stopnje k najde vse (k+1)-klike, ki jih tvorijo
    if len(V_k) < k+1:
        return None
    combs = combinations(V_k, k+1)
    cliques_k_list = []
    for comb in combs:
        if isClique(comb, E):
            cliques_k_list.append(tuple(sorted(comb)))
    return cliques_k_list

def cliques(V,E):
    E = set(E)
    degrees_dict = degrees(V,E)
    groups = {}
    groups[0] = []
    for v in degrees_dict:
        if degrees_dict[v] in groups:
            groups[degrees_dict[v]].append(v)
        else:
            groups[degrees_dict[v]] = [v]
    cliques_list = []
    for k in range(max(groups.keys())+1):
        V_k = []
        for l in groups:
            if l >= k:
                V_k += groups[l]
        c_k = cliques_k(V_k, k, E)
        if c_k:
            cliques_list += sorted(c_k)
    return cliques_list

def VR(S, epsilon):
    n = len(S)
    E = []
    for i in range(n):
        for j in range(i+1,n):
            d = np.sqrt((S[i][0] - S[j][0]) ** 2 + (S[i][1] - S[j][1]) ** 2)
            if d <= epsilon:
                E.append((i,j))
    rips = cliques(list(range(n)),E)
    rips_dims = {}
    for c in rips:
        if len(c)-1 in rips_dims:
            rips_dims[len(c)-1].append(tuple(c))
        else:
            rips_dims[len(c)-1] = [tuple(c)]
    return rips_dims

import timeit

# Pod 1 sekundo (~0.5 s)
if False:
    V = list(range(17))
    E = list(combinations(V,2))
    print(timeit.timeit("cliques(V,E)",globals=globals(), number=1))

# Pod 10 sekundami (~6 s)
if False:
    V = list(range(20))
    E = list(combinations(V,2))
    print(timeit.timeit("cliques(V,E)",globals=globals(), number=1))

# Pod 100 sekundami (~69 s)
if False:
    V = list(range(23))
    E = list(combinations(V,2))
    print(timeit.timeit("cliques(V,E)",globals=globals(), number=1))

# 1. test z vaj (naloga 28)
if False:
    S = [(0,0),(0.5,0.5),(0,1),(1,2),(1.5,1.5),(2,1.5),(2.5,1),(2,0)]
    for r in [1,1.2,1.75]:
        print()
        print('epsilon:',r)
        rips = VR(S,r)
        for k in rips:
            print('dim:',k)
            print(rips[k])

# 2. test z vaj (naloga 31)
if False:
    S = [(0,0),(1,1),(-2,3),(2,3),(4,2),(3,-1)]
    for r in [2.4,4.1]:
        print()
        print('epsilon:',r)
        rips = VR(S,r)
        for k in rips:
            print('dim:',k)
            print(rips[k])

# test za cliques
if False:
    np.random.seed(2)
    n = 20
    for _ in range(20):
        S = [i for i in range(n)]
        E = []
        for e in combinations(S,2):
            if np.random.random() > 0.5:
                E.append(e)
        print(cliques(S,E) == cliques1(S,E))