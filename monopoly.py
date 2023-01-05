from monopoly_exeptions import WrongInputError, ZeroThrowsError, LessThanRequiredError
from random import randint

class Dices:
    def  __init__(self):
        self._throws = 1
        self._dublets = 0

    def check_dublet(self, throw1, throw2):
        if throw1 == throw2:
            self._dublets +=1
            self.add_throws()
    
    def dublets(self):
        return self._dublets

    def throws(self):
        return self._throws

    def add_throws(self, throws=1):
        self._throws += throws

    def set_zero_throws(self):
        self._throws = 0

    def throw_dices(self):
        if self._throws != 0:
            self._throws -= 1
            x, y = dice_throw()
            self.check_dublet(x, y)
            if self.dublets() != 3:
                self.move_forward(x + y)
            else:
                "To be written"
        else:
            raise ZeroThrowsError

def dice_throw():
    x = randint(1,6)
    y = randint(1,6)
    return [x, y]

class Player(Dices):
    
    def __init__(self, money):
        super().__init__()
        self._properties = []
        self._cards = []
        self._money = money
        self._position = 0
        self._pause = 0
        self._isactive = True

    def properties(self):
        return self._properties

    def set_properties(self, list):
        self._properties = list
        for property in list:
            property.buy(self)

    def add_property(self, property):
        self._properties.append(property)
        property.buy(self)

    def subtract_property(self, property):
        property.sell()
        new_list = []
        for one_property in self.properties():
            if one_property != property:
                new_list.append(one_property)
        self.set_properties(new_list)

    def value_of_properties(self):
        sum = 0
        for property in self.properties():
            sum += property.price()
        return sum
    
    def cards(self):
        return self._cards

    def set_cards(self, cards):
        self._cards = cards

    def add_card(self, card):
        self._cards.append(card)

    def subtract_card(self, card):
        new_cards = []
        for one_card in self.cards():
            if one_card != card:
                new_cards.append(one_card)
        self.set_cards(new_cards)

    def money(self):
        return self._money

    def set_money(self, value):
        self._money = value

    def add_money(self, value):
        self._money += value

    def subtract_money(self, value):
        self._money -= value

    def debit(self):
        return self._money < 0

    def position(self):
        return self._position

    def go_to(self, place):
        self._position = place.position()

    def move_forward(self, value):
        self._position += value

    def move_backward(self, value):
        self._position -= value

    def pause(self):
        return self._pause

    def set_pause(self, value):
        self._pause = value

    def isactive(self):
        return self._isactive

    def set_inactive(self):
        self._isactive = False

class Squere:
    def __init__(self, type, position):
        self._type = type
        self._position = position

    def type(self):
        return self._type

    def position(self):
        return self._position

class Property(Squere):
    def __init__(self, position, price, rent, area, owner=None, houses=0):
        super().__init__("property", position)
        self._price = price
        self._rent = rent
        self._area = area
        self._owner = owner
        self._houses = houses
        self._pledge = False

    def position(self):
        return self._position

    def price(self):
        return self._price

    def set_rent(self, rent):
        self._rent = rent

    def rent(self):
        return self._rent

    def pay_rent(self, player):
        player.subtract_money(self.rent())

    def area(self):
        return self._area

    def set_owner(self, owner):
        self._owner = owner

    def owner(self):
        return self._owner

    def set_pledge(self, value):
        if self.pledge() == value:
            raise WrongInputError(f"Pledge is already set {value}")
        else:
            self._pledge = value

    def pledge(self):
        return self._pledge

    def add_houses(self, number=1):
        self._houses += number

    def subtract_houses(self, number=1):
        if self._houses < number:
            raise LessThanRequiredError
        else:
            self._houses -= number

    def houses(self):
        return self._houses

    def sell(self):
        owner = self.owner()
        owner.add_money(self.price())
        self.set_owner(None)
        

    def buy(self, player):
        self.set_owner(player)
        player.subtract_money(self.price())

    def trade(self, other):
        """To be written"""
        pass

    def __str__(self):
        """To be written"""
        pass

class Area:
    def __init__(self, list_of_properties):
        self._list_of_properties = list_of_properties

    def check_if_fully_occupied(self, list):
        for property in self.area():
            if property not in list:
                return False
        return True

    def area(self):
        return self._list_of_properties

# class Special_Squere(Squere):
#     def __init__(self, position):
#         super().__init__("Special", position)

#     def do_action(self, player):
#         if self == "Więzienie":
#             action == (player)
#         if self == "Start":
#             start
#         if self == "Parking":
#             parking()
#         if self == "Sz"


