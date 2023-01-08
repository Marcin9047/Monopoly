import pytest
from monopoly import Squere, Property, Area, Player, Dices, dice_throw, Special_Squere

"""Tests for class Player"""

def test_player_init():
    player = Player(3000)
    assert len(player.properties()) == 0
    assert len(player.cards()) == 0
    assert player.money() == 3000
    assert player.position() == 0
    assert player.pause() == 0
    assert player.isactive() == True

def test_set_properties():
    player = Player(3000)
    Warszawa = Property(3, 230, 150, "Poland", None)
    Gdańsk = Property(3, 230, 150, "Poland", None)
    player.set_properties([Warszawa, Gdańsk])
    assert player.properties() == [Warszawa, Gdańsk]

def test_add_property():
    player = Player(3000)
    Warszawa = Property(3, 230, 150, "Poland", None)
    Gdańsk = Property(3, 230, 150, "Poland", None)
    Kraków = Property(3, 230, 150, "Poland", None)
    player.set_properties([Warszawa, Gdańsk])
    player.add_property(Kraków)
    assert player.properties() == [Warszawa, Gdańsk, Kraków]

def test_subtract_property():
    player = Player(3000)
    Warszawa = Property(3, 230, 150, "Poland", None)
    Gdańsk = Property(3, 230, 150, "Poland", None)
    player.set_properties([Warszawa, Gdańsk])
    player.subtract_property(Warszawa)
    assert player.properties() == [Gdańsk]
    assert Gdańsk.owner() == player
    assert Warszawa.owner() == None

def test_sum_of_value():
    Warszawa = Property(3, 230, 150, "Poland", None)
    Gdańsk = Property(3, 230, 150, "Poland", None)
    player = Player(3000)
    player.set_properties([Warszawa, Gdańsk])
    assert player.value_of_properties() == 460
    assert Warszawa.owner() == player

def test_cards():
    player = Player(3000)
    assert len(player.cards()) == 0

def test_add_card():
    player = Player(3000)
    player.add_card("Key")
    assert player.cards() == ["Key"]

def test_subtract_card():
    player = Player(3000)
    player.add_card("Key")
    player.subtract_card("Key")
    assert len(player.cards()) == 0

def test_money():
    player = Player(3000)
    assert player.money() == 3000

def test_set_money():
    player = Player(3000)
    player.set_money(5000)
    assert player.money() == 5000

def test_add_money():
    player = Player(3000)
    player.add_money(2000)
    assert player.money() == 5000

def test_subtract_money():
    player = Player(3000)
    player.subtract_money(2000)
    assert player.money() == 1000

def test_debit():
    player = Player(3000)
    player.subtract_money(4000)
    assert player.debit() == True

def test_position_diff():
    player = Player(3000)
    assert player.position() == 0

def test_go_to():
    player = Player(3000)
    Warszawa = Property(3, 230, 150, "Poland")
    player.go_to(Warszawa) 
    assert player.position() == 3

def test_move_forward():
    player = Player(3000)
    player.move_forward(4)
    assert player.position() == 4

def test_move_backward():
    player = Player(3000)
    Warszawa = Property(3, 230, 150, "Poland")
    player.go_to(Warszawa)
    player.move_backward(2)
    assert player.position() == 1

def test_pause():
    player = Player(3000)
    assert player.pause() == 0

def test_set_pouse():
    player = Player(3000)
    player.set_pause(2)
    assert player.pause() == 2

def test_isactive():
    player = Player(3000)
    assert player.isactive() == True

def test_set_inactive():
    player = Player(3000)
    player.set_inactive()
    assert player.isactive() == False

"""Tests for class Square """

def test_squere():
    """Test of squere class"""
    Warszawa = Property(3, 230, 150, "Poland", "admin")
    assert Warszawa.type() == "property"
    assert Warszawa.position() == 3

"""Tests for class Property"""

def test_property_init():
    """Test of property class with all of the atributes writen"""
    Warszawa = Property(3, 230, 150, "Poland", "admin", 5)
    assert Warszawa.position() == 3
    assert Warszawa.price() == 230
    assert Warszawa.rent() == 150
    assert Warszawa.area() == "Poland"
    assert Warszawa.owner() == "admin"
    assert Warszawa.houses() == 5

def test_property_init_no_owner():
    """Test when owner and houses are not given. Program should give owner=None and houses=0"""
    Warszawa = Property(3, 230, 150, "Poland")
    assert Warszawa.position() == 3
    assert Warszawa.price() == 230
    assert Warszawa.area() == "Poland"
    assert Warszawa.owner() is None
    assert Warszawa.houses() == 0

def test_set_rent():
    Warszawa = Property(3, 230, 150, "Poland")
    Warszawa.set_rent(300)
    assert Warszawa.rent() == 300

def test_pay_rent():
    Warszawa = Property(3, 230, 150, "Poland")
    player = Player(300)
    Warszawa.pay_rent(player)
    assert player.money() == 150

def test_set_owner():
    Warszawa = Property(3, 230, 150, "Poland")
    player = Player(300)
    Warszawa.set_owner(player)
    assert Warszawa.owner() == player

def test_pledge():
    Warszawa = Property(3, 230, 150, "Poland")
    assert Warszawa.pledge() == False

def test_set_pledge():
    Warszawa = Property(3, 230, 150, "Poland")
    Warszawa.set_pledge(True)
    assert Warszawa.pledge() == True

def test_add_house():
    Warszawa = Property(3, 230, 150, "Poland")
    Warszawa.add_houses()
    assert Warszawa.houses() == 1

def test_add_houses():
    Warszawa = Property(3, 230, 150, "Poland")
    Warszawa.add_houses(3)
    assert Warszawa.houses() == 3

def test_subtract_houses():
    Warszawa = Property(3, 230, 150, "Poland")
    Warszawa.add_houses(3)
    Warszawa.subtract_houses(2)
    assert Warszawa.houses() == 1

def test_buy_property():
    Warszawa = Property(3, 230, 150, "Poland")
    player = Player(300)
    Warszawa.buy(player)
    assert Warszawa.owner() == player
    assert player.money() == 70

def test_sell_property():
    Warszawa = Property(3, 230, 150, "Poland")
    player = Player(300)
    Warszawa.buy(player)
    Warszawa.sell()
    assert Warszawa.owner() == None
    assert player.money() == 300

"""Tests for class Area"""

def test_area_init():
    Warszawa = Property(3, 230, 150, "Poland")
    Gdańsk = Property(2,200, 150, "Poland")
    Europa = Area([Warszawa, Gdańsk])
    assert Europa.area() == [Warszawa, Gdańsk]

def test_check_if_fully_occupied():
    Warszawa = Property(3, 230, 150, "Poland")
    Gdańsk = Property(2,200, 150, "Poland")
    Europa = Area([Warszawa, Gdańsk])
    assert Europa.check_if_fully_occupied([Warszawa]) == False
    assert Europa.check_if_fully_occupied([Gdańsk, Warszawa]) == True

"""Tests for class Dices"""

def test_init():
    player = Player(300)
    assert player.throws() == 1
    assert player.dublets() == 0

def test_check_dublet():
    player = Player(300)
    player.check_dublet(3, 3)
    assert player.dublets() == 1
    assert player.throws() == 2

def test_add_throws():
    player = Player(300)
    player.add_throws(3)
    assert player.throws() == 4

def test_set_zero_throws():
    player = Player(300)
    player.add_throws(3)
    player.set_zero_throws()
    assert player.throws() == 0

def test_dice_throw():
    """test if randint returns two intiger numbers"""
    list = dice_throw()
    assert len(list) == 2
    for number in list:
        assert isinstance(number, int)

def test_throw_dices():
    player = Player(300)
    player.throw_dices()
    assert player.position() != 0

"""Tests for class Special_squere"""

def test_init():
    prison = Special_Squere(7)
    start = Special_Squere(15)
    parking = Special_Squere(27)
    go_to_prison = Special_Squere(46)
    airport = Special_Squere(52)
    assert prison.position() == 7
    assert start.position() == 15

def test_do_Start_action():
    prison = Special_Squere(7)
    start = Special_Squere(15)
    parking = Special_Squere(27)
    go_to_prison = Special_Squere(46)
    airport = Special_Squere(52)
    player = Player(300)
    start.do_action(player)
    assert player.money() == 600
