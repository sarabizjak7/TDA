### FUNCTIONS FOR TASK: shelling disks ###

def makeDictGraph(T):
    """
    Returns the dict of form {t = {t1, t2, ...},...} where t is the index of tringle connected to triangles
    with indexes t1, t2,...
    """

    triangles = {}
    graph = {}

    for idx, triangle in enumerate(T):
        triangles[idx] = triangle

    # make a graph with indexes
    for index in triangles:
        graph[index] = set()

    # look for neighbours
    for i in range(len(triangles)):
        #print(i)
        t1, t2, t3 = triangles[i]

        for j in range (i + 1, len(triangles)):
            if t1 in triangles[j]:
                if t2 in triangles[j]:
                    #print("IM HERE1")
                    graph[i].add(j)
                    graph[j].add(i)
            if t2 in triangles[j]:
                if t3 in triangles[j]:
                    #print("IM HERE2")
                    graph[i].add(j)
                    graph[j].add(i)
            if t3 in triangles[j]:
                if t1 in triangles[j]:
                    #print("IM HERE3")
                    graph[i].add(j)
                    graph[j].add(i)

    # Outside ...
    graph[len(T)] = set()

    for key in graph:
        if len(graph[key]) < 3:
            graph[key].add(len(T))
            graph[len(T)].add(key)
            
    return graph



def dfs(graph, start):
    """
    Returns a set with all vertexes in a component with vertex start.
    """
    visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited


def numberOfComponents(T):
    """
    Returns the number of components in a graph.
    """
    graph = makeDictGraph(T)
    components = []
    for idx, triangle in enumerate(T):
        comp = dfs(graph, idx)
        components.append(list(comp))

    unique = []
    for element in components:
        el = sorted(element)
        if el not in unique:
            unique.append(el)

    return len(unique)


def G_minus_t(G, t):
    """
    Returns G - t
    """

    # remove the vertex
    G = del G[t]

    # remove the connections
    for key in G:
        if t in G[key]:
            G[key].remove(t)
            
    return G



