"""
Test the various strategies in strategies.py
"""
from py21.strategies import (basic_strategy, hit_to_seventeen,
                             minimum_bet, maximum_bet, decline_insurance,
                             accept_insurance)


def test_insurance():
    assert not decline_insurance()
    assert accept_insurance()


def test_basic_strategy(basic_player, basic_hand):
    action = basic_strategy(basic_player, basic_hand, 7, None)
    assert action == "DOUBLE-HIT"


def test_hit_to_seventeen(basic_player, basic_hand):
    action = hit_to_seventeen(basic_player, basic_hand)
    assert action == "HIT"


def test_basic_betting(basic_player):
    min_bet = minimum_bet(basic_player, 5, 500)
    assert min_bet == 5
    max_bet = maximum_bet(basic_player, 5, 500)
    assert max_bet == 500
