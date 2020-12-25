"""
Test suite for Player class
"""
import pytest
from py21 import Player


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


def test_settle_up():
    p = Player(95)
    setattr(p, "total_wagered", 5)
    # general payout
    hand_data = {
        "wager": 5,
        "insurance": False,
        "blackjack": False,
        "from_split": False,
        "result": "win"
    }
    p.settle_up(hand_data, 17, "win", 1, 1.5, False, 1, 0.5)
    assert p.bankroll == 105
    # blackjack payout
    hand_data = {
        "wager": 5,
        "insurance": False,
        "blackjack": True,
        "from_split": False,
        "result": "win"
    }
    p.settle_up(hand_data, 17, "win", 1, 1.5, False, 1, 0.5)
    assert p.bankroll == 117.5
    # split blackjack payout
    hand_data = {
        "wager": 5,
        "insurance": False,
        "blackjack": True,
        "from_split": True,
        "result": "win"
    }
    p.settle_up(hand_data, 17, "win", 1, 1.5, False, 1.5, 0.5)
    assert p.bankroll == 130
    # insurance payout
    hand_data = {
        "wager": 5,
        "insurance": True,
        "blackjack": False,
        "from_split": False,
        "result": "win"
    }
    p.settle_up(hand_data, 17, "loss", 1, 1.5, True, 1, 0.5)
    assert p.bankroll == 135
    # push
    hand_data = {
        "wager": 5,
        "insurance": False,
        "blackjack": False,
        "from_split": False,
        "result": "win"
    }
    p.settle_up(hand_data, 17, "push", 1, 1.5, False, 1, 0.5)
    assert p.bankroll == 140
    # surrender
    hand_data = {
        "wager": 5,
        "insurance": False,
        "blackjack": False,
        "from_split": False,
        "surrender": True,
        "result": "surrender"
    }
    p.settle_up(hand_data, 17, "surrender", 1, 1.5, False, 1, 0.5)
    assert p.bankroll == 142.5
