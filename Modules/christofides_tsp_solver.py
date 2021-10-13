"""
Written by Ayal Rana & Nir Presser
"""

import sys
import itertools
from Modules.graph import EDGE_NOT_EXIST, GraphGenerator


class ChristofidesTSPSolver(object):
    """
    A class to represent a minimal spreading tree
    """
    def __init__(self, graph):
        """
        Initiates the required resources for computing the solution
        @param graph: The graph in which the problem exist
        @type graph: Graph
        """
        self.graph = graph
        self.mst_graph = None
        self.reduced_to_odd_vertices_graph = None
        self.odd_vertices_of_graph = None
        self.minimal_match_cost = sys.maxsize
        self.perfect_matches = {}
        self.united_graph = None
        self.solution = None
        self.solution_cost = None

    def solve(self, start_vertex):
        """
        Solves the TSP problem using christofides algorithm
        @param start_vertex: The start vertex of the graph from which we will solve
        @type start_vertex: int
        @return: A route estimated to be the solution for the TSP
        @rtype: tuple(tuple(int), int)
        """
        if self.graph.get_num_of_existing_edges() == 2:
            for i in range(self.graph.size):
                if i == start_vertex:
                    continue

                if self.graph.get_edge(start_vertex, i) != EDGE_NOT_EXIST:
                    # We multiply by 2 because the graph is symmetric
                    return self.graph.get_edge(start_vertex, i) * 2, (start_vertex, i, start_vertex)

        self._find_mst(start_vertex)
        self.mst_graph.make_symmetric()
        route = self._find_euler_tour(start_vertex, self.mst_graph)
        route = self._remove_repeating_vertices(route)
        route.append(start_vertex)
        self.solution = tuple(route)
        self.solution_cost = self._calculate_route_cost(self.solution)

        return self.solution_cost, self.solution

    def solve_with_match(self, start):  # DO NOT USE - EXPERIMENTAL
        """
        Solves the TSP problem using christofides algorithm with matching
        @param start: The start vertex of the graph from which we will solve
        @type start: int
        @return: A route estimated to be the solution for the TSP
        @rtype: tuple(tuple(int), int)
        """
        self._find_mst(start)
        print(self.mst_graph.get_graph())
        self._odd_vertices_of_mst()
        self._reduce_to_odd_vertices()
        self._find_minimal_matching()
        self._unite_mst_and_match()
        route = self._find_euler_tour(start, self.united_graph)
        route = self._remove_repeating_vertices(route)
        route.append(start)
        self.solution = tuple(route)
        self.solution_cost = self._calculate_route_cost(self.solution)

        return self.solution_cost, self.solution

    def _find_mst(self, start):
        """
        Finds the Minimal Spanning Tree of the graph
        @param start: The root of the MST
        @type start: int
        @return: The MST represented as a graph
        @rtype: Graph
        """
        self.mst_graph = GraphGenerator(self.graph.size)
        self.mst_graph.make_zeros()
        reached_vertices = [start]

        vertex_to_add = None
        vertex_from = None

        num_of_vertices = self.graph.size

        for i in range(self.graph.size):
            found_edge = False
            for j in range(self.graph.size):
                if self.graph.get_edge(i, j) != EDGE_NOT_EXIST:
                    found_edge = True
                    break

            if not found_edge:
                num_of_vertices -= 1

        while len(reached_vertices) != num_of_vertices:

            vertices_to_check = [vertex for vertex in list(range(self.graph.size)) if vertex not in reached_vertices]
            minimal_edge = sys.maxsize
            for i in vertices_to_check:

                for vertex in reached_vertices:
                    if self.graph.get_edge(vertex, i) < minimal_edge and i not in reached_vertices:
                        minimal_edge = self.graph.get_edge(vertex, i)
                        vertex_from = vertex
                        vertex_to_add = i

            if minimal_edge != sys.maxsize:
                reached_vertices.append(vertex_to_add)
                self.mst_graph.set_edge(vertex_from, vertex_to_add, minimal_edge)
                self.mst_graph.set_edge(vertex_to_add, vertex_from, minimal_edge)

        return self.mst_graph

    def _odd_vertices_of_mst(self):
        """
        Returns the vertices having Odd degree in the Minimum Spanning Tree(MST).
        @return: List of vertices with an odd degree
        @rtype: List(int)
        """
        if not self.mst_graph:
            self._find_mst(0)

        vertices_degree = {}
        for i in range(self.mst_graph.size):
            vertices_degree[i] = 0
            for j in range(self.mst_graph.size):
                if self.mst_graph.get_edge(i, j) != EDGE_NOT_EXIST:
                    vertices_degree[i] = vertices_degree[i] + 1

        odd_vertices = [vertex for vertex, degree in vertices_degree.items() if degree % 2 == 1]
        self.odd_vertices_of_graph = odd_vertices

        return odd_vertices

    def _reduce_to_odd_vertices(self):
        """
        Reduces the original graph to be without even degree vertices
        @return: The new reduced graph
        @rtype: Graph
        """
        self.reduced_to_odd_vertices_graph = GraphGenerator(self.graph.size)
        self.reduced_to_odd_vertices_graph.make_zeros()

        odd_vertices = self._odd_vertices_of_mst()
        for i in odd_vertices:
            for j in odd_vertices:
                if self.graph.get_edge(i, j) != EDGE_NOT_EXIST:
                    edge_val = self.graph.get_edge(i, j)

                else:
                    edge_val = 0

                self.reduced_to_odd_vertices_graph.set_edge(i, j, edge_val)

        return self.reduced_to_odd_vertices_graph

    def _find_minimal_matching(self):
        """
        Finds the minimal perfect matching in a given graph
        @return: The minimal match and the minimal cost of the latter
        @rtype: tuple(list, list)
        """
        match_options = [set(i) for i in itertools.combinations(set(self.odd_vertices_of_graph), len(self.odd_vertices_of_graph) // 2)]
        vertex_sets_to_bipatrite = []
        minimal_match_cost = None
        minimal_match = None

        for vertex_set1 in match_options:
            vertex_set1 = list(sorted(vertex_set1))
            vertex_set2 = []

            for vertex in self.odd_vertices_of_graph:
                if vertex not in vertex_set1:
                    vertex_set2.append(vertex)

            matrix = [[-1000000 for j in range(len(vertex_set2))] for i in range(len(vertex_set1))]

            for i in range(len(vertex_set1)):
                for j in range(len(vertex_set2)):
                    if vertex_set1[i] < vertex_set2[j]:
                        matrix[i][j] = self.reduced_to_odd_vertices_graph.get_edge(vertex_set1[i], vertex_set2[j])

                    else:
                        matrix[i][j] = self.reduced_to_odd_vertices_graph.get_edge(vertex_set2[j], vertex_set1[i])

            vertex_sets_to_bipatrite.append(([vertex_set1, vertex_set2], matrix))

            items_cost = {}
            for item in vertex_sets_to_bipatrite:
                items_cost[self._find_minimal_cost(item)] = item

            minimal_match_cost = min([key for key in items_cost.keys()])
            minimal_match = items_cost[minimal_match_cost]
            self.minimal_match_cost = minimal_match_cost

        return minimal_match, minimal_match_cost

    def _find_minimal_cost(self, item):
        """
        Finds the minimal cost of a certain possible matching
        @param item: A pair of vertex set and a graph
        @type item: tuple
        @return: The minimal cost
        @rtype: int
        """
        vertex_set, bipart_graph = item
        minimal_cost = 0
        perfect_match = []
        v_set1 = list(vertex_set[0])
        v_set2 = list(vertex_set[1])

        while v_set1 and v_set2:
            minimal_edge = EDGE_NOT_EXIST
            vertex_to_remove_s1 = None
            vertex_to_remove_s2 = None

            for i in v_set1:
                for j in v_set2:
                    if self.graph.get_edge(i, j) < minimal_edge:
                        minimal_edge = self.graph.get_edge(i, j)
                        vertex_to_remove_s1 = i
                        vertex_to_remove_s2 = j

            v_set1.pop(v_set1.index(vertex_to_remove_s1))
            v_set2.pop(v_set2.index(vertex_to_remove_s2))
            if (vertex_to_remove_s1, vertex_to_remove_s2) not in perfect_match and (vertex_to_remove_s2, vertex_to_remove_s1) not in perfect_match:
                perfect_match.append((vertex_to_remove_s1, vertex_to_remove_s2))

            minimal_cost += minimal_edge

        self.perfect_matches[minimal_cost] = perfect_match

        return minimal_cost

    def _unite_mst_and_match(self):
        """
        Unites the MST and the matched graph
        @return: The new united graph
        @rtype: Graph
        """
        self.united_graph = GraphGenerator(self.mst_graph.size)
        self.united_graph.make_zeros()

        for i in range(self.mst_graph.size):
            for j in range(self.mst_graph.size):
                if self.mst_graph.get_edge(i, j) == EDGE_NOT_EXIST:
                    self.united_graph.set_edge(i, j, 0)

                else:
                    self.united_graph.set_edge(i, j, self.mst_graph.get_edge(i, j))

        perfect_match = self.perfect_matches[self.minimal_match_cost]
        for pair in perfect_match:
            v_from, v_to = pair
            self.united_graph.set_edge(v_from, v_to, self.graph.get_edge(v_from, v_to))
            self.united_graph.set_edge(v_to, v_from, self.graph.get_edge(v_to, v_from))

        return self.united_graph

    def _find_euler_tour(self, start, graph):
        """
        Finds an euler tour over the graph beginning from start
        @param start: The vertex to begin from
        @type start: int
        @param graph: The graph to find the euler route on
        @type graph: Graph
        @return: The euler route
        @rtype: ist(int)
        """
        num_of_edges = graph.get_num_of_existing_edges()
        edges_visited = []
        vertices_route = []
        tmp_graph = GraphGenerator(graph.size)
        for i in range(graph.size):
            for j in range(graph.size):
                if graph.get_edge(i, j) == EDGE_NOT_EXIST:
                    tmp_graph.set_edge(i, j, 0)

                else:
                    tmp_graph.set_edge(i, j, graph.get_edge(i, j))

        current_vertex = start
        while len(edges_visited) != num_of_edges:
            for i in range(graph.size):
                if current_vertex != i and tmp_graph.get_edge(current_vertex, i) != EDGE_NOT_EXIST:
                    if tmp_graph.get_edge(i, current_vertex) == EDGE_NOT_EXIST and tmp_graph.get_out_degree(current_vertex) > 1:
                        continue

                    edges_visited.append((current_vertex, i))
                    vertices_route.append(current_vertex)
                    tmp_graph.set_edge(current_vertex, i, 0)
                    current_vertex = i
                    break

        return vertices_route

    def _remove_repeating_vertices(self, route):
        """
        Removes repeated vertices from a particular route
        @param route: The route to modify
        @type route: list(int)
        @return: The new modified route
        @rtype: list(int)
        """
        reduced_route = []
        for i in route:
            if i in reduced_route:
                continue

            else:
                reduced_route.append(i)

        return reduced_route

    def _calculate_route_cost(self, route):
        """
        Calculates a routes cost
        @param route: The route to calculate
        @type route: tuple(int)
        @return: The cost of the route
        @rtype: int
        """
        cost = 0
        for i in range(len(route)-1):
            cost += self.graph.get_edge(route[i], route[i+1])

        return cost