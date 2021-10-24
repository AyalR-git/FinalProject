"""
Written by Ayal Rana & Nir Presser
"""

import pandas
import datetime
from Modules.tspd_solver import Solver
from Modules.dist_mat_creator import DistMatCreator
from Modules.globals import LOCATION_FACTOR, MINUTS_PER_HOUR


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
        dropped_locations = list(locations)
        num_locations = len(locations)
        locations_dict = {}
        for i in range(num_locations):
            locations_dict[i] = locations[i]

        dist_mat = self.d_mat_creator.get_dist_mat(locations)
        if not dist_mat:
            return []

        to_p = pandas.DataFrame(dist_mat, locations, locations)
        print(to_p)
        print("")

        self.solver = Solver(dist_mat=dist_mat, locations=locations, start_location=start_location)
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
            next_time = datetime.time(8, 30)
            rt_output = ""
            print(f"Route for day {index}:")
            iteration = 0
            for j in route:
                if iteration == len(route) - 1:
                    break

                if locations_dict[j] in dropped_locations:
                    dropped_locations.remove(locations_dict[j])

                rt_output += f"Drive Start Time: {next_time}\tDrive Start Location: {locations_dict[j]}\t"
                drive_dur = dist_mat[route[iteration]][route[iteration+1]]
                rt_output += "Drive Duration: {0} hours and {1} minutes\t".format(int(drive_dur*MINUTS_PER_HOUR)//MINUTS_PER_HOUR, int(drive_dur*MINUTS_PER_HOUR)%MINUTS_PER_HOUR)
                next_time = self._add_time(next_time, drive_dur)
                rt_output += f"Drive Arrival Time: {next_time}\tDrive Arrival Location:{locations_dict[route[iteration+1]]}\n"
                next_time = self._add_time(next_time, LOCATION_FACTOR)
                iteration += 1

            print(rt_output)
            print(f"Overall {iteration} location transitions\n")
            index += 1

        if dropped_locations:
            print("Dropped locations are:")
            for loc in dropped_locations:
                print(f"{loc}")

        print("\nCalculations are assuming a transit time of 1.5 hours average spent on each location")
        print("An overall of maximum of 11 hours of travel per day, All the rest is to sleep, eat and chill ;)\n\n")

        return plan

    def _add_time(self, time, hours_to_add):
        """
        Returns new time after hours_to_add
        :param time:
        :param hours_to_add:
        :return:
        """
        timedelta = datetime.timedelta(hours=hours_to_add)
        start = datetime.datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)
        end = start + timedelta
        return end.time()
