import json
from monopoly import Squere, Property, Area, Player, Dices, dice_throw

"""for properties"""

def read_database(database_file):
    with open(database_file, "r") as file_holder:
        data = json.load(file_holder)
        for area in data:
            list_of_properties = []
            for property in data[area]:
                row = data[area][property]
                position = row["position"]
                price = row["price"]
                rent = row["rent"]
                property = Property(position, price, rent, area)
                list_of_properties.append(property)
            area = Area(list_of_properties)

def write_game_logs(log_file, property):
    with open(log_file, "w") as file_holder:
        name, position, price, rent, area, owner, houses = property
        data = {
            "name": name,
            "position": position,
            "price": price,
            "rent": rent,
            "area": area,
            "owner": owner,
            "houses": houses
                }
        file_holder[Area][property] = data


read_database("/home/marcin9047/Programowanie - dom/monopoly/database.json")
