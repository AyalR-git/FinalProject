"""
Written by Ayal Rana & Nir Presser
"""

from map_ops import MapOps


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
        if not self.is_all_locations_exists(locations):
            return []

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

    def is_all_locations_exists(self, locations) -> False:
        """
        Checks if all locations exist
        :param locations: The locations to check
        :return: True or False
        """
        for loc in locations:
            if not self.map_ops.is_location_exists(loc):
                print(f"Location {loc} does not exist, cannot perform trip planning. Please verify your locations are valid")
                return False

        return True
