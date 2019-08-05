import os
import pandas as pd
from py21 import Game, Player
from py21.strategies import basic_strategy
from py21.utils import results_pct

# global variables
incorrect_moves = 0
total_moves = 0


def strategy(player, hand, dealer_up, game_params, **kwargs):
    """
    Strategy of asking user for input
    """
    global incorrect_moves, total_moves
    # find the correct action
    correct = basic_strategy(player, hand, dealer_up, game_params, **kwargs)
    # compare user inputs to what basic strategy suggests
    user = input("Action: ").upper()
    if user == "H":
        action = "HIT"
    elif user == "S":
        action = "STAND"
    elif user == "D":
        action = "DOUBLE"
    total_moves += 1
    if action != correct:
        incorrect_moves += 1
        print(f"Correct move was: {correct}")
    return action


def wager(player, min_bet, max_bet, **kwargs):
    print(f"Current Bankroll: {player.bankroll}")
    print(f"Minimum: {min_bet} Maximum: {max_bet}")
    bet = float(input("Wager: "))
    return bet


def insurance(player, count, ten_count, other_count, **kwargs):
    insure = input("Dealer shows an ace. Take insurance? (y/n): ")
    if insure == "y":
        return True
    elif insure == "n":
        return False


def training():
    """
    Core logic for creating a training app
    """
    num_decks = int(input("How many decks would you like to play with? "))
    start_bankroll = int(input("What is your bankroll? "))

    rules = {
        "num_decks": num_decks
    }
    player = Player(start_bankroll, strategy, wager, insurance)
    game = Game([player], rules=rules, verbose=True)
    play = "y"
    while play != "n":
        game.play_round()
        play = input("Play again? (y/n): ")
        os.system("clear")

    try:
        correct_pct = ((total_moves - incorrect_moves) / total_moves) * 100
        print(f"You made the correct move {correct_pct:.2f} of the time")
    except ZeroDivisionError:
        pass
    end_bankroll = player.bankroll
    print(f"Starting Bankroll: {start_bankroll}")
    print(f"Final Bankroll: {end_bankroll}")
    win, loss, push = results_pct(pd.DataFrame(player.history))
    print(f"Winning Percentage: {win * 100}")
    print(f"Lossing Percentage: {loss * 100}")
    print(f"Push Percentage: {push * 100}")


if __name__ == "__main__":
    training()
