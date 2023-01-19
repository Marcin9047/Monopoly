import json
from monopoly import Property, Area, Special_Square


class Database:
    def __init__(self, property_file, special_file):
        self.property_file = property_file
        self.special_file = special_file

    def read_database_properties(self):
        """for properties"""
        database_file = self.property_file
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
                        pos = int(row["position"])
                        price = int(row["price"])
                        rent = int(row["rent"])
                        new_property = Property(one, pos, price, rent, new)
                        all_properties.append(new_property)
            self.properties = all_properties

    def read_database_special(self):
        database_file = self.special_file
        with open(database_file, "r") as file_holder:
            data = json.load(file_holder)
            all_special = []
            for square in data:
                row = data[square]
                positions = row["position"]
                if len(row) == 2:
                    value = row["value"]
                else:
                    value = None
                for one in positions.split(", "):
                    new_special = Special_Square(square, int(one), value)
                    all_special.append(new_special)
            self.special = all_special

    def sort_database(self):
        """Sorts properties by their positions"""
        list1 = self.property_file
        list2 = self.special_file
        self.read_database_properties()
        self.read_database_special()
        list1 = self.properties
        list2 = self.special
        for one in list2:
            list1.append(one)
        dict = {}
        for property in list1:
            dict[property.position()] = property
        sorted_list = [dict[x] for x in range(0, len(dict))]
        return sorted_list
