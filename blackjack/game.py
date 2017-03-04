"""
Class to create and shuffle the deck and deal the cards
"""

from deck import Deck
from sidebets import *
from utils import *


class Game(object):

    def __init__(self):
        """

        Parameters
        ----------
        decks: Number of decks
        players: number of players
        """
        # Parameters needed to play game
        self.num_decks = None
        self.deck = None
        self.cut = None
        self.card_count = 0
        self.players = None
        self.num_hands = None
        self.hands_played = 0

        # Player lists used in the game
        self.players_list = []
        self.final_list = []

        # Initiate the dealer
        self.dealer = {'total': 0, 'soft': False, 'taken': 0}

        # Initiate data collection
        self.data = Data()

    @staticmethod
    def check_ace(card):
        """
        Checks if a card is an ace or not
        Parameters
        ----------
        card: Card object

        Returns
        -------
        True if ace, false otherwise

        """
        if card.rank == 14:
            return True
        else:
            return False

    @staticmethod
    def check_face(card):
        """
        Check if card is a face card
        Parameters
        ----------
        card

        Returns
        -------
        True if face card, false otherwise

        """
        if 11 <= card.rank <= 13:
            return True
        else:
            return False

    @staticmethod
    def face_card():
        """
        Returns 10 to replace value of a face card
        """
        return 10

    def count(self, card):
        """
        Count cards
        If the card value is between 2 and 6, add one to count
        If the card value is 10 or an ace, subtract one to count
        Otherwise, add nothing

        Parameters
        ----------
        card: card object

        Returns
        -------
        None

        """
        if 2 <= card.rank <= 6:
            self.card_count += 1
        elif card.rank >= 10:
            self.card_count -= 1

    @staticmethod
    def bust(hand):
        """
        Determines if a player busted

        Parameters
        ----------
        hand

        Returns
        -------

        """
        if hand['total'] > 21:
            return True
        else:
            return False

    def hit(self, hand):
        """
        Add one card to a hand

        Parameters
        ----------
        hand

        Returns
        -------

        """
        card = self.deck.deal()
        start_count = self.card_count
        self.data.card_freq(card, self.card_count, self.players,
                            self.hands_played, self.num_decks)
        self.count(card)
        start = hand['total']
        if self.check_ace(card):
            if hand['total'] <= 10:
                hand['total'] += 11
                hand['ace val'] = 11
            else:
                hand['total'] += 1
                hand['ace val'] = 1
        elif self.check_face(card):
            hand['total'] += self.face_card()
        else:
            hand['total'] += card.rank
        hand['taken'] += 1
        if hand['total'] > 21 and hand['soft'] and hand['ace val'] == 11:
            hand['total'] -= 10
            hand['ace val'] = 1
        self.data.hit_result(start, hand['total'], start_count, self.num_decks)
        return self.bust(hand)

    def check_blackjack(self, hand):
        """
        Check if player or dealer has blackjack

        Parameters
        ----------
        hand

        Returns
        -------
        True if player has blackjack, false otherwise

        """
        # If card one is of value ten check for an ace in card two
        if 10 <= hand['card one'].rank <= 13:
            if self.check_ace(hand['card two']):
                return True
            else:
                return False
        # If card one is an ace, check if card two is worth ten
        elif self.check_ace(hand['card one']):
            if 10 <= hand['card two'].rank <= 13:
                return True
            else:
                return False
        # If neither are the case, return false
        else:
            return False

    def split_logic(self, card, pos):
        """
        Contains logic for creating a split hand
        Parameters
        ----------
        card

        Returns
        -------
        A complete hand

        """
        # Create new hand to be returned
        hand = {'total': 0, 'taken': 0, 'card one': card, 'bust': False,
                'pos': pos}
        hand['soft'] = self.check_ace(card)
        if hand['soft']:
            hand['total'] = 11
            hand['ace val'] = 11
        else:
            hand['total'] = card.rank
        card_two = self.deck.deal()
        self.data.card_freq(card_two, self.card_count, self.players,
                            self.hands_played, self.num_decks)
        hand['card two'] = card_two
        self.count(card_two)
        ace = self.check_ace(card_two)
        if ace and not hand['soft']:
            hand['soft'] = True
            hand['total'] += 11
            hand['ace val'] = 11
        elif ace and hand['soft']:
            hand['total'] += 1
            hand['ace val'] = 1
        elif self.check_face(card_two):
            hand['total'] += 10
        else:
            hand['total'] += card_two.rank
        # Check if hand can be split
        if hand['card one'].rank == hand['card two'].rank:
            hand['split'] = True
        else:
            hand['split'] = False
        hand['start'] = hand['total']
        return hand

    def split_hand(self, hand, d_up):
        """
        Determines action to take based on card values and dealer up card
        Parameters
        ----------
        hand: Player's cards and total
        d_up: Dealer's up card

        Returns
        -------

        """
        # Always split aces and eights
        if hand['card one'].rank == 14 or hand['card one'].rank == 8:
            # Create and play with two new hands
            hand_one = self.split_logic(hand['card one'], hand['pos'])
            self.play_hand(hand_one, d_up)
            hand_two = self.split_logic(hand['card two'], hand['pos'])
            self.play_hand(hand_two, d_up)
        elif hand['card one'].rank == 9:
            if not d_up == 7 and 10 <= d_up <= 14:
                hand_one = self.split_logic(hand['card one'], hand['pos'])
                self.play_hand(hand_one, d_up)
                hand_two = self.split_logic(hand['card two'], hand['pos'])
                self.play_hand(hand_two, d_up)
            else:
                hand['split'] = False
                self.play_hand(hand, d_up)
        elif (2 <= hand['card one'].rank <= 3 or
              6 <= hand['card one'].rank <= 7):
            if 2 <= d_up <= 7:
                hand_one = self.split_logic(hand['card one'], hand['pos'])
                self.play_hand(hand_one, d_up)
                hand_two = self.split_logic(hand['card two'], hand['pos'])
                self.play_hand(hand_two, d_up)
            else:
                hand['split'] = False
                self.play_hand(hand, d_up)
        elif hand['card one'].rank == 4:
            if 5 <= d_up <= 6:
                hand_one = self.split_logic(hand['card one'], hand['pos'])
                self.play_hand(hand_one, d_up)
                hand_two = self.split_logic(hand['card two'], hand['pos'])
                self.play_hand(hand_two, d_up)
            else:
                hand['split'] = False
                self.play_hand(hand, d_up)
        # Never split tens
        else:
            hand['split'] = False
            self.play_hand(hand, d_up)

    def hard_total(self, hand, d_up):
        """
        Determines which action to take based on player's hand total and the
        dealer's up card

        Parameters
        ----------
        hand: Player's cards and total
        d_up: Dealer's up card

        Returns
        -------
        Bust, Stand

        """
        # Always stand if total is above 17
        if hand['total'] >= 17:
            return False, True
        elif 4 <= hand['total'] <= 8:
            return self.hit(hand), False
        elif 13 <= hand['total'] <= 16:
            if 2 <= d_up <= 6:
                return False, True
            elif d_up >= 7:
                return self.hit(hand), False
        elif hand['total'] == 12:
            if 4 <= d_up <= 6:
                return False, True
            else:
                return self.hit(hand), False
        elif hand['total'] == 11:
            if 4 <= d_up <= 6:
                return self.hit(hand), False
            # When doubling down call hit and return stand as True
            else:
                return self.hit(hand), True
        elif hand['total'] == 10:
            if 10 <= d_up <= 14:
                return self.hit(hand), False
            else:
                return self.hit(hand), True
        elif hand['total'] == 9:
            if 3 <= d_up <= 6:
                return self.hit(hand), True
            else:
                return self.hit(hand), False
        else:
            return self.hit(hand), False

    def soft_total(self, hand, d_up):
        """
        Logic for playing a soft hand
        Parameters
        ----------
        hand
        d_up

        Returns
        -------
        bust, stand

        """
        if hand['total'] >= 19:
            return False, True
        elif hand['total'] == 18:
            if 3 <= d_up <= 6:
                return self.hit(hand), True
            elif 9 < d_up < 14:
                return self.hit(hand), False
            else:
                return False, True
        elif hand['total'] == 17:
            if 3 <= d_up <= 6:
                return self.hit(hand), True
            else:
                return self.hit(hand), False
        elif hand['total'] == 15 or hand['total'] == 16:
            if 4 <= d_up <= 6:
                return self.hit(hand), True
            else:
                return self.hit(hand), False
        else:
            if d_up == 5 or d_up == 6:
                return self.hit(hand), True
            else:
                return self.hit(hand), False

    def dealer_play(self, dealer):
        """
        Contains the dealer's strategy. Assumes dealer stands on soft 17

        Returns
        -------
        Tuple where the first element is a boolean indicating if the dealer
        busted and the second is a boolean indicating if the dealer is standing

        """
        if dealer['total'] >= 17:
            return False, True
        else:
            return self.hit(dealer), False

    def deal_hand(self):
        """
        Deal initial hands

        Returns
        -------
        None

        """

        # Give each player and the dealer their first card
        for player in range(self.players):
            player_dict = {'total': 0, 'pos': player, 'start': 0}
            card = self.deck.deal()
            self.data.card_freq(card, self.card_count, self.players,
                                self.hands_played, self.num_decks)
            self.count(card)
            player_dict['card one'] = card
            player_dict['soft'] = self.check_ace(card)
            if self.check_ace(card):
                player_dict['total'] = 11
                player_dict['ace val'] = 11
            elif self.check_face(card):
                player_dict['total'] += self.face_card()
            else:
                player_dict['total'] = card.rank
            self.players_list.append(player_dict)

        card = self.deck.deal()
        self.data.card_freq(card, self.card_count, self.players,
                            self.hands_played, self.num_decks)
        self.count(card)
        self.dealer['card one'] = card
        self.dealer['soft'] = self.check_ace(card)
        if self.dealer['soft']:
            self.dealer['total'] = 11
            self.dealer['ace val'] = 11
        elif self.check_face(card):
            self.dealer['total'] += self.face_card()
        else:
            self.dealer['total'] += card.rank

        # Give each player and dealer a second card
        for player in self.players_list:
            card = self.deck.deal()
            self.data.card_freq(card, self.card_count, self.players,
                                self.hands_played, self.num_decks)
            self.count(card)
            player['card two'] = card
            ace = self.check_ace(card)
            if ace and not player['soft']:
                player['soft'] = True
                player['total'] += 11
                player['ace val'] = 11
            elif ace and player['soft']:
                player['total'] += 1
            elif self.check_face(card):
                player['total'] += self.face_card()
            else:
                player['total'] += card.rank
            # Check if a hand can be split
            if player['card one'] == player['card two']:
                player['split'] = True
            else:
                player['split'] = False
            player['start'] = player['total']
            player['taken'] = 0
            player['bust'] = False

        # Give dealer second card
        card = self.deck.deal()
        self.data.card_freq(card, self.card_count, self.players,
                            self.hands_played, self.num_decks)
        self.dealer['card two'] = card
        ace = self.check_ace(card)
        if ace and not self.dealer['soft']:
            self.dealer['soft'] = True
            self.dealer['total'] += 11
            self.dealer['ace val'] = 11
        elif ace:
            self.dealer['total'] += 1
        elif self.check_face(card):
            self.dealer['total'] += self.face_card()
        else:
            self.dealer['total'] += card.rank
        self.dealer['start'] = self.dealer['total']

    def play_hand(self, hand, d_up):
        """
        Calls strategy functions
        Appends each hand passed through to the final list
        Returns
        -------

        """
        self.hands_played += 1
        hand['start'] = hand['total']
        bust = False
        stand = False
        while not bust and not stand:
            if hand['split']:
                self.split_hand(hand, d_up)
                break
            elif not hand['soft'] and not hand['split']:
                bust, stand = self.hard_total(hand, d_up)
            elif hand['soft'] and not hand['split']:
                bust, stand = self.soft_total(hand, d_up)
        hand['bust'] = bust
        if not hand['split']:
            self.final_list.append(hand)

    def play_round(self):
        """
        Deal out all of the hands, then call play hand function with each hand
        in player list
        Returns
        -------

        """
        all_bust = True
        num_blackjacks = 0
        self.deal_hand()
        self.dealer['blackjack'] = self.check_blackjack(self.dealer)
        dealer_up = self.dealer['card one'].rank
        # If the dealer has an ace showing, add blackjack result to data
        if dealer_up == 14:
            if self.dealer['blackjack']:
                self.data.insurance(1, self.num_decks)
            else:
                self.data.insurance(0, self.num_decks)
        # Check all side bets and blackjack
        for hand in self.players_list:
            poker, inbtwn = side_bets(hand['card one'], hand['card two'],
                                      self.dealer['card one'])
            hand['poker'] = poker
            hand['inbtwn'] = inbtwn
            hand['blackjack'] = self.check_blackjack(hand)
            self.data.collect_side(poker, inbtwn, self.card_count,
                                   self.num_decks)
        # Play each hand if dealer doesn't have blackjack
        if not self.dealer['blackjack']:
            for hand in self.players_list:
                self.play_hand(hand, dealer_up)
                if not hand['bust']:
                    all_bust = False
                if hand['blackjack']:
                    num_blackjacks += 1
        # Only count the dealer's second card after all players play
        self.count(self.dealer['card two'])
        # Only play the dealer's hand if at least one player didn't bust
        if not all_bust and num_blackjacks != len(self.players_list):
            d_bust = False
            d_stand = False
            while not d_bust and not d_stand:
                d_bust, d_stand = self.dealer_play(self.dealer)
            self.dealer['bust'] = d_bust
        else:
            self.dealer['bust'] = False
        # Call compare function to see which players won
        if not self.dealer['blackjack']:
            self.compare(self.final_list)
        else:
            self.compare(self.players_list)
        # Clear player and final lists after the round is complete.
        del self.players_list[:]
        del self.final_list[:]
        # Clear the dealer dictionary
        self.dealer = {'total': 0, 'soft': False, 'taken': 0}

    def compare(self, players):
        """
        Iterate through the player's and compare totals with the dealer
        Parameters
        ----------
        players: The full list of hands played

        Returns
        -------
        Gives a value to player['result']:
        0 if player busts
        1 if player wins
        2 if player loses, but doesn't bust
        3 if push
        4 if player wins and dealer busts
        5 if dealer has blackjack

        """
        for player in players:
            if self.dealer['blackjack']:
                player['result'] = 5
            elif self.dealer['bust'] and not player['bust']:
                player['result'] = 4
            elif player['bust']:
                player['result'] = 0
            else:
                if player['total'] > self.dealer['total']:
                    player['result'] = 1
                elif player['total'] < self.dealer['total']:
                    player['result'] = 2
                else:
                    player['result'] = 3
            # Add results to data
            self.data.results(player['start'], player['total'],
                              self.dealer['total'],
                              self.dealer['card one'].rank, player['taken'],
                              self.num_decks, player['pos'], self.players,
                              player['result'])

    def sim_game(self, decks, players, num_hands):
        """
        Simulates the specified number of blackjack hands

        Parameters
        ----------
        decks: Number of decks to use
        players: Number of players playing
        num_hands: Number of hands to be simulated

        Returns
        -------

        """
        # Parameters needed to play game
        self.num_decks = decks
        self.deck = Deck(self.num_decks)
        self.deck.shuffle()
        self.cut = len(self.deck) * 0.25
        self.players = players
        self.num_hands = num_hands
        print 'Playing Game'
        for i in range(self.num_hands):
            self.play_round()
            if len(self.deck) < self.cut:
                self.deck.create_deck()
                self.deck.shuffle()
                msg = 'Full deck not recreated'
                if len(self.deck) != 52 * self.num_decks:
                    raise ValueError(msg)
                self.card_count = 0
                self.hands_played = 0
