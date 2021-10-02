"""
Written by Ayal Rana & Nir Presser
"""

from globals import *
from solver import Solver
from dist_mat_creator import DistMatCreator


class TripPlanner(object):
    """
    A class that wraps the entities that are used to provide the planned trip
    """
    def __init__(self):
        """
        Initiates the object
        """
        self.model = {}
        self.solver = Solver()
        self.d_mat_creator = DistMatCreator()

    def get_plan(self, locations: list):
        """
        Return a trip plan by which the user can travel
        :param locations: List of the locations to visit on the trip
        :return: The trip plan
        """
        # Create the model
        self.__init_model(locations)

        plan, dropped_locations = self.solver.solve(self.model)

        # TODO: Need to choose what to return or print here
        return ""

    def __init_model(self, locations: list):
        """
        Return the model to the solver
        :param locations: List of the locations to visit on the trip
        :return: Model for the solver
        """
        self.model[DISTANCE_MATRIX] = self.d_mat_creator.get_dis_mat(locations)
        self.model[DEMANDS] = [0, 1, 1, 3, 6, 3, 6, 8, 8, 1, 2, 1, 2, 6, 6, 8, 8]
        self.model[DAY_CAPACITIES] = [15, 15, 15, 15]
        self.model[NUM_DAYS] = 4
        self.model[DEPOT] = 0


if __name__ == "__main__":
    obj = TripPlanner()
    obj.get_plan([])
