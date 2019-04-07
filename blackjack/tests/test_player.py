"""
Test suite for Player class
"""
import pytest
from blackjack import Player


def test_wager():
    def bad_min_wager(player, min_bet, max_bet):
        return 1

    def bad_max_wager(player, min_bet, max_bet):
        return 1000

    p = Player(100, wager_func=bad_min_wager)
    with pytest.raises(AssertionError):
        p.wager(min_bet=5, max_bet=500)

    p = Player(100, wager_func=bad_max_wager)
    with pytest.raises(AssertionError):
        p.wager(min_bet=5, max_bet=500)

    with pytest.raises(AssertionError):
        p.wager(min_bet=5, max_bet=5000)
