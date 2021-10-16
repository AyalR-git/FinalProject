"""
Written by Ayal Rana & Nir Presser
"""

import re
import urllib.request
from Modules.globals import *


class MapOps(object):
    """
    The google maps operations wrapper object
    """
    def __init__(self):
        """
        Initiats the object
        """
        self.bing_maps_url = DIRECTIONS_URL

    def is_location_exists(self, country, loc) -> bool:
        """
        Verifies if a location exists or no.
        :param country: The country in which to search for location
        :param loc: The location to check
        :return: True or False
        """
        try:
            route_url = COUNTRY_URL % loc
            request = urllib.request.Request(route_url)
            response = urllib.request.urlopen(request)
            res = response.read().decode(encoding="utf-8")

            countries_list = re.findall(COUNTRY_REGION_PATTERN, res)
            if country not in countries_list:
                return False

            return True

        except Exception as e:
            print(e)
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

        res = response.read().decode(encoding="utf-8")
        duration = float(re.findall(TRAVEL_DURATION_PATTERN, res)[0]) / SEC_IN_HOUR
        return duration

    def is_in_country_region(self, country, loc):
        """

        :param country:
        :param loc:
        :return:
        """
        country_url = COUNTRY_URL % loc
        request = urllib.request.Request(country_url)
        response = urllib.request.urlopen(request)

        r = response.read().decode(encoding="utf-8")
        countries_list = re.findall(COUNTRY_REGION_PATTERN, r)
        if country not in countries_list:
            return False

        return True
