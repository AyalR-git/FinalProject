"""
Written by Ayal Rana & Nir Presser
"""

from globals import API_KEY
from datetime import datetime
from googlemaps.client import Client


class MapOps(object):
    """
    The google maps operations wrapper object
    """
    def __init__(self):
        """
        Initiats the object
        """
        self.gmaps = Client(API_KEY)

    def get_distance(self, loc1, loc2) -> tuple:
        """
        Gets the distance between two locations
        :param loc1: First location
        :param loc2: Second location
        :return: The distance and duration between the places (dist, dur)
        """
        now = datetime.now()
        directions_result = self.gmaps.directions(loc1, loc2, mode="transit", departure_time=now)
        # TODO: Need to test and parse output to return dist and dur (maybe only dur since the hours is what we want)
        return 1, 1
