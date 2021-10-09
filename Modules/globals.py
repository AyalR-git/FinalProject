"""
Written by Ayal Rana & Nir Presser
"""

# Translation of target params to solver params
DISTANCE_MATRIX = "distance_matrix"
DEMANDS = "demands"
DAY_CAPACITIES = "vehicle_capacities"
NUM_DAYS = "num_vehicles"
DEPOT = "depot"

# Defines to use bingmaps
API_KEY = "AkDeY4EhjZQkB_KGuhPdKpbAi_sEnJGOk-HEuigZtXWRkwut1SUWwXTDfFrUGmFm"
DIRECTIONS_URL = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=%s&wp.1=%s&key={API_KEY}"
TRAVEL_DURATION_PATTERN = "<TravelDuration>([0-9]+)"
SEC_IN_HOUR = 3600
NOT_FOUND_ERROR = "HTTP Error 404: Not Found"
DEFAULT_LOCATION_CHECKER = "Vienna"
