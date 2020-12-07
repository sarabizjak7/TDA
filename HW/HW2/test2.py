import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random


def triangulate(S, vertical):

    if vertical == False:
        S = [(s[1], s[0]) for s in S]

    S = sorted(S)
    checked_pts, E, T, D = [S[0]], [], [], {}
    D[S[0]] = []

    print(S)
    
    # line sweep
    ccc = 0
    for A in S[1:]:
        #print(ccc)
        ccc = ccc + 1
        edges_to_add = []
        for B in checked_pts:
            #print("Points: ", B, A)

            counter, inter = 0, False
            while counter < len(E) and not inter:
                inter = intersect(E[counter], (B, A))
                #print("E: " + str(E[counter]))
                #print("AB: " + str(print(B, A)))
                #if inter == True: print("inter: ", B, A)
                counter = counter + 1

            if inter == False:
                #print("Add edge")
                edges_to_add.append(B),E.append((B,A))
                if not A in D:
                    D[A] = []
                D[A].append(B)
                D[B].append(A)

        checked_pts.append(A)

        print("new edges: " + str(edges_to_add))
        print("dict: " + str(dictio))
        #print("checked: " + str(checked))
        
        T = add_triangles(T, D, edges_to_add, A)
        #print(T)

    T = check_triangles(T,S)

    if vertical == False:
        E = [((e[0][1], e[0][0]), (e[1][1], e[1][0])) for e in E]
        T = [((e[0][1], e[0][0]), (e[1][1], e[1][0]), (e[2][1], e[2][0]))for e in T]

    return E, T

def generify(S):
    return [(s[0]+random.uniform(-0.1, 0.1) ,s[1]+random.uniform(-0.1, 0.1)) for s in S]

def check_triangles(T,S):
    T_new = []
    for triangle in T:
        counter, inside_point = 0, False
        while counter < len(S) and not inside_point:
            inside_point = insideQ(triangle,S[counter]) and not S[counter] in triangle
            counter = counter + 1
        if inside_point == False:
            T_new.append(triangle)
    return T_new

def orientation(A,B,C):
    return np.cross((A[0] - B[0], A[1] - B[1]), (C[0] - B[0], C[1] - B[1]))

def intersect(edge_a, edge_c):
    (A,B),(C,D) = edge_a,edge_c
    or1, or2 = orientation(A,B,C), orientation(A,B,D)
    or3, or4 = orientation(C,D,A), orientation(C,D,B)
    return or1*or2 < 0 and or3*or4 <0

def add_triangles(T,D,new_edges,tmp_pt):
    tmp_T = []
    for end_pt in new_edges: #edge = (chk_pt, tmp_pt)
        for neighbour in D[end_pt]:
            if neighbour in new_edges and not sorted([neighbour,end_pt]) in tmp_T:
                tmp_T.append(sorted([end_pt,neighbour]))
                T.append((end_pt,neighbour,tmp_pt))
    return T

def plot_triangulation(P):
    for p in P:
        plt.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], color='k', linestyle='-')
    plt.show()

# jordan

def insideQ(P,T):

    online, counter = 0, 0
    (x,y) = T

    for i in range(len(P)):

        j = (i+1)%len(P)
        x1, x2, y1, y2 = P[i][0], P[j][0], P[i][1], P[j][1]

        if (x1 >= x) and (x2 <= x):
            tmpx, tmpy = x1, y1
            x1, y1 = x2, y2
            x2, y2 = tmpx, tmpy

        if (x1 > x) and (x2 > x):
            if (y - y1) * (y - y2) < 0:
                counter+=1
                online = 0
                #print('normal', counter)
            elif y != y1  and y == y2:
                online = (y - y1)
                #print('special1', counter)
            elif y1 == y and y2 != y:
                if (y2 - y) * online > 0:
                    counter+=1
                    #print('special2', counter)
                online = 0

        elif (x-x1)*(x-x2) <= 0:
            if (y - y1) * (y - y2) <= 0:
                if x1 == x2:
                    return True #'x1==x2'
                yp = ((y2-y1)/(x2-x1))*(x-x1) + y1
                #print(yp,y1,y2)
                if yp == y:
                    return True #'yp == y'
                elif (y2 - y1)*(y - yp) > 0 :
                    counter += 1
                    #print('diagon', counter)

    return (counter%2 == 1)

# testi

def org_test():
    S = [(0, 0), (3, 9), (5, -1), (9, 4), (7, -5)]
    E,T = triangulate(S, False)
    plot_triangulation(E)
    #print(E)
    #print(T)

def generate_sto():
    return [(random.uniform(5,25),random.uniform(5,25)) for _ in range(100)]

def sto_test():
    S = generate_sto()
    E, T = triangulate(S, True)
    plot_triangulation(E)

#sto_test()
#E = [((0, 0), (3, 9)), ((0, 0), (5, -1)), ((3, 9), (5, -1)), ((0, 0), (7, -5)), ((3, 9), (7, -5)), ((5, -1), (7, -5)), ((3, 9), (9, 4)), ((7, -5), (9, 4))]
#T = [((0, 0), (3, 9), (5, -1)), ((0, 0), (5, -1), (7, -5)), ((3, 9), (5, -1), (7, -5)), ((3, 9), (7, -5), (9, 4))]
