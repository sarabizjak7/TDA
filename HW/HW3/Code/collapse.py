import itertools

def free_faces(d, dim):
    """
    Finds free faces 
    """
    faces = []
    faces_pt = []
    for i in range(dim, -1, -1):
        for idx, simplex in enumerate(d[i]):
            #print("idx: " + str(idx))
            #print("simplex: " + str(simplex))
            if len(simplex[1]) == 1:
                faces.append((d[i + 1][simplex[1][0]][0], simplex[0], simplex[1][0], idx,))
                faces_pt.append((d[i + 1][simplex[1][0]][0], simplex[0]))
    return faces, faces_pt


def max_vertex(X):
    """
    Finds max vertex in a simplex X
    """
    maks = 0
    for x in X:
        for vertex in x:
            if vertex > maks:
                maks = vertex
    return maks


def get_simplices(X, max_dim):
    """
    Returns a dict with all simplices
    """
    # Prepare dict
    simplices = {}
    for i in range(1, max_dim):
        simplices[i] = []
    for x in X:
        for i in range(2, len(x) + 1):
            for l in list(itertools.combinations(x, i)):
                if l not in simplices[i - 1]:
                    simplices[i - 1].append(l)
    return simplices

    
def collapse(X, progress = True):
    """
    Returns the list of all simplices that are left after all possible collapses have been made.
    """
    
    #### PRINTING ####
    if progress == True:
        print("Initial simplicial complex:")
        print(X)
        print(" ")
    ##################

    X_remaining = X

    # Dict of all simplices

    max_dim = max([len(x) for x in X])
    max_v = max_vertex(X)
    simplices = get_simplices(X, max_dim)
    simplices[0] = [(i + 1,) for i in range(max_v)]

    #print(simplices)
    
    # Prepare data...
    h = {max_dim - 1: [[x, [], []] for x in simplices[max_dim - 1]]}
    for i in range(0, max_dim - 1):
        h[i] = []
    for i in range(max_dim - 2, -1, -1):
        for idx1, scx1 in enumerate(simplices[i]):
            #print("idx1: " + str(idx1))
            #print("scx1: " + str(scx1))
            h[i].append([scx1, [], []])
            for idx2, scx2 in enumerate(simplices[i + 1]):
                #print("idx2: " + str(idx2))
                #print("scx2: " + str(scx2))
                sub = True
                for el in scx1:
                    #print("el: " + str(el))
                    #print("[0]: " + str(scx2[0]))
                    if el not in scx2:
                        sub = False
                if sub == True:
                    h[i + 1][idx2][2].append(idx1)
                    h[i][idx1][1].append(idx2)

    collaps = True
    col_dim = max_dim - 2

    while collaps == True:
        faces, faces_pt = free_faces(h, col_dim)

        #### PRINTING ####
        if progress == True:
                print('Free faces:')
                print(faces_pt)
        else:
            continue
        ##################

        if faces:
            [sigma, tau, sigma_idx, tau_idx] = faces.pop(0)
            faces_pt.pop(0)

            #### PRINTING ####
            if progress == True:
                print("Choose a simplex sigma with a free face tau:")
                print('sigma = ' + str(sigma))
                print('tau = ' + str(tau))
            else:
                continue
            ##################

            col_dim = len(sigma) - 2

            if col_dim > -15:

                repair_h = [(col_dim, sigma_idx, i) for i in h[col_dim + 1][sigma_idx][2]]

                h[col_dim + 1][sigma_idx][1] = []
                h[col_dim + 1][sigma_idx][2] = [] 

                for r in repair_h:
                    [dim, idx_plus, idx_org] = r
                    h[dim][idx_org][1].remove(idx_plus)

                repair_h = [(col_dim - 1, tau_idx, i) for i in h[col_dim][tau_idx][2]]

                h[col_dim][tau_idx][1] = []
                h[col_dim][tau_idx][2] = []

                for r in repair_h:
                     [dim, idx_plus, idx_org] = r
                     h[dim][idx_org][1].remove(idx_plus)   

                if sigma in X:
                    X_remaining.remove(sigma)

                    #### PRINTING ####
                    if progress == True:
                        print("Remaining simplices after the elementary collapse:")
                        print(X_remaining)
                        print(" ")
                    else:
                        continue
                    ##################

                else:
                    continue
                
            else:
                collaps = False
        else:
            collaps = False

        complex = []
        for dim in h:
            for scx in h[dim]:
                if not (not scx[1] and not scx[2]):
                    complex.append(scx[0])
    if not complex:
        complex = [(tau,)]
    print(" ")
    print("END: ")
    print(complex)
