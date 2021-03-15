from itertools import chain, combinations
from random import sample
from typing import Optional

# Types
Vertex = int
Simplex = tuple[Vertex, ...]
SimplicialComplex = set[Simplex]
DiscreteGradientVectorField = tuple[dict[Simplex, Simplex], set[Simplex]]


def expand(scx: SimplicialComplex) -> SimplicialComplex:
    """Expand the given simplicial complex.

    That is return the simplicial complex that has all simplices listed
    explicitely. For instance:

    >>> expand({(1, 2, 3)})
    {(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)}
    """
    result: SimplicialComplex = set()
    for top_simplex in scx:
        # Iterate through all the simplices contained in the simplex
        # top_simplex. That is the same as iterating through all the
        # non-empty subsets of the set of points representing the simplex.
        # See https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset
        # for detailed explanation of the method used to generate the subsets.
        #
        # Add the generated simlices to the set result.
        result.update(
            chain.from_iterable(
                combinations(top_simplex, r) for r in range(1, len(top_simplex) + 1)
            )
        )
    return result


def free_faces(scx: SimplicialComplex) -> set[tuple[Simplex, Simplex]]:
    """Get a set of pairs (s, p) in the complex where s is a free face of p."""
    # NOTE: the implementation bellow is very ineficient. When parent/child
    # relations in the complex are computed in advance it could help a lot.
    free_faces: list[tuple[Simplex, Simplex]] = []
    for simplex in scx:
        dimension = len(simplex) - 1
        parents = []
        for possible_parent in scx:
            possible_parent_dimension = len(possible_parent) - 1
            if possible_parent_dimension == dimension + 1:
                if set(simplex).issubset(set(possible_parent)):
                    parents.append(possible_parent)
        if len(parents) == 1:
            # We have a free face
            free_faces.append((simplex, parents[0]))
    return free_faces


def top_simplices(scx: SimplicialComplex) -> set[Simplex]:
    """Get a set of top-dimensional simplices in the complex.

    Return an empty set if the given simplicial complex is empty.
    """
    top_simplices = set()
    top_dimension = 0

    for simplex in scx:
        dimension = len(simplex) - 1
        if dimension > top_dimension:
            top_simplices = {simplex}
            top_dimension = dimension
        elif dimension == top_dimension:
            top_simplices.add(simplex)
    return top_simplices


def random_discrete_gradient_vector_field(
    scx: SimplicialComplex,
) -> DiscreteGradientVectorField:
    expanded_scx = expand(scx)
    # A mapping representing arrows in discrete gradient vector field.
    V: dict[Simplex, Simplex] = dict()
    # A set representing critical simplices in discrete gradient vector field.
    C: set[Simplex] = set()
    # Repeat the procedure bellow until complex is not empty.
    # 1. Find free face s and its parent p.
    # 2. Remove s and p from simplicial complex and add mapping from s to p
    #    into discrete gradient vector field.
    # 3. If there is no free face pick one top-dimensional simplex at random
    #    and remove it from the complex and add it to the list of critical
    #    simplices.
    while expanded_scx:
        collapse_pairs = free_faces(expanded_scx)
        if collapse_pairs:
            # We have a free face.
            collapse_pair = sample(collapse_pairs, 1)[0]
            expanded_scx.remove(collapse_pair[0])
            expanded_scx.remove(collapse_pair[1])
            V[collapse_pair[0]] = collapse_pair[1]
        else:
            # No free face was found.
            top_simplex = sample(top_simplices(expanded_scx), 1)[0]
            expanded_scx.remove(top_simplex)
            C.add(top_simplex)

    return (V, C)


e0 = set([(1, 2, 3)])
e1 = {(1, 2, 5), (2, 3, 5), (3, 5, 6), (3, 4, 6), (1, 4, 6), (1, 2, 4)}
e2 = {(1, 3, 6), (3, 4, 6), (4, 5, 6), (2, 5, 6), (2, 3, 5), (1, 3, 5)}
e3 = {(1, 2, 3), (2, 3, 6), (3, 4, 6), (4, 5, 6)}

for simplicial_complex in (e0, e1, e2, e3):
    print(f"Simplicial complex: {simplicial_complex}.")
    V, C = random_discrete_gradient_vector_field(simplicial_complex)
    print(f"Discrete gradient vector field: {V}.")
    print(f"Critical simplices: {C}")
    print("-" * 80)
