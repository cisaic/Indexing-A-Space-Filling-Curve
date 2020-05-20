import numpy as np

# find index along a particular dimension x
# split range into _dim_ sections (ex. if dim = 3, split range into 3 sections)
# follow dictionary to determine which subsection to narrow focus to
def calc_index(dic, seq, dim, x):
    
    '''
    Calculates index for particular dimension 
    
    Parameters:
    ----------
    dic: Dictionary 
        Labels with corresponding transformations
        
    seq: String
        Input string to be converted 
        
    dim: int
        Dimensions of curve at order 0 
        
    x: position of dimension to search in dictionary
        
    Returns
    -------
    span[0]: int
        integer value for index position along given dimension 
    '''
    
    order = len(seq)
    n = dim ** order
    span = np.linspace(0, n, num=dim+1, endpoint=True, dtype = int)
    
    for val in seq:
        index = dic[val][x]
        span = np.linspace(span[index], span[index+1], num = dim+1, endpoint = True, dtype = int)

    return span[0]
