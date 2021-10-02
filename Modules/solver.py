"""
Written by Ayal Rana & Nir Presser
"""

from globals import *
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2


class Solver(object):
    """
    The solver object
    """
    def __init__(self):
        """
        Initiats the object
        """
        self.model = None
        self.manager = None

    def solve(self, model) -> tuple:
        """
        Solves the problem according to the input
        :param model: The model to solve
        :return: Tuple of the plan + the dropped locations
        """
        self.model = model

        # Create the routing index manager.
        self.manager = pywrapcp.RoutingIndexManager(len(self.model[DISTANCE_MATRIX]), self.model[NUM_DAYS], self.model[DEPOT])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(self.manager)
        transit_callback_index = routing.RegisterTransitCallback(self._distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        demand_callback_index = routing.RegisterUnaryTransitCallback(self._demand_callback)
        routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, self.model[DAY_CAPACITIES], True, 'Capacity')

        # Allow to drop nodes.
        penalty = 1000
        for node in range(1, len(self.model[DISTANCE_MATRIX])):
            routing.AddDisjunction([self.manager.NodeToIndex(node)], penalty)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_parameters.time_limit.FromSeconds(1)

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        # TODO: Need to replace the print_solution to something we want to work with
        if assignment:
            print_solution(self.model, self.manager, routing, assignment)

        return 1, 1  # TODO: change to actual return values

    def _distance_callback(self, from_index, to_index):
        """
        :param from_index: The index from
        :param to_index: The index to
        :return: Returns the distance between the two nodes
        """
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)

        return self.model[DISTANCE_MATRIX][from_node][to_node]

    def _demand_callback(self, from_index):
        """
        :param from_index: The index from which to get the node
        :return: Returns the demand of the node
        """
        # Convert from routing variable Index to demands NodeIndex.
        from_node = self.manager.IndexToNode(from_index)

        return self.model[DEMANDS][from_node]


# TESTING FUNCS #

def print_solution(data, manager, routing, assignment):
    """Prints assignment on console."""
    print(f'Objective: {assignment.ObjectiveValue()}')
    # Display dropped nodes.
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)
    # Display routes
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total Distance of all routes: {}m'.format(total_distance))
    print('Total Load of all routes: {}'.format(total_load))

# !- TESTING FUNCS  -! #
