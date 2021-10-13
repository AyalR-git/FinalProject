"""
Written by Ayal Rana & Nir Presser
"""

import sys
from Modules.graph import Graph
from Modules.globals import MAX_ROUND_TRIP
from Modules.christofides_tsp_solver import ChristofidesTSPSolver


class TSPDSolver(object):
    """
    The solver object
    """
    def __init__(self, dist_mat, locations, max_round_trip=MAX_ROUND_TRIP, start_location=0):
        """
        Initiats the object
        """
        self.start_location = start_location
        self.dist_mat = dist_mat
        self.locations = locations
        self.num_locations = len(self.locations)
        self.locations_dict = {}
        for i in range(self.num_locations):
            self.locations_dict[i] = locations[i]

        self.max_round_trip = max_round_trip

    def solve(self, dist_mat):
        """
        Solves the problem according to the input
        :return: Tuple of the plan + the dropped locations
        """
        graph = Graph(dist_mat=dist_mat, size=self.num_locations)
        _, optimal_routes = self.get_optimal_travel_routes(graph)

        return optimal_routes

    def get_optimal_travel_routes(self, graph, solver_obj=ChristofidesTSPSolver):
        """
        Returns the best travel plan for a drone with a limit of a distance per round trip
        @param graph:The graph on which we will analyze the travel plan
        @type graph: Graph
        @param solver_obj: The solver constructor for creating a solver object
        @type solver_obj: Solver Obj
        """
        possible_routes = {}
        optimal_route = []
        current = 0

        _min = sys.maxsize
        all_sub_sets = graph.all_sub_partitions(self.start_location)
        for i in all_sub_sets:
            possible_routes[str(i)] = []
            subsets = []
            for j in i:
                subsets.append(graph.create_graph_from_subset(graph, j))

            current = 0
            for g in subsets:
                solver = solver_obj(g)
                cost, route = solver.solve(self.start_location)

                # If cost is above max_round_dist drone cannot perform this trip
                if cost >= sys.maxsize or current >= sys.maxsize or cost > self.max_round_trip:
                    current = sys.maxsize
                else:
                    current += cost

                possible_routes[str(i)].append(route)

            if _min > current >= 0:
                optimal_route = possible_routes[str(i)]
                _min = current

        if _min == sys.maxsize:
            print("No possible way to make a travel plan with this constraint\'s duration limit: %s" % self.max_round_trip)
            return None, None

        return _min, optimal_route
