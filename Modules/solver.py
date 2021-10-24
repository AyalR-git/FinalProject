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
        self.locations_dict = {}

    # TODO: Need to understand why this solver still dropping nodes even after giving demands 0 to all nodes.
    # TODO: This is the last thing in order to finish the solver
    def solve(self, model, locations) -> tuple:
        """
        Solves the problem according to the input
        :param model: The model to solve
        :param locations: The locations list
        :return: Tuple of the plan + the dropped locations
        """
        for i in range(len(locations)):
            self.locations_dict[i] = locations[i]

        self.model = model

        # Create the routing index manager.
        self.manager = pywrapcp.RoutingIndexManager(len(self.model[DISTANCE_MATRIX]), self.model[NUM_DAYS], self.model[DEPOT])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(self.manager)
        transit_callback_index = routing.RegisterTransitCallback(self._distance_callback)

        # Define cost of each arc
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        demand_callback_index = routing.RegisterUnaryTransitCallback(self._demand_callback)
        routing.AddDimensionWithVehicleCapacity(demand_callback_index, 0, self.model[DAY_CAPACITIES], True, 'Capacity')

        # Define duration limit
        routing.AddDimension(transit_callback_index, 0, 9, True, 'Distance')
        routing.SetFixedCostOfAllVehicles(9)

        # Allow to drop nodes.
        penalty = 1000
        for node in range(1, len(self.model[DISTANCE_MATRIX])):
            routing.AddDisjunction([self.manager.NodeToIndex(node)], penalty)

        routing.SetPrimaryConstrainedDimension("Distance")

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.EVALUATOR_STRATEGY
        routing.SetFirstSolutionEvaluator(evaluator=self._distance_callback)
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        search_parameters.time_limit.FromSeconds(1)

        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        return self.print_solution(self.model, self.manager, routing, assignment)

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

    def print_solution(self, data, manager, routing, assignment):
        """Prints assignment on console."""
        print(f'Objective: {assignment.ObjectiveValue()}')
        dropped_nodes_list = []
        trip_plan = {}

        # Display dropped nodes.
        dropped_nodes = 'Dropped nodes:'
        for node in range(routing.Size()):
            if routing.IsStart(node) or routing.IsEnd(node):
                continue

            if assignment.Value(routing.NextVar(node)) == node:
                dropped_nodes += ' {}'.format(manager.IndexToNode(node))
                dropped_nodes_list.append(self.locations_dict[manager.IndexToNode(node)])

        print(dropped_nodes)
        # Display routes
        total_distance = 0
        total_load = 0

        for day_id in range(data[NUM_DAYS]):
            trip_plan[day_id] = []
            index = routing.Start(day_id)
            plan_output = '-------------------------------Route for Day {}-------------------------------\n'.format(day_id)
            route_duration = 0
            route_load = 0
            previous_index = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                trip_plan[day_id].append(self.locations_dict[node_index])
                route_load += data[DEMANDS][node_index]
                plan_output += '"{0}" - Overall Driving Hours - {1} ---->\n'.format(self.locations_dict[node_index], route_load)
                previous_index = index
                index = assignment.Value(routing.NextVar(index))
                route_duration += routing.GetArcCostForVehicle(previous_index, index, day_id)

            plan_output += '"{0}" - Overall Driving Hours - {1}\n'.format(self.locations_dict[manager.IndexToNode(index)], route_load)
            plan_output += 'Duration of the route: {} Hours\n'.format(route_duration)
            plan_output += 'Total time left to spend at the locations: {}\n'.format(HOUR_PER_DAY - HOUR_PER_SLEEP - route_duration)
            plan_output += '------------------------------------------------------------------------------\n\n'
            print(plan_output)
            total_distance += route_duration
            total_load += route_load

        return trip_plan, dropped_nodes_list
