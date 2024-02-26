import pytest
from py21 import Card, Hand, Player, Game


@pytest.fixture(scope="session")
def basic_player():
    return Player(100)


@pytest.fixture(scope="session")
def basic_hand(basic_player, basic_game):
    hand = Hand(
        Card(5, "D"), player=basic_player, min_bet=5, max_bet=500,
        game_params=basic_game.game_params
    )
    hand.add_card_two(Card(6, "S"))
    return hand


@pytest.fixture(scope="session")
def basic_game():
    return Game([Player(100)])
