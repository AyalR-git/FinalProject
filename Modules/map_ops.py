"""
Written by Ayal Rana & Nir Presser
"""

import re
import urllib.request
from globals import (DIRECTIONS_URL, TRAVEL_DURATION_PATTERN,
                     SEC_IN_HOUR, NOT_FOUND_ERROR, DEFAULT_LOCATION_CHECKER)


class MapOps(object):
    """
    The google maps operations wrapper object
    """
    def __init__(self):
        """
        Initiats the object
        """
        self.bing_maps_url = DIRECTIONS_URL

    def is_location_exists(self, loc) -> bool:
        """
        Verifies if a location exists or no.
        :param loc: The location to check
        :return: True or False
        """
        try:
            route_url = DIRECTIONS_URL % (loc, DEFAULT_LOCATION_CHECKER)
            request = urllib.request.Request(route_url)
            response = urllib.request.urlopen(request)
            return True

        except Exception:
                return False

    def get_duration(self, loc1, loc2) -> float:
        """
        Gets the distance between two locations
        :param loc1: First location
        :param loc2: Second location
        :return: The duration between the locations
        """
        route_url = DIRECTIONS_URL % (loc1, loc2)
        request = urllib.request.Request(route_url)
        response = urllib.request.urlopen(request)

        r = response.read().decode(encoding="utf-8")
        duration = float(re.findall(TRAVEL_DURATION_PATTERN, r)[0]) / SEC_IN_HOUR
        return duration
