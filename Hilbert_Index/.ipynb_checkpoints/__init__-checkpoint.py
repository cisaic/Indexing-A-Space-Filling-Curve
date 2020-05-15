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
    else:
        rules = {'a': np.array([0,0]),
                 'b': np.array([0,1]),
                 'c': np.array([1,1]),
                 'd': np.array([1,0])
                }
        dim = 2
        index = np.array([])

        for order, val in enumerate(seq[::-1].lower()):
            if index.size == 0:
                index = np.zeros_like(rules[val])
            index += (dim ** order) * rules[val] 

        return index.tolist()