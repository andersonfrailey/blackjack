# Blackjack

`py21` is a blackjack simulator. Users can run the simulation using the
default rules or specify their own. Additionally, users can test their own
playing and betting strategies.

## Installation

Right now `py21` can only be installed from source. Clone or download this
repository, then navigate to the directory you cloned to and run
`pip install -e .`.

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
such as the player's hand, dealer's up card, and the count.

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

### Parameters currently available to be modified:

#### `soft_stand`

Whether or not the dealer must stand on a soft total.
Default value: True
Possible values: True, False

#### `stand_total`

Hand value the dealer must reach before they can stand.
Default value: 17
Possible values: 4-21

#### `double_after_split`

Whether or not a player can double down after splitting a pair.
Default value: True
Possible values: True, False

#### `payout`

Payout for a winning hand.
Default value: 1 (1:1)
Possible values: 0-9e99

#### `blackjack_payout`

Total payout if the player has blackjack.
Default value: 1.5 (3/2)
Possible values: 0-9e99 (infinity)

#### `shuffle_freq`

How often the deck is shuffled. If this value is greater than one, the deck
will be shuffled after that many hands are played. If it is less than one, the
deck will be shuffled when that percentage of the deck is left.
Default value: 4
Possible values: 0-9e99 (note: if the shuffle frequency is too low, an
error will be raised when the deck runs out of cards)

#### `min_bet`

Minimum bet required.
Default value: 5
Possible Values: 0-`max_bet

#### `max_bet`

Maximum bet allowed.
Default value: 500
Possible values: `min_bet`-9e99

#### `max_players`

Maximum number of players allowed in a game.
Default value: 10
Possible values: 1-9e99

#### `insurance_allowed`

Whether or not a player is allowed to take insurance when the dealer shoes an ace.
Default value: True
Possible values: True, False

#### `insurance_pct`

What share of a player's original bet they must pay to purchase insurance.
Default value: 0.5
Possible values: 0-1