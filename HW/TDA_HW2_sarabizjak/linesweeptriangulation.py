import matplotlib.pyplot as plt
import random
from shapely.geometry import Point, Polygon, MultiPoint, LineString
from matplotlib import pyplot
from descartes.patch import PolygonPatch

def triangulate(S, vertical = True):
    """
    Input: Cloud of points S
    Output:
            E : list of edges
            T : triangles obtained by the line sweep algorithm
    """

    # copy for plotting:
    S = generify(S)
    Points = S

    # points in order depending on verical or horizontal... 
    if vertical == False:
        S = [(s[1], s[0]) for s in S]
    S = sorted(S)
    print(S)

    # make empty lists for output
    E = []
    T = []
    # dict for neigh... tracking
    dictio = {}
    dictio[S[0]] = []
    
    checked = [S[0]]

    for A in S[1:]:
        new_edges = []
        for B in checked:
            counter = 0
            intersection = False
            while counter < len(E) and not intersection:
                line1 = LineString(E[counter])
                line2 = LineString([B, A])
                if line1.crosses(line2):
                    intersection = True
                else:
                    intersection = False
                #print("INTER: " + str(inter))
                #print("E: " + str(E[counter]))
                counter += 1

            # ce se ne seka, dodamo rob...
            if intersection == False:
                new_edges.append(B)
                E.append((B, A))
                if A not in dictio:
                    dictio[A] = []
                if B not in dictio:
                    dictio[B] = []
                dictio[A].append(B)
                dictio[B].append(A)

        checked.append(A)
        #print("new edges: " + str(new_edges))
        #print("dict: " + str(dictio))
        #print("checked: " + str(checked))
        
        # Dodamo trikotnike
        new_triangles = []
        for edge in new_edges:
            #print("edge: " + str(edge))
            for neigh in dictio[edge]:
                #print("neigh: " + str(neigh))
                if neigh in new_edges and sorted([neigh, edge]) not in new_triangles:
                    #print("IM HERE")
                    new_triangles.append(sorted([edge, neigh]))
                    T.append((edge, neigh, A))
                    #print("T1: " + str(T))

        #print("T2: " + str(T))
    
    # Preverimo, ce je katera od zacetnih tock v trikotniku

    for triangle in T:
        count = 0
        inside = False
        while count < len(S) and not inside:
            P = Polygon(triangle)
            p = Point(S[count])
            if p.within(P) and not S[count] in triangle:
                inside = True
            else:
                inside = False
            count += 1
        if inside == True:
            #print("REMOVE")
            T.remove(triangle)

        
    # zamenjamo, ce potrebno, odvisno od zacetnih pogojev
    if vertical == False:
        E = [((e[0][1], e[0][0]), (e[1][1], e[1][0])) for e in E]
        T = [((t[0][1], t[0][0]), (t[1][1], t[1][0]), (t[2][1], t[2][0])) for t in T]

    # Plot
    
    for e in E:
        plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color = 'k', linestyle = '-', linewidth = 1.0)

    for s in Points:
        plt.plot(s[0], s[1], marker = ".", markersize = 5, color = "k")
            
    plt.show()
    
    return E, T               

                     
#S = [(0, 0), (3, 9), (5, -1), (9, 4), (7, -5)]

# Generate 100 points ...

#S = [(random.uniform(0, 20), random.uniform(0, 20)) for _ in range(100)]
#E, T = triangulate(S)    
    
#for e in E:
#    plt.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color = 'k', linestyle = '-')
#plt.show()

def generify(S):
    return [(s[0] + random.uniform(-0.1, 0.1), s[1] + random.uniform(-0.1, 0.1)) for s in S]
