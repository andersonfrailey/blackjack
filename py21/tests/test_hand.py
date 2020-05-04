"""
Test suite for the Hand class
"""
import pytest
from py21 import Card, Hand, Player


def test_hand_implementation():
    card_one = Card(2, "C")
    card_two = Card(3, "H")
    player = Player(100, None, None)
    Hand(card_one, player)

    with pytest.raises(TypeError):
        Hand("2C", card_two, player=player)
    with pytest.raises(TypeError):
        Hand(card_one, card_two, dict)

    hand = Hand(Card(12, "H"))
    hand.add_card_two(Card(5, "S"))
    assert hand.total == 15
    assert not hand.soft
    hand.add_card(Card(4, "D"))
    assert hand.total == 19
    hand.add_card(Card(10, "S"))
    assert hand.bust


def test_add_card_two():
    card = Card(3, "C")
    player = Player(100, None)
    hand = Hand(card, player)
    with pytest.raises(TypeError):
        hand.add_card_two("2C")
    card_two = Card(2, "D")
    hand.add_card_two(card_two)
    assert hand.total == 5


def test_comparisons():
    hand = Hand(Card(2, "H"), player=Player(100, None, None),
                min_bet=5, max_bet=500)
    hand.add_card_two(Card(3, "D"))
    with pytest.raises(TypeError):
        hand > 3
    with pytest.raises(TypeError):
        hand < 3
    with pytest.raises(TypeError):
        hand == 3


def test_blackjack():
    hand = Hand(Card(14, "C"))
    hand.add_card_two(Card(10, "D"))
    assert hand.blackjack
    hand = Hand(Card(12, "C"))
    hand.add_card_two(Card(14, "S"))
    assert hand.blackjack


def test_soft():
    hand = Hand(Card(14, "C"))
    hand.add_card_two(Card(14, "D"))
    assert hand.soft
    assert hand.total == 12
    hand.add_card(Card(14, "D"))
    assert hand.soft
    assert hand.total == 13
    hand.add_card(Card(10, "H"))
    assert not hand.soft
    assert hand.total == 13

    hand = Hand(Card(5, "D"))
    hand.add_card_two(Card(14, "S"))
    assert hand.soft
    assert hand.total == 16

    hand = Hand(Card(6, "H"))
    hand.add_card_two(Card(3, "H"))
    hand.add_card(Card(14, "H"))
    assert hand.soft
    assert hand.total == 20

    hand = Hand(Card(14, "D"))
    hand.add_card_two(Card(3, "H"))
    hand.add_card(Card(10, "C"))
    assert not hand.soft
    assert hand.total == 14
    hand.add_card(Card(14, "S"))
    assert hand.total == 15
    assert not hand.soft

    hand = Hand(Card(3, "D"))
    hand.add_card_two(Card(6, "S"))
    hand.add_card(Card(2, "H"))
    hand.add_card(Card(14, "S"))
    assert not hand.soft
    assert hand.total == 12

    # edge case. you're delt a bunch of aces
    hand = Hand(Card(14, "S"))
    hand.add_card_two(Card(14, "D"))
    for _ in range(9):
        hand.add_card(Card(14, "S"))
    assert hand.total == 21
    assert hand.num_hard_aces == 1
    hand.add_card(Card(14, "S"))
    assert not hand.bust
    assert hand.total == 12
    assert not hand.soft
    assert hand.num_hard_aces == 0
