import pytest
from py21 import Card, Hand, Player


@pytest.fixture(scope="session")
def basic_player():
    return Player(100)


@pytest.fixture(scope="session")
def basic_hand(basic_player):
    hand = Hand(Card(5, "D"), player=basic_player, min_bet=5, max_bet=500)
    hand.add_card_two(Card(6, "S"))
    return hand
