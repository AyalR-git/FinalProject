"""
Written by Ayal Rana & Nir Presser
"""

from Modules.map_ops import MapOps
from Modules.trip_planner import TripPlanner
from Modules.globals import STATUS_EXIT, STATUS_CHANGE, DONE, MAX_TRAVEL_DURATION, COUNTRIES


def main():
    """
    The main app to communicate with the user
    """
    open_note()
    status = STATUS_CHANGE

    while status == STATUS_CHANGE:
        status = app()

    print("Thanks for using the Trip Planner app - Till next time! :) ")
    exit(STATUS_EXIT)


def app():
    """
    The actual app
    :return: status
    """
    source = 0
    location_list = []
    map_ops = MapOps()

    country = input("Please choose a country to travel: ")
    while country.lower() not in COUNTRIES:
        print(f"Country {country} does not exist, please enter an existing country name")
        country = input("Please choose a country to travel:")

    s_loc = input("Please choose a location at which you want to sleep: ")
    s_loc = replace_spaces(s_loc)
    while not map_ops.is_location_exists(country=country, loc=s_loc):
        print(f"Location {s_loc} does not exist please enter a new one")
        s_loc = input("Please choose a location at which you want to sleep: ")
        s_loc = replace_spaces(s_loc)

    location_list.append(s_loc)

    number_of_days = input("Please enter the number of days you want to travel: ")
    while type(number_of_days) is str:
        try:
            number_of_days = int(number_of_days)

        except Exception as e:
            number_of_days = input("Input was not a valid number - please enter a number: ")

    print("Please enter the places you want to visit in an ordered fashion after each prompt you'll get")
    print("Please pay attention to write every location ACCURATELY!")
    print("When you are done, please submit the word 'done' in LOWER CASE")
    while True:
        loc = input("Please enter a location you want to visit: ")
        loc = replace_spaces(loc)
        if loc == DONE:
            break

        if not map_ops.is_location_exists(country=country, loc=loc):
            print(f"Location {loc} does not exist in {country} - Please enter a new one")
            continue

        if loc in location_list:
            print(f"Location {loc} was already chosen, please choose a different one")
            continue

        if map_ops.get_duration(s_loc, loc) > MAX_TRAVEL_DURATION:
            print(f"Location {loc} is too far from {s_loc} to travel in one day, choose another")
            continue

        location_list.append(loc)

    print("These are the locations you entered:")
    for pl in location_list:
        print(pl)

    for i in range(len(location_list)):
        if location_list[i] == s_loc:
            source = i
            break

    planner = TripPlanner()
    plan = planner.get_plan(locations=location_list, num_of_days=number_of_days, start_location=source)
    if not plan:
        print("An error occured please start the app again")
        exit(0)

    print("Are you satisfied with the plan? (Please choose the right number for you)")
    choice = input("1. I think I need to change something....                 2. All good, can't wait to get there!\n")
    if int(choice) == STATUS_CHANGE:
        return STATUS_CHANGE

    return STATUS_EXIT


def replace_spaces(s):
    """
    Replaces spaces with "-"
    :param s: The string to format
    :return: The foramted string
    """
    return s.replace(" ", "-")


def open_note():
    """
    Open note method
    """
    print("Hello and welcome to the trip planner app!")
    print("Here you can enter your destinations and easely get an itenerary by which to travel")
    print("Please notice our usage cooporation with Bing Maps")
    print("Lets get started!")


if __name__ == "__main__":
    main()
