"""
Test Suite for Card class
"""
import pytest
from py21 import Card


def test_card_implementation():
    with pytest.raises(ValueError):
        Card(15, "C")
    with pytest.raises(ValueError):
        Card(2, "F")


def test_add_cards():
    card_one = Card(2, "C")
    card_two = Card(3, "D")
    assert isinstance(card_one + card_two, int)
    with pytest.raises(TypeError):
        card_one + []
