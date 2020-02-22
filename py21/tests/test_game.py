"""
Test suite for the game class
"""
# ignore no-member in pylist because it's raised for the game parameters
# because pylint doesn't know about paramtools
# pylint: disable=no-member
import pytest
from py21 import Game, Player


def test_game_implementation():
    with pytest.raises(TypeError):
        Game([Player(100)], "str")
    # ensure that the parameters are updated properly
    rules = {"insurance_allowed": False,
             "blackjack_payout": 1.2}
    game = Game([Player(100)], rules)
    assert game.game_params.blackjack_payout == 1.2
    assert not game.game_params.insurance_allowed

    # ensure player limits are imposed
    rules = {"max_players": 2}
    with pytest.raises(AssertionError):
        Game([Player(100), Player(100), Player(100)], rules)
    with pytest.raises(AssertionError):
        Game([])

    # ensure surender throws and error if not allowed
    rules = {"surrender_allowed": False}

    def surender(**kwargs):
        return "SURRENDER"

    player = Player(100, strategy_func=surender)
    game = Game([player], rules=rules)
    with pytest.raises(ValueError):
        game.play_round()

    # test split and count implementations
    rules = {"shuffle_freq": 0}
    t_game = Game([Player(100)], rules=rules, test=True)
    t_game.play_round()
    assert t_game.player_list[0].bankroll == 110.0
    assert t_game.count == 3


def test_simulation():
    game = Game([Player(100)])
    game.simulate(10)
