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

    def get_plan(self, locations: list, num_of_days: int):
        """
        Return a trip plan by which the user can travel
        :param locations: List of the locations to visit on the trip
        :param num_of_days: Number of days for the trip
        :return: The trip plan
        """
        # Create the model
        self.__init_model(locations=locations, num_of_days=num_of_days)
        plan, dropped_locations = self.solver.solve(self.model, locations)

        return plan, dropped_locations

    def __init_model(self, locations: list, num_of_days: int):
        """
        Return the model to the solver
        :param locations: List of the locations to visit on the trip
        :param num_of_days: Number of days for the trip
        :return: Model for the solver
        """
        self.model[DISTANCE_MATRIX] = self.d_mat_creator.get_dis_mat(locations)
        self.model[DEMANDS] = [0]*len(locations)
        self.model[DAY_CAPACITIES] = [6]*num_of_days
        self.model[NUM_DAYS] = num_of_days
        self.model[DEPOT] = 0


if __name__ == "__main__":
    obj = TripPlanner()
    p, d = obj.get_plan(locations=["Vienna", "Graz", "Gusausee", "Innsbruck", "Murau"], num_of_days=1)
    print(p)
    print(d)
