import numpy as np
from collections import defaultdict

class HilbertCurveGenerator_3D:
    def __init__(self):
        self.space_alphabet = 'ABCDEFGH'
        self.recurrence_matrix = np.array([[0, 3, 4, 7, 6, 5, 2, 1],
                                           [0, 7, 6, 1, 2, 5, 4, 3],
                                           [0, 7, 6, 1, 2, 5, 4, 3],
                                           [2, 3, 0, 1, 6, 7, 4, 5],
                                           [2, 3, 0, 1, 6, 7, 4, 5],
                                           [4, 3, 2, 5, 6, 1, 0, 7],
                                           [4, 3, 2, 5, 6, 1, 0, 7],
                                           [6, 5, 2, 1, 0, 3, 4, 7]
                                           ]
                                          )
        self.quad_mappings = {'A': np.array([-1.0, -1.0, -1.0]),
                              'B': np.array([-1.0, 1.0, -1.0]),
                              'C': np.array([-1.0, 1.0, 1.0]),
                              'D': np.array([-1.0, -1.0, 1.0]),
                              'E': np.array([1.0, -1.0, 1.0]),
                              'F': np.array([1.0, 1.0, 1.0]),
                              'G': np.array([1.0, 1.0, -1.0]),
                              'H': np.array([1.0, -1.0, -1.0])
                              }

    def __recurse(self, base_array=None):
        if not base_array:
            base_array = self.space_alphabet

        next_results = []
        # Initial Run?

        if type(base_array) == str:
            base_array = np.array(list(base_array))
            # use idx to lookup reorder opperation to perform of base_array
            for idx, quad in enumerate(base_array):
                reorder_array = self.recurrence_matrix[idx]
                reordered_base = base_array[reorder_array]
                next_result = quad + '|' + ''.join(reordered_base)
                next_results.append(next_result)
        else:
            for quad_data in base_array:
                quad_base, base_array = quad_data.split('|')
                reordered_bases = self.__recurse(base_array=base_array)
                _ = [next_results.append(quad_base + reordered_base)
                     for reordered_base in reordered_bases]
        return next_results

    def __expand_last_recursion(self, quad_values):
        expanded_quads = []
        for quad_data in quad_values:
            quad_base, base_array = quad_data.split('|')
            _ = [expanded_quads.append(quad_base + sub_quad)
                 for sub_quad in base_array]
        return expanded_quads

    def generate_curve(self, plot_depth, return_plot_data=True):
        trace_data = defaultdict(lambda: defaultdict(lambda: []))

        recursed_data = None

        if plot_depth == 1:
            quad_labels = list(self.space_alphabet)
            return quad_labels
            
        else:
            for depth in range(1, plot_depth):
                if not recursed_data:
                    recursed_data = self.__recurse(base_array=self.space_alphabet)
                else:
                    recursed_data = self.__recurse(base_array=recursed_data)

                quad_labels = self.__expand_last_recursion(recursed_data)

            return quad_labels
