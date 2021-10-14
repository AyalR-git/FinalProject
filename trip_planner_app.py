"""
Written by Ayal Rana & Nir Presser
"""

from Modules.map_ops import MapOps
from Modules.trip_planner import TripPlanner
from Modules.globals import STATUS_EXIT, STATUS_CHANGE, DONE


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

    number_of_days = input("Please enter the number of days you want to travel: ")
    number_of_days = int(number_of_days)

    print("Please enter the places you want to visit in an ordered fashion after each prompt you'll get")
    print("Please pay attention to write every location ACCURATELY!")
    print("When you are done, please submit the word 'done' in LOWER CASE")
    while True:
        loc = input("Please enter a location you want to visit: ")
        if loc == DONE:
            break

        if not map_ops.is_location_exists(loc):
            print(f"Location {loc} does not exist - Please enter a new one")
            continue

        location_list.append(loc)

    print("These are the locations you entered:")
    for pl in location_list:
        print(pl)

    s_loc = input("Please choose one of the locations (By name) at which you want to sleep: ")
    for i in range(len(location_list)):
        if location_list[i] == s_loc:
            source = i

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
