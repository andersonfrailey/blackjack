"""
Test suite for the deck class
"""
import pytest
from blackjack import Card, Deck


def test_deck():
    with pytest.raises(TypeError):
        Deck("one")
    deck = Deck(3)
    assert len(deck) == 52 * 3
    while deck:
        card = deck.deal()
        assert isinstance(card, Card)
    with pytest.raises(IndexError):
        deck.deal()
