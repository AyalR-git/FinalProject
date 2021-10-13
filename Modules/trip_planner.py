"""
Written by Ayal Rana & Nir Presser
"""

from Modules.tspd_solver import TSPDSolver
from Modules.dist_mat_creator import DistMatCreator


class TripPlanner(object):
    """
    A class that wraps the entities that are used to provide the planned trip
    """
    def __init__(self):
        """
        Initiates the object
        """
        self.solver = None
        self.d_mat_creator = DistMatCreator()

    def get_plan(self, locations: list, num_of_days: int, start_location=0):
        """
        Return a trip plan by which the user can travel
        :param locations: List of the locations to visit on the trip
        :param num_of_days: Number of days for the trip
        :param start_location: The location from which to start
        :return: The trip plan
        """
        plan = []
        num_locations = len(locations)
        locations_dict = {}
        for i in range(num_locations):
            locations_dict[i] = locations[i]

        dist_mat = self.d_mat_creator.get_dis_mat(locations)
        if not dist_mat:
            return []

        self.solver = TSPDSolver(dist_mat=dist_mat, locations=locations, start_location=start_location)
        optimal_routes = self.solver.solve(dist_mat)

        # Get only the plan for the number of days given
        for i in range(num_of_days):
            if not optimal_routes:
                break

            max_route = None
            max_len = 0
            max_index = None
            routes_to_check = list(optimal_routes)
            for j in range(len(routes_to_check)):
                if len(routes_to_check[j]) > max_len:
                    max_route = routes_to_check[j]
                    max_index = j
                    max_len = len(routes_to_check[j])

            optimal_routes.pop(max_index)
            plan.append(max_route)

        # Print Plan
        print(f"Best plan for {num_of_days} days:")
        index = 1
        for route in plan:
            rt_output = ""
            print(f"Route for day {index}:")
            iteration = 0
            for j in route:
                if iteration == len(route) - 1:
                    rt_output += f"  {locations_dict[j]}"
                    break

                rt_output += "  {0}  -----  Drive Duration: {1:.2f} Hours ----->".format(locations_dict[j], dist_mat[route[iteration]][route[iteration+1]])
                iteration += 1

            print(rt_output)
            print("\n")
            print("Calculations are assuming a transit time of 1.5 hours average spent on each location")
            print("An overall of maximum of 11 hours of travel per day, All the rest is to sleep, eat and chill ;)\n\n")

            index += 1

        return plan
