import json
from monopoly import Property, Area, Special_Square


def read_database_properties(database_file):
    """for properties"""
    with open(database_file, "r") as file_holder:
        data = json.load(file_holder)
        all_properties = []
        for area in data:
            new = Area(area)
            for one in data[area]:
                if one == "colour":
                    colour = data[area][one]
                    list = []
                    for i in colour.split(", "):
                        list.append(int(i))
                    new.set_colour(tuple(list))
                else:
                    row = data[area][one]
                    position = int(row["position"])
                    price = int(row["price"])
                    rent = int(row["rent"])
                    new_property = Property(one, position, price, rent, new)
                    all_properties.append(new_property)
        return all_properties


def read_database_special(database_file):
    with open(database_file, "r") as file_holder:
        data = json.load(file_holder)
        all_special = []
        for square in data:
            row = data[square]
            positions = row["position"]
            for one in positions.split(", "):
                new_special = Special_Square(square, int(one))
                all_special.append(new_special)
        return all_special


def sort_database(file1, file2):
    """Sorts properties by their positions"""
    list1 = read_database_properties(file1)
    list2 = read_database_special(file2)
    for one in list2:
        list1.append(one)
    dict = {}
    for property in list1:
        dict[property.position()] = property
    sorted_list = [dict[x] for x in range(0, len(dict))]
    return sorted_list


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
