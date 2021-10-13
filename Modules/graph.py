"""
Written by Ayal Rana & Nir Presser
"""

import sys
import numpy as np
from itertools import permutations

# A great value unlikely to occur, to represent that edge does not exist
EDGE_NOT_EXIST = sys.maxsize


class GraphGenerator(object):
    """
    Class that generates a random graph with random values, according to size given
    """
    def __new__(cls, size, upper_bound=100):
        """
        Generate a random graph with random values of size 'size'
        :param size: The number of vertices
        :type: int
        :param upper_bound: The upper bound of random values for graph edges
        :type: int
        """
        ret = Graph(size, upper_bound)
        ret.randomize_edges()
        return ret


class Graph(object):
    """
    Class that represents a graph
    """
    def __init__(self, size, upper_bound=100, dist_mat=None):
        """
        Creating a Graph instance with required attributes
        :param size: The number of vertices
        :param upper_bound: An upper bound for matrix size
        :param dist_mat: A matrix from which to create the graph
        """
        self.dist_mat = dist_mat
        self.upper_bound = upper_bound
        self.size = size
        zeros = [[0] * size for i in range(size)]
        self._graph = np.array([zeros[i] for i in range(size)])

        if dist_mat:
            for i in range(size):
                for j in range(size):
                    self._graph[i][j] = dist_mat[i][j] + 1.5

    def __copy__(self):
        """
        Creates and returns a copy of this graph instance
        :return: Copied instance f this graph
        :rtype: Graph
        """
        if self.dist_mat:
            graph_copy = Graph(dist_mat=self.dist_mat, size=self.size)

        else:
            graph_copy = Graph(size=self.size)

        graph_copy._graph = np.array(self._graph)
        return graph_copy

    def randomize_edges(self):
        """
        Randomizes the edges of the graph, 0 is referred as edge does not exist
        """
        self._graph = np.random.randint(1, self.upper_bound, size=(self.size, self.size))
        for i in range(self.size):
            self._graph[i][i] = 0

    def make_zeros(self):
        """
        Makes all the edges equal to zero
        """
        for i in range(self.size):
            for j in range(self.size):
                self._graph[i][j] = 0

    def get_edge(self, vertex1, vertex2):
        """
        Return the edge's weight between 2 vertices
        :param vertex1: The source vertex index
        :type: int
        :param vertex2: The dest vertex index
        :type: int
        :return: The weight of the edge between vertex1 and vertex2 or EDGE_NOT_EXIST
        :rtype: int
        """
        return [self._graph[vertex1][vertex2], EDGE_NOT_EXIST][self._graph[vertex1][vertex2] == 0]

    def set_edge(self, vertex1, vertex2, val):
        """
        Return the edge's weight between 2 vertices
        :param vertex1: The source vertex index
        :type: int
        :param vertex2: The dest vertex index
        :type: int
        :param val: The value to insert
        :type: int
        """
        self._graph[vertex1][vertex2] = val

    def all_poss_round_trips(self, start_vertex):
        """
        Returns all possible round trips order in the graph - from start_vertex to start_vertex through all vertices
        :param start_vertex: The vertex from which we want all possible round trips
        :type: int
        :return: List of all possible round trips when each round trip is represented as tuple
        :rtype: list(tuple)
        """
        tuple_of_first = (start_vertex,)
        vertices_t0_perm = []
        for i in range(self.size):
            if self.get_edge(start_vertex, i) != EDGE_NOT_EXIST:
                vertices_t0_perm.append(i)

        ret = list(permutations(vertices_t0_perm))
        for i in range(len(ret)):
            ret[i] = tuple_of_first + ret[i] + tuple_of_first

        return ret

    def get_graph(self):
        """
        Returns the graph
        :return: the graph
        :rtype: numpy.array[][]
        """
        return self._graph

    def get_num_of_existing_edges(self):
        """
        Returns the number of existing edges in the graph
        :return: Num of edges
        :rtype: int
        """
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if self._graph[i][j] != 0:
                    cnt += 1

        return cnt

    def triangle_inequality_graph(self):
        """
        Adjusts the values of the graph to have values that aplly to the triangle inequality
        """
        lower = self.upper_bound
        self._graph = np.random.randint(lower, (self.upper_bound * 2), size=(self.size, self.size))
        for i in range(self.size):
            self._graph[i][i] = 0

    def make_symmetric(self):
        """
        Makes the graph symetric
        """
        for i in range(self.size):
            for j in range(self.size):
                if j > i:
                    continue
                self._graph[i][j] = self._graph[j][i]

    def get_out_degree(self, vertex):
        """
        Returns the out degree of the vertex given
        :param vertex: The vertex whose edges we check
        :type vertex: int
        :return: The number of edges vertex has
        :rtype: int
        """
        return len([i for i in range(self.size) if self.get_edge(vertex, i) != EDGE_NOT_EXIST])

    def partition(self, collection):
        """
        Returns a partition from a particular collection of vertices
        :param collection: The list of vertices
        :type collection: list
        :return: The partition
        :rtype: list
        """
        if len(collection) == 1:
            yield [collection]
            return

        first = collection[0]
        for smaller in self.partition(collection[1:]):
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[first] + subset] + smaller[n + 1:]

            yield [[first]] + smaller

    def all_sub_partitions(self, start_city):
        """
        computes all the available sub-partitions in the graph.
        :param start_city: start (and end) city of the roundtrip.
        :type: int.
        :return: all the available sub-partitions.
        :rtype: list.
        """
        cities = list(range(0, self.size))
        cities.pop(cities.index(start_city))
        starting_city = [start_city, ]
        ret = []
        for p in self.partition(cities):
            for i in range(len(p)):
                p[i] = starting_city + p[i] + starting_city
            ret.append(p)
        return ret

    def create_graph_from_subset(self, G, subset):
        """
        Creates a graph from a subpartition
        :param G: The original graph
        :type G: Graph
        :param subset: The subset from which to create the graph
        :type subset: list
        :return: The graph representation of the subset
        :rtype: Graph
        """
        local_g = GraphGenerator(G.size, 10)
        local_g.make_zeros()
        for i in subset:
            for j in subset:
                temp = G.get_edge(i, j)
                if temp == EDGE_NOT_EXIST:
                    local_g.set_edge(i, j, 0)
                    continue
                local_g.set_edge(i, j, G.get_edge(i, j))

        return local_g
