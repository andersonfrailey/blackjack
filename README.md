# Blackjack

`blackjack` is a blackjack simulator. Users can run the simulation using the
default rules or specify their own. Additionally, users can test their own
playing and betting strategies.

## Using `blackjack`

To run the simulator, the user must initiate one instance of the `Game` class
and at least one instance of the `Player` class.

The `Player` class requires one input, `bankroll`, and has two optional inputs,
`strategy_func` and `wager_func`.
`bankroll` should be an numerical value indicating the bankroll
the player will be starting with.

`strategy_func` should be a function that will
return what action the player will take in a given situation. This function
can take as inputs a number of variables containing information about the game
such as the player's hand, dealer's up card, and the count.

`wager_func` should be a function that will determine how much the player will
wager in a hand. Like the function used for `strategy_func` it can take as
arguments variables on the status of the game.

The `Game` class has two required arguments and two optional ones. `num_decks`
is an integer for the number of decks used in the game, `players` is a list of
instances of the `Players` class that will be used in the game. `rules` can be
a dictionary containing changes to the game's default rules to run the simulation
under different scenarios. An explanation of how the dictionary should be
structured is below. Finally, `verbose` is a boolean indicator for whether or
not you want information printed out as the game is played.

Running a simulation can be done in a few lines of code:

```python
from blackjack import Game, Player

# initiate Player object
player = Player(100)
# initiate Game object
game = Game(1, [player])

# run simulation 1,000,000 times
game.simulate(1000000)
```

## Updating Game Parameters

To update a rule in the game, use this dictionary format:

`{param: [{"value": new_rule}]}`

For example, here is how to change the blackjack payout from 3:2 to 6:5:

```python
from blackjack import Game, Player

rules = {"blackjack_payout": [{"value": 1.2}]}}

player = Player(100)
game = Game(1, [player], rules)

game.simulate(1000000)
```