"""
Written by Ayal Rana & Nir Presser
"""

from pycountry import countries

# Translation of target params to solver params
DISTANCE_MATRIX = "distance_matrix"
DEMANDS = "demands"
DAY_CAPACITIES = "vehicle_capacities"
NUM_DAYS = "num_vehicles"
DEPOT = "depot"
DONE = "done"
STATUS_CHANGE = 1
STATUS_EXIT = 0
MAX_ROUND_TRIP = 11
LOCATION_FACTOR = 1.5
MAX_TRAVEL_DURATION = 5
COUNTRY_REGION_PATTERN = '"countryRegion":"([a-zA-Z]+)"'

# Defines to use bingmaps
API_KEY = "AkDeY4EhjZQkB_KGuhPdKpbAi_sEnJGOk-HEuigZtXWRkwut1SUWwXTDfFrUGmFm"
DIRECTIONS_URL = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=%s&wp.1=%s&key={API_KEY}"
COUNTRY_URL = f"http://dev.virtualearth.net/REST/v1/Locations?locality=%s&key={API_KEY}"
LOCALITY_URL = f"http://dev.virtualearth.net/REST/v1/Locations?countryRegion=%s&locality=%s&key={API_KEY}"
TRAVEL_DURATION_PATTERN = "<TravelDuration>([0-9]+)"
SEC_IN_HOUR = 3600
NOT_FOUND_ERROR = "HTTP Error 404: Not Found"
DEFAULT_LOCATION_CHECKER = "Vienna"
HOUR_PER_DAY = 24
HOUR_PER_SLEEP = 7
MINUTS_PER_HOUR = 60

# Countries DB
COUNTRIES = [c.name.lower() for c in countries]
