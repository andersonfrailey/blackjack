"""
Functions for determining if a player wins a side bet
Checks poker hands and in between bets
"""


def royal_flush(hand):
    """
    Check for a royal flush

    Parameters
    ----------
    hand: The player and dealer's cards

    Returns
    -------

    """
    royal = True
    rank = 14
    suit = hand[0].suit
    for card in hand:
        if card.rank == rank and card.suit == suit:
            rank -= 1
        else:
            royal = False
            break
    if royal:
        return True, 'Royal Flush'
    else:
        return False, 'Loss'


def straight_flush(hand):
    """
    Check for straight flush

    Parameters
    ----------
    hand: The player and dealer's cards

    Returns
    -------

    """
    st_fl = True
    # Set the top rank and suit
    rank = hand[0].rank
    suit = hand[0].suit
    # Check each card
    for card in hand:
        if card.rank == rank and card.suit == suit:
            rank -= 1
        else:
            st_fl = False
            break
    if st_fl:
        return True, 'Straight Flush'
    else:
        return False, 'Loss'


def flush(hand):
    """
    Check if there is a flush

    Parameters
    ----------
    hand: The player and dealer's cards

    Returns
    -------

    """
    # See if all the suits are the same
    if hand[0].suit == hand[1].suit and hand[1].suit == hand[2].suit:
        return True, 'Flush'
    else:
        return False, 'Loss'


def straight(hand):
    """
    Check for a straight

    Parameters
    ----------
    hand: The player and dealer's cards

    Returns
    -------

    """
    # Set start rank
    rank = hand[0].rank
    st = True
    for card in hand:
        if card.rank == rank:
            rank -= 1
        else:
            st = False
            break
    if st:
        return True, 'Straight'
    else:
        return False, 'Loss'


def three(hand):
    """
    Check three of a kind

    Parameters
    ----------
    hand: The player and dealer's cards

    Returns
    -------

    """
    # Check if all ranks are equal
    if hand[0].rank == hand[1].rank and hand[1].rank == hand[2].rank:
        return True, 'Three of a Kind'
    else:
        return False, 'Loss'


def poker_hands(hand):
    """
    Checks the poker hands and returns either a hand or loss

    Parameters
    ----------
    hand: The player and dealer's cards

    Returns
    -------

    """
    found = False
    result = 'loss'
    # Check each hand possibility until one is found
    if not found:
        found, result = royal_flush(hand)
    if not found:
        found, result = straight_flush(hand)
    if not found:
        found, result = flush(hand)
    if not found:
        found, result = straight(hand)
    if not found:
        found, result = three(hand)
    return result


def spread(card_one, card_two, dealer):
    """
    Determines the spread of an in between

    Parameters
    ----------
    card_one
    card_two
    dealer

    Returns
    -------
    0 if all number are the same
    1 if the spread is one
    2 if the spread is two
    3 if the spread is three
    4 if the spread is four or greater

    """
    first = card_one.rank - dealer.rank
    second = dealer.rank - card_two.rank
    sp = max([first, second])
    # If the spread is greater than four, only return four
    if sp >= 4:
        return '4+'
    else:
        return sp


def in_between(card_one, card_two, dealer):
    """
    Checks to see if the dealer's cards are in between the players
    Parameters
    ----------
    card_one: Player's largest card
    card_two: Player's smallest card
    dealer: Dealer's card

    Returns
    -------
    The distance between the cards or number indicating a loss

    """
    # Only call the spread function if the dealer's card is in between
    if card_one.rank >= dealer.rank >= card_two.rank:
        return spread(card_one, card_two, dealer)
    else:
        return 'Loss'


def side_bets(card_one, card_two, dealer):
    """

    Parameters
    ----------
    card_one: Player's first card
    card_two: Player's second card
    dealer: dealer's card

    Returns
    -------
    Result of both poker and in between side bets

    """
    poker_hand = [card_one, card_two, dealer]
    final_hand = sorted(poker_hand, key=lambda x: x.rank, reverse=True)
    poker = poker_hands(final_hand)
    inbtwn_hand = [card_one, card_two]
    final_inbtwn = sorted(inbtwn_hand, key=lambda x: x.rank, reverse=True)
    inbtwn = in_between(final_inbtwn[0], final_inbtwn[1], dealer)

    return poker, inbtwn
