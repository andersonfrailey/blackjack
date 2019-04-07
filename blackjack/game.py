""""
The Game class is used to handle all of the logistics of the game including
dealing the cards, playing the players hands, and playing the dealer
"""
import os
from .deck import Deck
from .hand import Hand
from paramtools.parameters import Parameters
from tqdm import tqdm


CUR_PATH = os.path.abspath(os.path.dirname(__file__))


class GameParams(Parameters):
    schema = os.path.join(CUR_PATH, "schema.json")
    defaults = os.path.join(CUR_PATH, "rules.json")
    array_first = True


class Game:

    def __init__(self, num_decks, players, rules=None, verbose=False):
        """
        Parameters
        ----------
        num_decks: number of decks to play with.
        rules: rules of the game regarding whether a dealer hits on soft 17
            or not.
        players: list of Python objects that are used to act as players in the
            game.
        rules: dictionary containing any rule updates
        verbose: boolean indicator for whether or not output should be printed
            as the game progresses
        """
        # game parameters
        self.num_decks = num_decks
        self.deck = Deck(num_decks)
        self.count = 0
        self.ten_count = 16 * num_decks
        self.player_list = players
        self.count = 0
        self.num_players = len(players)
        self.rules = rules
        self.game_params = GameParams(array_first=True)
        self.hands = []
        # update rules for the game
        if self.rules:
            if not isinstance(self.rules, dict):
                raise TypeError("'rules' must be a dictionary.")
            self._update_params(self.rules)
        self.verbose = verbose

        # burn first card
        self.deck.deal()

    def play_round(self):
        """
        Play a single round of blackjack
        """
        start_count = self.count
        self.deck.hands_played += 1
        hands = []  # holds all of the hands the players will play
        # deal first card to all players
        for player in self.player_list:
            # skip any players without a high enough bankroll
            if player.bankroll < self.game_params.min_bet:
                continue
            card_one = self.deck.deal()
            self._count(card_one)
            min_bet = self.game_params.min_bet
            max_bet = self.game_params.max_bet
            hands.append(Hand(card_one, player=player,
                              min_bet=min_bet, max_bet=max_bet))
        # deal to dealer
        card = self.deck.deal()
        self._count(card)
        dealer = Hand(card)
        dealer_up = dealer.card_one
        # deal second card to all players
        for hand in hands:
            card_two = self.deck.deal()
            self._count(card_two)
            hand.add_card_two(card_two)
        # deal second card to dealer, but don't count until later
        dealer.add_card_two(self.deck.deal())
        if self.verbose:
            print(f"Dealer Up Card: {dealer.card_one}")
            print(f"Player Hands:")
            for hand in hands:
                print(f"{hand.cards[0]}{hand.cards[1]}")
            if dealer.blackjack:
                print("Dealer Blackjack")
        # check for dealer blackjack
        # play only if the dealer doesn't have blackjack
        if not dealer.blackjack:
            # play each hand
            num_busts_splits_blackjacks = 0
            for hand in hands:
                # if the new hand is from a split, add a second card before
                # playing
                if hand.from_split:
                    card = self.deck.deal()
                    self._count(card)
                    hand.add_card_two(card)
                if hand.blackjack:
                    num_busts_splits_blackjacks += 1
                if self.verbose:
                    print(f"{hand.cards[0]}{hands.card[1]}")
                while not hand.stand and not hand.bust:
                    action = hand.player.action(hand, dealer_up,
                                                start_count=start_count)
                    if self.verbose:
                        print(f"Player action: {action}")
                    if action == "STAND":
                        setattr(hand, "stand", True)
                        continue
                    elif action == "SPLIT":
                        # only allow split if the card ranks are equal and they
                        # only have two cards
                        allowed = (hand.card_one == hand.cards[1] and
                                   len(hand.cards) == 2)
                        if not allowed:
                            action = "HIT"
                        else:
                            # create two new hands using original two cards
                            hand_one_card = hand.card_one
                            hand_two_card = hand.cards[1]
                            hand_one = Hand(hand_one_card, from_split=True,
                                            player=hand.player)
                            hand_two = Hand(hand_two_card, from_split=True,
                                            player=hand.player)
                            hands.insert(hands.index(hand) + 1, hand_one)
                            hands.insert(hands.index(hand) + 2, hand_two)
                            # flag the hand as split
                            setattr(hand, "split", True)
                            num_busts_splits_blackjacks += 1
                            continue
                    elif action == "DOUBLE":
                        # can only double in your first move
                        allowed = len(hand.cards) == 2
                        # not all games allow you to double split hands
                        if hand.from_split:
                            allowed = self.game_params.double_after_split
                        # if allowed, you must stand after doubling down
                        if allowed:
                            setattr(hand, "stand", True)
                        # whether or not the double is allowed, the player will
                        # add a card
                        action = "HIT"
                    if action == "HIT":
                        card = self.deck.deal()
                        self._count(card)
                        hand.add_card(card)
                        if self.verbose:
                            print(f"Card Received: {card}")
                            print(f"New Total: {hand.total}")
                    if hand.bust:
                        num_busts_splits_blackjacks += 1

            # count dealer's second card
            self._count(dealer.cards[1])
            if self.verbose:
                print(f"Dealer Hand: {dealer.cards[0]} {dealer.cards[1]}")
            # if needed, play the dealer
            dealer_play = num_busts_splits_blackjacks != len(hands)
            if dealer_play:
                stand_total = self.game_params.stand_total
                soft_stand = self.game_params.soft_stand
                if dealer.total >= stand_total:
                    # logic for determining if a dealer plays soft hands
                    if dealer.total == stand_total and dealer.soft:
                        dealer_stand = soft_stand
                    else:
                        dealer_stand = True
                else:
                    dealer_stand = False
                while not dealer_stand and not dealer.bust:
                    card = self.deck.deal()
                    self._count(card)
                    dealer.add_card(card)
                    if self.verbose:
                        print(f"Dealer Draws: {card}")
                        print(f"New Dealer Total: {dealer.total}")
                    if dealer.total >= stand_total:
                        if dealer.total == stand_total and dealer.soft:
                            dealer_stand = soft_stand
                        else:
                            dealer_stand = True

        self._compare(hands, dealer,
                      self.game_params.blackjack_payout)
        # check if the deck should be shuffled
        burn = self.deck.check_status(self.game_params.shuffle_freq)
        # burn first card
        if burn:
            self.deck.deal()

    def simulate(self, rounds):
        """
        Simulate a given number of hands of blackjack
        """
        for i in tqdm(range(rounds)):
            self.play_round()

    # Start private methods

    def _update_params(self, rules):
        """
        Update the game parameters based on user input
        """
        self.game_params.adjust(rules)

    def _compare(self, hands, dealer, blackjack_payout):
        """
        Function to compare the dealer to each hand in hands and settle up
        """
        for hand in hands:
            # skip split hands
            if hand.split:
                continue
            if self.verbose:
                print(f"Player Total: {hand.total}")
                print(f"Dealer Total: {dealer.total}")
            if hand.bust:
                hand.player.settle_up(hand.summary_data(), dealer.total,
                                      "loss", blackjack_payout)
            elif dealer.bust:
                hand.player.settle_up(hand.summary_data(), dealer.total,
                                      "win", blackjack_payout)
            elif hand > dealer:
                hand.player.settle_up(hand.summary_data(), dealer.total,
                                      "win", blackjack_payout)
            elif hand < dealer:
                hand.player.settle_up(hand.summary_data(), dealer.total,
                                      "loss", blackjack_payout)
            else:
                hand.player.settle_up(hand.summary_data(), dealer.total,
                                      "push", blackjack_payout)
            if self.verbose:
                print(f"Player Bankroll: {hand.player.bankroll}")

    def _count(self, card):
        """
        Count cards as they're delt
        """
        if 2 <= card.rank <= 6:
            self.count += 1
        elif card.rank >= 10:
            self.count -= 1
            self.ten_count -= 1
