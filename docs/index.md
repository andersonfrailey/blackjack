# How to Use Py21

## Basic Usage

All that you need to do to run the simulator is initiate instances of the `Game`
and `Player` objects from the `py21` package. The `Player` object has one
required argument and three optional arguments:

* `bankroll`: starting bankroll for the player (required).
* `strategy_func`: function used to determine the action a player takes (optional).
* `wager_func`: function used to determine how a player bets (optional).
* `insurance_func`: function used to determine when the player takes insurance (optional).

Instructions on how to write you're own custom functions for each of the
arguments appear later in the document. By default, the player is set to use
basic strategy, bet the minimum, and never take insurance.

The `Game` object takes one required argument and two optional ones:

* `players`: list of `Player` objects that will be used in the game (required)
* `rules`: dictionary containing updates to the game's rules (optional)
* `verbose`: True/False for whether or not you want output to be printed while
  the game is being played (optional)

```python
from py21 import Game, Player

player = Player(100)
game = Game([player])
```

If you would like to modify the rules to the game before playing, you can do so
by using a dictionary with a `{parameter: new_rule} format.

```python
new_rules = {"num_decks": 8}
game = Game([player], rules=new_rules)
```

A full list of the game parameters you can change can be found [here](https://github.com/andersonfrailey/blackjack/blob/master/docs/default_rules.md).

At this point, you are ready to play. You can play a single round, or simulate
as many as you wish.

```python
game.play_round()  # simulate a single round
game.simulate(n)  # simulate n rounds
```

## Creating Custom Functions

To take your simulations to the next level, you can create custom functions to
control player actions.

When you initiate the `Player` object, you can specify a function to call when
an action like hit or stand is required. This function is called with the
following arguments:

* `player`: the player object the function is attached to.
* `hand`: the player's current hand. This is an instance of the `Hand` class.
* `dealer_up`: the dealer's up card.
* `start_count`: the count at the start of the hand.
* `count`: the current count.
* `ten_count`: number of cards with a value of ten left in the deck.
* `other_count`: number of cards with a value other than ten left in the deck.
* `game_params`: the current rules of the game.

You can use all of these arguments to determine when a player hits, stands,
splits, or doubles down. The returned value of this function must be one of the
following: HIT, STAND, SPLIT, DOUBLE.

```python
from py21 import Player


def hit_to_seventeen(player, hand, **kwargs):
    """
    Hit until the hand total reaches 17

    This function can be used at the strategy_func argument in an instance of
    of the Player class.
    """
    if hand.total >= 17:
        return "STAND"
    else:
        return "HIT"


player = Player(bankroll=100, strategy_func=hit_to_seventeen)
```

The same arguments (except for `dealer_up`) can be used to determine what the
player wagers as well. The only restriction is that the value returned by the
function must be between the minimum and maximum bet.

```python
import random
from py21 import Player


def random_bet(player, min_bet, max_bet, **kwargs):
    """
    Return a bet between the minimum and maximum bet
    """
    return random.randint(min_bet, max_bet)


player = Player(bankroll=1000, wager_func=random_bet)
```

They can also be used to determine if the player accepts or declines insurance
when the dealer is showing an ace. This must return `True` or `False`.


```python
from py21 import Player


def decline_insurance(**kwargs):
    """
    Function for always declining insurance.

    This can be used as the insurance_func argument in an insuance of the
    Player class.
    """
    return False


player = Player(bankroll=100, insurance_func=deline_insurance)
```