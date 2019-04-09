"""
Test suite for the game class
"""
import pytest
from blackjack import Game, Player


def test_game_implementation():
    with pytest.raises(TypeError):
        Game(6, [Player(100)], "str")
    # ensure that the parameters are updated properly
    rules = {"insurance_allowed": False,
             "blackjack_payout": 1.2}
    game = Game(6, [Player(100)], rules)
    assert game.game_params.blackjack_payout == 1.2
    assert not game.game_params.insurance_allowed

    # ensure player limits are imposed
    rules = {"max_players": 2}
    with pytest.raises(AssertionError):
        Game(1, [Player(100), Player(100), Player(100)], rules)
    with pytest.raises(AssertionError):
        Game(1, [])


def test_simulation():
    game = Game(1, [Player(100)])
    game.simulate(10)
