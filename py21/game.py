""""
The Game class is used to handle all of the logistics of the game including
dealing the cards, playing the players hands, and playing the dealer
"""
import copy
import os
from .deck import Deck
from .hand import Hand
from paramtools.parameters import Parameters
from tqdm import tqdm


CUR_PATH = os.path.abspath(os.path.dirname(__file__))


class GameParams(Parameters):
    defaults = os.path.join(CUR_PATH, "rules.json")
    array_first = True


class Game:

    def __init__(self, players, rules=None, verbose=False):
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
        # make a copy of rules to avoid modifying the original dictionary
        self.rules = copy.deepcopy(rules)
        self.game_params = GameParams(array_first=True)
        # update rules for the game
        if self.rules:
            if not isinstance(self.rules, dict):
                raise TypeError("'rules' must be a dictionary.")
            self._update_params(self.rules)
        self.num_decks = self.game_params.num_decks
        self.deck = Deck(self.num_decks)
        self.count = 0
        self.ten_count = 16 * self.num_decks  # count of tens seen
        self.other_count = 36 * self.num_decks  # count of non-tens seens
        self.player_list = players
        self.count = 0
        self.num_players = len(players)
        assert 1 <= self.num_players <= self.game_params.max_players
        self.verbose = verbose

        # variables for data collection
        self.hit_results = []
        self.round_id = 1

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
                              min_bet=min_bet, max_bet=max_bet,
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
                        count=self.count,
                        ten_count=self.ten_count,
                        other_count=self.other_count
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
            hand_id = 0
            # play each hand
            num_busts_splits_blackjacks = 0
            for hand in hands:
                hand_id += 1
                # if the new hand is from a split, add a second card before
                # playing
                if hand.from_split:
                    card = self.deck.deal()
                    self._count(card)
                    hand.add_card_two(card)
                if hand.blackjack:
                    num_busts_splits_blackjacks += 1
                if self.verbose:
                    print(f"{hand.cards[0]}{hand.cards[1]}")
                while not hand.stand and not hand.bust:
                    action = hand.player.action(hand, dealer_up.value,
                                                start_count=start_count,
                                                count=self.count,
                                                ten_count=self.ten_count,
                                                other_count=self.other_count,
                                                game_params=self.game_params)
                    if self.verbose:
                        print(f"Player action: {action}")
                    if action == "STAND":
                        setattr(hand, "stand", True)
                        continue
                    elif action == "SPLIT":
                        # only allow split if the card ranks are equal and they
                        # only have two cards
                        card_match = hand.card_one == hand.cards[1]
                        starting_hand = len(hand.cards) == 1
                        bankroll = hand.player.bankroll >= hand.wager
                        allowed = card_match and starting_hand and bankroll
                        if not allowed:
                            action = "HIT"
                        else:
                            # create two new hands using original two cards
                            hand_one_card = hand.card_one
                            hand_two_card = hand.cards[1]
                            hand_one = Hand(hand_one_card, from_split=True,
                                            player=hand.player,
                                            min_bet=min_bet,
                                            max_bet=max_bet,
                                            game_params=self.game_params)
                            hand_two = Hand(hand_two_card, from_split=True,
                                            player=hand.player,
                                            min_bet=min_bet,
                                            max_bet=max_bet,
                                            game_params=self.game_params)
                            # insert the hands in the hands list so they are
                            # iterated over next
                            hands.insert(hands.index(hand) + 1, hand_one)
                            hands.insert(hands.index(hand) + 2, hand_two)
                            # flag the hand as split and skip other play logic
                            setattr(hand, "split", True)
                            num_busts_splits_blackjacks += 1
                            continue
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

        self._compare(hands, dealer, self.game_params.payout,
                      self.game_params.blackjack_payout)
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
        Simulate a given number of hands of blackjack
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
        Update the game parameters based on user input
        """
        for param in rules.keys():
            val = rules[param]
            rules[param] = [{"value": val}]
        self.game_params.adjust(rules)

    def _compare(self, hands, dealer, payout, blackjack_payout):
        """
        Function to compare the dealer to each hand in hands and settle up
        """
        additional_data = {
            "round_id": self.round_id,
            "dealer_blackjack": int(dealer.blackjack),
            "dealer_up": dealer.card_one.value
        }
        for hand in hands:
            hand_data = {**hand.summary_data(), **additional_data}
            hand_data["hand_id"] = hands.index(hand) + 1
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
        if 2 <= card.rank <= 6:
            self.count += 1
        elif card.rank >= 10:
            self.count -= 1
            self.ten_count -= 1
        if card.value < 10:
            self.other_count -= 1
