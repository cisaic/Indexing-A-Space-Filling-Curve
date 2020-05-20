import numpy as np
from .calc_index import calc_index
from .define_order import define_order
import string

# constrained to max 52 states for now, to maintain simplicity in label alphabet
def hilbert_index3D(seq, dims):
    
    '''
    General function for converting sequence into numeric index
    for any space filling curve in n dimensions
    
    Parameters:
    ----------
    seq: String
        Input string to be converted 
        
    dims: int array
        Array of dimensions of curve at order 0 
        
    Returns
    -------
    result: list
        List of matrix indices 
    '''

    states = np.prod(dims)

    #transformation matrix 
    transform = [np.array(np.arange(dim)) for dim in dims]
    tr = np.array(np.meshgrid(*transform)).T.reshape(-1,len(dims))

    tr = define_order(tr)
    
    #create orthant labels
    alph = string.ascii_uppercase[:states]
    
    #dictionary of orthant labels and corresponding transformations
    dic = {}
    for key, val in zip (alph, tr):
        dic[key] = val
    
    # x, y, z, etc. coordinate values for point on the curve 
    result = np.zeros_like(dims)
    for i, val in enumerate(dims): 
        result[i] = calc_index(dic, seq, dims[i], i)
    
    return result