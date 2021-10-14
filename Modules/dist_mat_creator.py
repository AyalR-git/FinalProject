"""
Written by Ayal Rana & Nir Presser
"""

from Modules.map_ops import MapOps


class DistMatCreator(object):
    """
    An object that creates a distance matrix
    """
    def __init__(self):
        """
        Initiats the object
        """
        self.map_ops = MapOps()

    def get_dis_mat(self, locations):
        """
        Creates a distance matrix from the given list of location using the MapOps object
        :param locations: The locations from which to create the matrix
        :return: A distance matrix
        """
        num_locations = len(locations)
        mat = []
        for i in range(num_locations):
            mat.append([0.]*num_locations)

        for i in range(num_locations):
            for j in range(num_locations):
                if i == j:
                    mat[i][j] = 0
                else:
                    mat[i][j] = self.map_ops.get_duration(locations[i], locations[j])

        return mat
