
### FUNCTIONS FOR TASK: deciding connectivity ###

def makeDictGraph(V, E):
    """
    Returns the dict of form {v: {v1, v2},...} where vertex v is connected to v1 and v2.
    """
    graph = {}
    for v in V:
        for e in E:
            if v in e:
                a, b = e
                if v != a:
                    if v in graph:
                        graph[v].add(a)
                    else:
                        graph[v] = set([a])
                else:
                    if v in graph:
                        graph[v].add(b)
                    else:
                        graph[v] = set([b])
        if v not in graph:
            graph[v] = set()
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
        

def findComponents(V, E):
    """
    Returns all components in a graph.
    """
    graph = makeDictGraph(V, E)
    components = []
    for v in V:
        comp = dfs(graph, v)
        components.append(list(comp))

    unique = []
    for element in components:
        el = sorted(element)
        if el not in unique:
            unique.append(el)

    return unique
        
        
