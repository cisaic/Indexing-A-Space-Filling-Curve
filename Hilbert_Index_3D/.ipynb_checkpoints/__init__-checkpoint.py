import numpy as np

def hilbert_index(seq):
    '''
    Converts input sequence into matrix index 
    for space filling curve in 4 quadrants ABCD
    
    Parameters:
    ----------
    seq: String
        Input string to be converted 
        
    Returns
    -------
    index: list
        List of x,y matrix indices 
    '''
    rules = {'A': np.array([-1, -1, -1]),
             'B': np.array([-1, 1, -1]),
             'C': np.array([-1, 1, 1]),
             'D': np.array([-1, -1, 1]),
             'E': np.array([1, -1, 1]),
             'F': np.array([1, 1, 1]),
             'G': np.array([1, 1, -1]),
             'H': np.array([1, -1, -1])
            }
    dim = 2
    index = np.array([])
    
    for order, val in enumerate(seq[::-1].upper()):
        if index.size == 0:
            index = np.zeros_like(rules[val])
        index += (dim ** order) * rules[val] 
    
    return index.tolist()