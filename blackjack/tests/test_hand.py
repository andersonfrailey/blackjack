"""
Test suite for the Hand class
"""
import pytest
from blackjack import Card, Hand, Player


def test_hand_implementation():
    card_one = Card(2, "C")
    card_two = Card(3, "H")
    player = Player(100, None, None)
    Hand(card_one, player)

    with pytest.raises(TypeError):
        Hand("2C", card_two, player=player)
    with pytest.raises(TypeError):
        Hand(card_one, card_two, dict)


def test_add_card_two():
    card = Card(3, "C")
    player = Player(100, None)
    hand = Hand(card, player)
    with pytest.raises(TypeError):
        hand.add_card_two("2C")
    card_two = Card(2, "D")
    hand.add_card_two(card_two)


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
