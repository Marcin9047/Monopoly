import json
from monopoly import Squere, Property, Area, Player, Dices, dice_throw

"""for properties"""

def read_database(database_file):
    with open(database_file, "r") as file_holder:
        data = json.load(file_holder)
        for number, properties in enumerate(data):
            list_of_properties = []
            for one in properties:
                name, position, price, rent, area = one
                name = Property(position, price, rent, area)
                list_of_properties.append(name)
            number = Area(list_of_properties)

def write_game_logs(log_file):
    with open(log_file, "w") as file_holder:
        for area in Area:
            file_holder[area] = [
            for property in Property:
                position, price, rent, area, owner, houses = str(property)
                    ]