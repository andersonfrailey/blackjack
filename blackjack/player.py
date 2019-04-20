"""
Definition of the player class
"""
from .strategies import hit_to_seventeen, minimum_bet, decline_insurance


class Player:

    def __init__(self, bankroll, strategy_func=None, wager_func=None,
                 insurance_func=None):
        """
        Parameters
        ----------
        bankroll: starting bankroll for a player
        strategy: CSV file containing a player's strategy
        wager: function to determine how much the player will be wagering
        """
        self.bankroll = bankroll
        # self.strategy = strategy
        self.history = []  # holds hand history
        if not wager_func:
            self.wager_func = minimum_bet
        else:
            self.wager_func = wager_func
        if not strategy_func:
            self.strategy_func = hit_to_seventeen
        else:
            self.strategy_func = strategy_func
        if not insurance_func:
            self.insurance_func = decline_insurance
        else:
            self.insurance_func = insurance_func

    def wager(self, min_bet, max_bet, **kwargs):
        """
        This function is essentially a wrapper for the wager function passed in
        by the user when initializing the Player object.
        """
        wager = self.wager_func(player=self, min_bet=min_bet, max_bet=max_bet,
                                **kwargs)
        # assert that the bet is within table stakes and player can afford it
        assert min_bet <= wager <= max_bet, (
            f"{wager} not between min. bet {min_bet} and max bet {max_bet}"
        )
        assert wager <= self.bankroll, {
            f"{wager} greater than bankroll {self.bankroll}"
        }
        self.bankroll -= wager
        return wager

    def action(self, hand, dealer_up, **kwargs):
        """
        This method returns a player action based on the dealer's up card and
        the hand total.
        """
        if hand.blackjack:
            return "STAND"
        action = self.strategy_func(player=self, hand=hand,
                                    dealer_up=dealer_up, **kwargs).upper()
        assert action in ["STAND", "SPLIT", "HIT", "DOUBLE"]
        return action

    def insurance(self, **kwargs):
        return self.insurance_func(player=self, **kwargs)

    def settle_up(self, hand_data, dealer_total, result, payout,
                  blackjack_payout, dealer_blackjack):
        """
        This method logs all of the data for a given hand
        Parameters
        ----------
        hand_data: dictionary containing information on the hand
        dealer_total: final total for the dealer
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
                payout = wager + (wager * blackjack_payout)
            else:
                payout = wager + (wager * payout)
            self.bankroll += payout
        elif result == "push":
            # add back wager if they push
            self.bankroll += wager
        additonal_data["end_bankroll"] = self.bankroll
        self.history.append({**hand_data, **additonal_data})
