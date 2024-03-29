"""
Command line interface to play blackjack with
"""

import argparse
from py21.game import Game
from py21.player import Player
from py21.strategies import basic_strategy


BASIC_MAP = {"HIT": "H", "STAND": "S", "DOUBLE": "D", "SPLIT": "SP", "SURRENDER": "R"}
ACTION_MAP = {value: key for key, value in BASIC_MAP.items()}
correct = 0
incorrect = 0
total_moves = 0


def cli_main(testing=False):
    desc = "Welcome to the py21 CLI! "
    parser = argparse.ArgumentParser(prog="py21", description=desc)
    parser.add_argument(
        "--training-basic",
        help=(
            "If this flag is included, your choices will be compared to basic "
            "strategy, and you'll be told if you made the correct choice or "
            "not."
        ),
        # default to true until we add more features and options
        default=True,
        action="store_true",
    )
    bankroll = bankroll_input(testing)
    player = Player(bankroll, strategy_func=strategy, wager_func=wager)
    game = Game([player])
    _continue = "y"
    total_hands = 0
    while _continue.lower() != "n":
        game.play_round()
        results = player.history[-1]
        if results["blackjack"]:
            print("\nBlackjack!")
        if results["dealer_blackjack"]:
            print("\nDealer had blackjack :(")
        print(f"\nYour final hand: {results['cards']}")
        print(f"Final total: {results['total']}")
        print(f"Dealter total: {results['dealer_total']}")
        print(f"Hand result: {results['result']}")
        _continue = input("Play again? (y/n) ")
        if _continue.lower() not in ["y", "n"]:
            while _continue.lower() not in ["y", "n"]:
                print("Invalid input. Please enter 'y' or 'n'")
                _continue = input("Play again? (y/n) ")
        total_hands += 1
    # summarize the results
    print(f"\nTotal hands played: {total_hands}")
    correct_pct = (correct / total_moves) * 100
    print(
        f"According to basic strategy, you made the right move {correct_pct:.2f}% of the time"
    )
    print(f"You started with ${player.start_bankroll}...")
    print(f"and finished with ${player.bankroll}")


def strategy(player, hand, dealer_up, game_params, **kwargs):
    global correct, incorrect, total_moves
    print(f"\nDealer shows: {dealer_up}")
    print("Your hand: ", hand)
    valid = False
    options = ["Hit (H)", "Stand (S)", "Double Down (D)", "Surrender (R)", "Split (SP)"]
    while not valid:
        print(f"Options: {options}")
        action = input("What would you like to do? ").upper()
        valid = validate_action(action, hand, game_params)
    # check what basic strategy would do
    basic_strat = basic_strategy(player, hand, dealer_up, game_params, **kwargs)
    if action == BASIC_MAP[basic_strat]:
        print("Basic strategy says that's the right move!")
        correct += 1
    else:
        print(f"Basic strategy says to {basic_strat} instead")
        incorrect += 1
    total_moves += 1
    return ACTION_MAP[action.upper()]


def wager(player, min_bet, max_bet, **kwargs):
    print(f"\nMinimum bet: {min_bet}")
    print(f"Maximum bet: {max_bet}")
    print(f"Your bankroll: {player.bankroll}")
    valid = False
    while not valid:
        bet = int(input("How much would you like to wager? "))
        valid = validate_bet(bet, min_bet, max_bet, player.bankroll)
    return bet


def insurance(**kwargs):
    def validate_insurance(insure):
        if insure not in ["Y", "N"]:
            print("Must enter `y` or `n`")
            return False
        return True

    valid = False
    while not valid:
        insure = input("Dealer shows an Ace. Do you want insurance? (y/n) ").upper()
        valid = validate_insurance(insure)
    if insure == "Y":
        return True
    else:
        return False


def validate_bet(bet, min_bet, max_bet, bankroll):
    """
    Ensure that the bet is acceptable
    """
    if not (isinstance(bet, int) or isinstance(bet, float)):
        print("Bet must be a float or integer")
        return False
    elif bet < min_bet:
        print(f"You must bet at least {min_bet}")
        return False
    elif bet > max_bet:
        print(f"You cannot bet more than {max_bet}")
        return False
    elif bet > bankroll:
        print("You don't have enough to make that bet")
        return False
    return True


def validate_action(action, hand, game_params):
    options = ["H", "S", "D", "R", "SP"]
    if action.upper() not in options:
        print(f"{action} is invalid. Pick one of the following:")
        return False
    # ensure that the selected move is allowed
    end_note = "Please choose another action."
    if action.upper() == "D":
        if len(hand.cards) != 2:
            print(f"You can only double-down at the start of a hand. {end_note}")
            return False
        if hand.player.bankroll < hand.wager:
            print(f"You don't have enough money to double down :(. {end_note}")
            return False
        if hand.from_split and not game_params.double_after_split:
            print(f"You can't double down after splitting. {end_note}")
            return False
    elif action.upper() == "SP":
        if hand.cards[0].value != hand.cards[1].value:
            print(f"Your cards must have the same value to split them. {end_note}")
            return False
        if len(hand.cards) != 2:
            print(f"You can only split your first two cards. {end_note}")
            return False
    elif action.upper() == "R":
        if len(hand.cards) != 2:
            print(f"You can only surrender at the start of the hand. {end_note}")
            return False
        if not game_params.surrender_allowed:
            print(f"Surrendering isn't allowed in this game. {end_note}")
            return False

    return True


def bankroll_input(testing):
    bankroll = 0
    while bankroll <= 0:
        try:
            bankroll = float(input("What's your bankroll? "))
        except ValueError as e:
            print("Your bankroll must be a number")
            if testing:
                raise e
        if bankroll <= 0:
            print("Your bankroll must be greater than 0")
            if testing:
                raise ValueError("Bankroll must be greater than 0")
    return bankroll
