### PART 1 ###

def orientation(A, B, C): 
    """
    Returns the orientation of the points A, B and C,
    where points are given as A = (x1, y2), B = (x2, y2) and C = (x3, y3).
    """
    
    cross_product = (B[1] - A[1]) * (C[0] - B[0]) - (B[0] - A[0]) * (C[1] - B[1]) 

    if cross_product > 0:   
        return -1    # Clockwise orientation
    elif cross_product < 0: 
        return 1    # Counterclockwise orientation
    else:  
        return 0    # None -- points are colinear
