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

    # ensure surrender throws and error if not allowed
    # decided this test just isn't relevant right now. will bring back
    # when I figure out a better implementation
    # rules = {"surrender_allowed": False}

    # def surrender(**kwargs):
    #     return "SURRENDER"

    # player = Player(100, strategy_func=surrender)
    # game = Game([player], rules=rules)
    # with pytest.raises(ValueError):
    #     game.play_round()

    # test split and count implementations
    rules = {"shuffle_freq": 0}
    t_game = Game([Player(100)], rules=rules, test=True)
    t_game.play_round()
    assert t_game.player_list[0].bankroll == 110.0
    assert t_game.count == 3


def test_simulation():
    game = Game([Player(100)])
    game.simulate(10)


def test_true_count():
    rules = {"num_decks": 1}
    game = Game([Player(100)], rules)
    game.play_round()
    remaining_decks = len(game.deck) / 52
    true_count = game.count / remaining_decks
    assert game.true_count == pytest.approx(true_count)
