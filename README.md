[![PyPI version fury.io](https://badge.fury.io/py/py21.svg)](https://pypi.python.org/pypi/py21/)
[![PyPi downloads](https://pypip.in/d/py21/badge.png)](https://crate.io/packages/$REPO/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)


# Blackjack

`py21` is a blackjack simulator. Users can run the simulation using the
default rules or specify their own. Additionally, users can test their own
playing and betting strategies.

## Installation

Right now `py21` can be installed from source or PyPI.

To download from source, clone or download this
repository, then navigate to the directory you cloned to and run
`pip install -e .`.

To download from PyPI, use `pip install py21`

## Using `py21`

To run the simulator, the user must initiate one instance of the `Game` class
and at least one instance of the `Player` class.

The `Player` class requires one input, `bankroll`, and has three optional inputs:
`strategy_func`, `wager_func`, and `insurance_func`.

`bankroll` should be an numerical value indicating the bankroll
the player will be starting with.

`strategy_func` should be a function that will
return what action the player will take in a given situation. This function
can take as inputs a number of variables containing information about the game
such as the player's hand, dealer's up card, and the count. It must return one
of the following: `HIT`, `STAND`, `SPLIT`, `DOUBLE`.

`wager_func` should be a function that will determine how much the player will
wager in a hand. Like the function used for `strategy_func` it can take as
arguments variables on the status of the game. It must return a number that is
within the minimum and maximum bets allowed, and no more than the player's
bankroll.

`insurance_func` should be a function that will determine if a player takes
insurance when the dealer is showing an ace. It must return `True` or `False`.

The `Game` class has one required argument and two optional ones. `players`
is a list of instances of the `Players` class that will be used in the game.
`rules` can be a dictionary containing changes to the game's default rules to
run the simulation under different scenarios. An explanation of how the
dictionary should be structured is below. Finally, `verbose` is a boolean
indicator for whether or not you want information printed out as the game is
played.

Running a simulation can be done in a few lines of code:

```python
from py21 import Game, Player

# initiate Player object
player = Player(100)
# initiate Game object
game = Game([player])

# run simulation 1,000,000 times
game.simulate(1000000)
```

## Updating Game Parameters

To update a rule in the game, use this dictionary format:

`{param: new_rule}`

For example, here is how to change the blackjack payout from 3:2 to 6:5:

```python
from py21 import Game, Player

rules = {"blackjack_payout": 1.2}

player = Player(100)
game = Game([player], rules)

game.simulate(1000000)
```

A list of the game parameters you can update can be found [here](https://github.com/andersonfrailey/blackjack/blob/master/docs/default_rules.md).

As of version 1.6.0, there is also a CLI for `py21`. To use it, run `blackjack`
from the command line.
