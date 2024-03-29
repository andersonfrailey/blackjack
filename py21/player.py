"""
Definition of the player class
"""
from multiprocessing.sharedctypes import Value
from py21.strategies import basic_strategy, minimum_bet, decline_insurance


class Player:

    def __init__(self, bankroll, strategy_func=None, wager_func=None,
                 insurance_func=None):
        """
        Parameters
        ----------
        bankroll: starting bankroll for a player
        strategy_func: function to determine which action the player will take
            under a given situation.
        wager_func: function to determine how much the player will be wagering.
        insurance_func: function to determine when the player takes insurance.
        """
        self.bankroll = bankroll
        self.start_bankroll = self.bankroll
        # keep a rolling tally of the amount wagered
        self.total_wagered = 0
        self.roi = 0
        # self.strategy = strategy
        self.history = []  # holds hand history
        if not wager_func:
            self.wager_func = minimum_bet
        else:
            self.wager_func = wager_func
        if not strategy_func:
            self.strategy_func = basic_strategy
        else:
            self.strategy_func = strategy_func
        if not insurance_func:
            self.insurance_func = decline_insurance
        else:
            self.insurance_func = insurance_func

    def wager(self, min_bet, max_bet, split_wager=None, **kwargs):
        """
        This method is a wrapper for the wager function passed in
        by the user when initializing the Player object.
        """
        if split_wager:
            wager = split_wager
        else:
            wager = self.wager_func(
                player=self, min_bet=min_bet, max_bet=max_bet, **kwargs
            )
        # assert that the bet is within table stakes and player can afford it
        assert min_bet <= wager <= max_bet, (
            f"{wager} not between min. bet {min_bet} and max bet {max_bet}"
        )
        assert wager <= self.bankroll, {
            f"{wager} greater than bankroll {self.bankroll}"
        }
        self.bankroll -= wager
        self.total_wagered += wager
        return wager

    def action(self, hand, dealer_up, game_params, **kwargs):
        """
        This method is a wrapper for the strategy function passed in by the
        user when initializing the Player object.
        """
        if hand.blackjack:
            return "STAND"
        action = self.strategy_func(
            player=self, hand=hand, dealer_up=dealer_up,
            game_params=game_params, **kwargs
        ).upper()
        if action not in hand.valid_actions:
            self._raise_error(action, hand, game_params)
        return action

    def insurance(self, **kwargs):
        """
        This method is a wrapper for the insurance function passed in by the
        user when initializing the Player object.
        """
        action = self.insurance_func(player=self, **kwargs)
        assert isinstance(action, bool), (
            "Insurance action must be True or False"
        )
        return action

    def settle_up(self, hand_data, dealer_total, result, payout,
                  blackjack_payout, dealer_blackjack, split_bj_payout,
                  surrender_pct):
        """
        This method logs all of the data for a given hand.
        Parameters
        ----------
        hand_data: dictionary containing information on the hand
        dealer_total: final total for the dealer
        payout: payout for winning a hand
        blackjack_payout: payout for winning a hand with blackjack
        dealer_blackjack: boolean indicating whether or not the dealer had
            blackjack
        split_bj_payout: payout for having a blackjack on a split hand
        surrender_pct: percentage of your bet you get back after surrendering
        Returns
        -------
        None
        """
        wager = hand_data["wager"]
        additonal_data = {
            "dealer_total": dealer_total,
            # add back initial wager to get starting bankroll
            "start_bankroll": self.bankroll + wager,
            "result": result
        }
        # pay off insurance
        if hand_data["insurance"] and dealer_blackjack:
            self.bankroll += wager
        # adjust bankroll according to result
        if result == "win":
            if hand_data["blackjack"]:
                if hand_data["from_split"]:
                    _payout = wager + (wager * split_bj_payout)
                else:
                    _payout = wager + (wager * blackjack_payout)
            else:
                _payout = wager + (wager * payout)
            self.bankroll += _payout
        elif result == "push":
            # add back wager if they push
            self.bankroll += wager
        elif result == "surrender":
            self.bankroll += wager * surrender_pct
        additonal_data["end_bankroll"] = self.bankroll
        # return from betting the player has gotten
        self.roi = (self.bankroll - self.start_bankroll) / self.total_wagered
        additonal_data["roi"] = self.roi
        self.history.append({**hand_data, **additonal_data})

    def _raise_error(self, action, hand, game_params):
        """
        Explain why the given action was invalid
        """
        if action == "SURRENDER":
            if not game_params.surrender_allowed:
                msg = "Surrendering is not allowed"
            elif hand.from_split and not game_params.surrender_after_split:
                msg = "Surrendering not allowed after splitting"
            elif len(hand) != 2:
                msg = "Cannot surrender after taking a card"
        elif action == "DOUBLE":
            if len(hand) != 2:
                msg = "Cannot double down after taking a card"
            elif self.bankroll < hand.wager:
                raise ValueError("Insufficient funds to double down")
            elif hand.from_split and not game_params.double_after_split:
                msg = "Not allowed to double after a split"
        elif action == "SPLIT":
            if len(hand) != 2:
                msg = "Cannot split after taking a card"
            elif self.bankroll < hand.wager:
                raise ValueError("Insufficient funds to split")
            elif hand.cards[0] != hand.cards[1]:
                msg = "Can only split matching cards"
            elif hand.nsplits > game_params.max_split_hands:
                msg = f"Cannot split more than {game_params.max_split_hands} times"

        raise ValueError(msg)
