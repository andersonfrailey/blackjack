""""
The Game class is used to handle all of the logistics of the game including
dealing the cards, playing the players hands, and playing the dealer
"""
# ignore no-member in pylist because it's raised for the game parameters
# because pylint doesn't know about paramtools
# pylint: disable=no-member
import copy
import difflib
from .deck import Deck
from .hand import Hand
from paramtools.parameters import Parameters
from tqdm import tqdm
from pathlib import Path


CUR_PATH = Path(__file__).resolve().parent


class GameParams(Parameters):
    defaults = Path(CUR_PATH, "rules.json").open("r").read()
    array_first = True


class Game:

    def __init__(self, players, rules=None, verbose=False, test=False):
        """
        Parameters
        ----------
        players: list of Python objects that are used to act as players in the
            game.
        rules: dictionary containing any rule updates
        verbose: boolean indicator for whether or not output should be printed
            as the game progresses
        test: boolean value for whether or not this is a test run. This should
            only be used during unit tests
        """
        # game parameters
        # make a copy of rules to avoid modifying the original dictionary
        self.rules = copy.deepcopy(rules)
        self.game_params = GameParams(array_first=True)
        # update rules for the game
        if self.rules:
            if not isinstance(self.rules, dict):
                raise TypeError("'rules' must be a dictionary.")
            self._update_params(self.rules)
        self.num_decks = self.game_params.num_decks
        self.deck = Deck(self.num_decks, test=test)
        self.count = 0
        self.ten_count = 16 * self.num_decks  # count of tens seen
        self.other_count = 36 * self.num_decks  # count of non-tens seens
        self.player_list = players
        self.num_players = len(players)
        assert 1 <= self.num_players <= self.game_params.max_players
        self.verbose = verbose

        # variables for data collection
        self.hit_results = []
        self.round_id = 1

        # burn first card
        self.deck.deal()

        # list to hold completed hands. Will be cleared after each round
        self._completed_hands = []
        # counter for the number of times a hand is split. Used to enforce max
        # number of times a hand can be split
        self._num_splits = 0

    def play_round(self):
        """
        Play a single round of blackjack. This method will loop through all of
        the players in self.player_list assigning each a hand (as long as they
        have enough money left to make the minimum bet) and then playing that
        hand to completion.
        """
        # set all counts at the time players would be betting
        start_count = self.count
        start_ten_count = self.ten_count
        start_other_count = self.other_count
        self.deck.hands_played += 1
        hands = []  # holds all of the hands the players will play
        min_bet = self.game_params.min_bet
        max_bet = self.game_params.max_bet
        # deal first card to all players
        for player in self.player_list:
            # skip any players without a high enough bankroll
            if player.bankroll < self.game_params.min_bet:
                continue
            card_one = self.deck.deal()
            self._count(card_one)
            hands.append(Hand(card_one, player=player,
                              min_bet=min_bet, max_bet=max_bet,
                              count=start_count, ten_count=start_ten_count,
                              other_count=start_other_count,
                              game_params=self.game_params))
        # break out of function if there are no more players with money
        if hands == []:
            return "break"
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
        if dealer.card_one.rank == 14:
            if self.game_params.insurance_allowed:
                for hand in hands:
                    insurance = hand.player.insurance(
                        start_count=start_count,
                        count=self.count,
                        ten_count=self.ten_count,
                        other_count=self.other_count,
                        game_params=self.game_params
                    )
                    setattr(hand, "insurance", insurance)
                    if insurance:
                        payment = self.game_params.insurance_pct * hand.wager
                        hand.player.bankroll -= payment
        if self.verbose:
            print(f"Dealer Up Card: {dealer.card_one}")
            print(f"Player Hands:")
            for hand in hands:
                print(f"{hand.cards[0]}{hand.cards[1]}")
                print(f"Wager: {hand.wager}")
            if dealer.blackjack:
                print("Dealer Blackjack")
        # check for dealer blackjack
        # play only if the dealer doesn't have blackjack
        if not dealer.blackjack:
            # play each hand
            num_busts_splits_blackjacks = 0
            for _hand_id, hand in enumerate(hands):
                hand_id = _hand_id + 1
                if self.verbose:
                    print(f"{hand.cards[0]}{hand.cards[1]}")
                # if they have blackjack, skip to the next hand
                if hand.blackjack:
                    num_busts_splits_blackjacks += 1
                    continue
                self._play_hand(
                    hand, dealer_up.value, min_bet, max_bet, hand_id,
                    start_count, start_ten_count, start_other_count
                )
                # reset number of splt hands
                setattr(self, "_num_splits", 0)
            # count dealer's second card
            self._count(dealer.cards[1])
            if self.verbose:
                print(f"Dealer Hand: {dealer.cards[0]} {dealer.cards[1]}")
            # if needed, play the dealer
            dealer_play = False
            # we only need the dealer to play their hand if there's someone
            # who hasn't busted or gotten blackjack
            for hand in self._completed_hands:
                if not hand.bust and not hand.blackjack:
                    dealer_play = True
                    break
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

        self._compare(dealer, self.game_params.payout,
                      self.game_params.blackjack_payout)
        # clear completed hands list
        del self._completed_hands[:]
        # check if the deck should be shuffled
        new_deck = self.deck.check_status(self.game_params.shuffle_freq)
        # burn first card
        if new_deck:
            self.deck.deal()
            setattr(self, "count", 0)
            setattr(self, "ten_count", 16 * self.num_decks)
            setattr(self, "other_count", 36 * self.num_decks)

            if self.verbose:
                print("Shuffling deck")
        self.round_id += 1

    def simulate(self, rounds):
        """
        Simulate a given number of hands of blackjack. This method calls the
        play_round method for the number of rounds specified.

        Parameters
        ----------
        rounds: number of rounds to be played
        """
        for i in tqdm(range(rounds)):
            # break out of loop if all players run out of money
            holder = self.play_round()
            if holder:
                print(f"All player's out of money. {i} hands played.")
                break

    # Start private methods

    def _update_params(self, rules):
        """
        Update the game parameters based on user input.
        """
        allowed_params = self.game_params.specification().keys()
        for param in rules.keys():
            # ensure parameter is allowed
            if param not in allowed_params:
                similar = difflib.get_close_matches(param, allowed_params)
                msg = (
                    f"Unexpected parameter name {param}. Similar parameter(s) "
                    f"are: {similar}"
                )
                raise ValueError(msg)
        self.game_params.adjust(rules)

    def _play_hand(self, hand, dealer_up, min_bet, max_bet, hand_id,
                   start_count, start_ten_count, start_other_count):
        """
        Function that contains all of the logic for playing a hand
        """
        while not hand.stand and not hand.bust and not hand.surrender:
            action = hand.player.action(hand, dealer_up,
                                        start_count=start_count,
                                        count=self.count,
                                        ten_count=self.ten_count,
                                        other_count=self.other_count,
                                        game_params=self.game_params)
            if self.verbose:
                print(f"Player action: {action}")
            if action == "STAND":
                setattr(hand, "stand", True)
                break
            elif action == "SPLIT":
                # only allow split if the card ranks are equal and they
                # only have two cards
                card_match = hand.card_one == hand.cards[1]
                starting_hand = len(hand.cards) == 2
                bankroll = hand.player.bankroll >= hand.wager
                n_splits = self._num_splits < self.game_params.max_split_hands
                allowed = (
                    card_match and starting_hand and bankroll and n_splits
                )
                if not allowed:
                    if self.verbose:
                        print(
                            "Split not allowed. Hitting instead. "
                            "See listed flags for explanation\n"
                            f"card match: {card_match}\n"
                            f"start of hand: {starting_hand}\n"
                            f"large enough bankroll: {bankroll}\n"
                            f"fewer than 3 splits: {n_splits}"
                        )
                    action = "HIT"
                else:
                    self._num_splits += 1
                    hand.split = True
                    # We need to "return" the original wager the
                    # player made because each subsequent hand will
                    # subtract an equal wager from the bankroll.
                    # this keeps us from double chargind for the first
                    # split hand
                    hand.player.bankroll += hand.wager
                    # create two new hands using original two cards
                    hand_one_card = hand.card_one
                    hand_two_card = hand.cards[1]
                    hand_one = Hand(hand_one_card, from_split=True,
                                    player=hand.player,
                                    min_bet=min_bet,
                                    max_bet=max_bet,
                                    start_count=start_count,
                                    count=start_count,
                                    ten_count=start_ten_count,
                                    other_count=start_other_count,
                                    game_params=self.game_params,
                                    split_wager=hand.wager)
                    hand_two = Hand(hand_two_card, from_split=True,
                                    player=hand.player,
                                    min_bet=min_bet,
                                    max_bet=max_bet,
                                    start_count=start_count,
                                    count=start_count,
                                    ten_count=start_ten_count,
                                    other_count=start_other_count,
                                    game_params=self.game_params,
                                    split_wager=hand.wager)
                    # play both hands
                    if self.verbose:
                        print("Playing Split Hands")
                        print("First Split Hand")
                    card_two = self.deck.deal()
                    self._count(card_two)
                    hand_one.add_card_two(card_two)
                    if self.verbose:
                        print(f"New Hand: {hand_one.cards[0]}{card_two}")
                    self._play_hand(
                        hand_one, dealer_up, min_bet, max_bet, hand_id,
                        start_count, start_ten_count, start_other_count
                    )
                    if self.verbose:
                        print("Second Split Hand")
                    # play second hand from split
                    card_two = self.deck.deal()
                    self._count(card_two)
                    hand_two.add_card_two(card_two)
                    if self.verbose:
                        print(f"New Hand: {hand_two.cards[0]}{card_two}")
                    self._play_hand(
                        hand_two, dealer_up, min_bet, max_bet, hand_id,
                        start_count, start_ten_count, start_other_count
                    )
                    # exit loop
                    break
            elif action == "DOUBLE":
                # can only double in your first move
                allowed = (len(hand.cards) == 2 and
                            hand.player.bankroll >= hand.wager)
                # not all games allow you to double split hands
                if hand.from_split:
                    allowed = self.game_params.double_after_split
                # if allowed, you must stand after doubling down
                if allowed:
                    setattr(hand, "stand", True)
                    # double the player's bet
                    hand.player.bankroll -= hand.wager
                    setattr(hand, "wager", hand.wager * 2)
                # if not allowed to double, just hit
                else:
                    action = "HIT"
            elif action == "SURRENDER":
                # only allow surrender if they player hasn't taken a
                # card yet and if the game rules allow
                allowed = (
                    self.game_params.surrender_allowed &
                    len(hand.cards) == 2
                )
                if hand.from_split and allowed:
                    allowed = self.game_params.surrender_after_split
                if allowed:
                    setattr(hand, "surrender", True)
                else:
                    raise ValueError(
                        "Surrender is not allowed"
                    )
                continue
            if action == "HIT" or action == "DOUBLE":
                hit_data = {"start_total": hand.total,
                            "start_count": self.count,
                            "start_ten_count": self.ten_count,
                            "start_other_count": self.other_count,
                            "round_id": self.round_id,
                            "hand_id": hand_id,
                            "action": action,
                            "soft": int(hand.soft)}
                card = self.deck.deal()
                hit_data["card_received_rank"] = card.rank
                self._count(card)
                hand.add_card(card)
                hit_data["new_total"] = hand.total
                card_received_value = (hit_data["new_total"] -
                                       hit_data["start_total"])
                hit_data["card_received_value"] = card_received_value
                self.hit_results.append(hit_data)
                if self.verbose:
                    print(f"Card Received: {card}")
                    print(f"New Total: {hand.total}")
        # only append non-split hands
        if not hand.split:
            self._completed_hands.append(hand)

    def _compare(self, dealer, payout, blackjack_payout):
        """
        Function to compare the dealer to each hand in hands and settle up
        """
        additional_data = {
            "round_id": self.round_id,
            "dealer_blackjack": int(dealer.blackjack),
            "dealer_up": dealer.card_one.value
        }
        for hand in self._completed_hands:
            hand_data = {**hand.summary_data(), **additional_data}
            hand_data["hand_id"] = self._completed_hands.index(hand) + 1
            # skip split hands
            if hand.split:
                continue
            if self.verbose:
                print(f"Player Total: {hand.total}")
                print(f"Dealer Total: {dealer.total}")
            if hand.bust:
                hand.player.settle_up(hand_data, dealer.total,
                                      "loss", payout, blackjack_payout,
                                      dealer.blackjack)
            elif dealer.bust:
                hand.player.settle_up(hand_data, dealer.total,
                                      "win", payout, blackjack_payout,
                                      dealer.blackjack)
            elif hand > dealer:
                hand.player.settle_up(hand_data, dealer.total,
                                      "win", payout, blackjack_payout,
                                      dealer.blackjack)
            elif hand < dealer:
                hand.player.settle_up(hand_data, dealer.total,
                                      "loss", payout, blackjack_payout,
                                      dealer.blackjack)
            else:
                if self.verbose:
                    print("Push")
                hand.player.settle_up(hand_data, dealer.total,
                                      "push", payout, blackjack_payout,
                                      dealer.blackjack)
            if self.verbose:
                print(f"Player Bankroll: {hand.player.bankroll}\n")

    def _count(self, card):
        """
        Count cards as they're delt
        """
        if 2 <= card.value <= 6:
            self.count += 1
        elif card.value >= 10:
            self.count -= 1
            self.ten_count -= 1
        if card.value < 10:
            self.other_count -= 1
