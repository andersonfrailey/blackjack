"""
Test suite for the game class
"""
import pytest
from blackjack import Game


def test_game_implementation():
    with pytest.raises(TypeError):
        Game(6, [], "str")
    # ensure that the parameters are updated properly
    game = Game(6, [], {"blackjack_payout": [{"value": 1.2}]})
    assert game.game_params.blackjack_payout == 1.2
