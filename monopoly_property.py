from monopoly import Square
from monopoly_exeptions import *


class Property(Square):
    """Class with the parameters of property on the board
    Super class: Square
    Methods to: pay rent, buy/sell, increase/decrease rent, buy/sell houses,
    set pladge and set house cost
    """
    def __init__(self, name, position, price, rent, area, owner=None, house=0):
        """
        name: string
        position: intiger
        price: intiger
        rent: intiger
        area: Area class object
        owner=None: Player class object
        houses=None: intiger

        Gives type:"property" and position to Area class
        adds property to area and sets house cost
        """
        super().__init__("property", position)
        self._name = name
        self._price = price
        self._rent = rent
        self._area = area
        self._owner = owner
        self._houses = house
        self._pledge = False
        self._area.add_property(self)
        self.set_house_cost()

    def name(self):
        return self._name

    def position(self):
        return self._position

    def price(self):
        return self._price

    def increase_rent(self, rent):
        self._rent += rent

    def decrease_rent(self, rent):
        self._rent -= rent

    def rent(self):
        return self._rent

    def pay_rent(self, player):
        """
        Pays rent of the property to the owner or just
        subtract money if property is pladged
        input: Player class object
        reaises NotEnoughtMoneyError if player is unable to pay
        """
        value = self.rent()
        if player.check_debit(value):
            raise NotEnoughtMoneyError
        player.subtract_money(value)
        if self.pledge() is False:
            self.owner().add_money(value)

    def area(self):
        return self._area

    def set_owner(self, owner):
        self._owner = owner

    def owner(self):
        return self._owner

    def set_pledge(self, value=True):
        """Sets player pladge by given value
        value=True: True/False
        if value same as pladge raises WrongInputError
        If value == True gives half of the property price to the player
        if value == False subtract same money from owner
        """
        if self.pledge() == value:
            raise WrongInputError
        else:
            pld_money = self.price() // 2
            if value:
                self.owner().add_money(pld_money)
                self._pledge = True
            else:
                self.owner().subtract_money(pld_money)
                self._pledge = True

    def pledge(self):
        return self._pledge

    def set_house_cost(self):
        """Sets house cost base on the side of the board"""
        side = (self.position() // 10) + 1
        self._house_cost = 100 * side

    def check_house_cost(self):
        return self._house_cost

    def buy_house(self):
        """Method to buy house ona property if
        player is an owner of every property in area
            if not: rases NotOwnerOfEveryError
            if houses on property equal 4: property is full
            raises HousesFullError
            raises NotEnoughtMoneyError if player cant afford to buy a house
        """
        if not self.area().check_if_fully_occupied(self.owner()):
            raise NotOwnerOfEveryError
        if self.houses() == 4:
            raise HousesFullError
        cost = self.check_house_cost()
        if self.owner().check_debit(cost):
            raise NotEnoughtMoneyError
        for property in self.area().area_properties():
            if property.houses() < self.houses():
                raise HousesNotEquallyError
        self._houses += 1
        increase = (5 * self.rent()) // 10
        if self.houses() <= 2:
            self.owner().subtract_money(cost)
            self.increase_rent(increase)
        else:
            self.owner().subtract_money(2 * cost)
            self.increase_rent(2 * increase)

    def sell_house(self):
        """Method to sell house on property.
        Raises ZeroHousesError if there is already no houses on property
        """
        if self._houses == 0:
            raise ZeroHousesError
        else:
            self._houses -= 1
            self.owner().add_money(self.check_house_cost())

    def houses(self):
        return self._houses

    def sell(self):
        """Method to sell property"""
        owner = self.owner()
        owner.add_money(self.price())
        self.set_owner(None)
        owner.subtract_property(self)

    def buy(self, player):
        """Method to buy property
        input: Player class object
        raises NotEnoughtMoneyError if player can afford to buy this property
        """
        if player.check_debit(self.price()):
            raise NotEnoughtMoneyError
        self.set_owner(player)
        player.subtract_money(self.price())
        player.add_property(self)
