# Default Game Parameters

## `soft_stand`

Whether or not the dealer must stand on a soft total.

Default value: True

Possible values: True, False

## `stand_total`

Hand value the dealer must reach before they can stand.

Default value: 17

Possible values: 4-21

## `double_after_split`

Whether or not a player can double down after splitting a pair.

Default value: True

Possible values: True, False

## `payout`

Payout for a winning hand.

Default value: 1 (1:1)

Possible values: 0-9e99

## `blackjack_payout`

Total payout if the player has blackjack.

Default value: 1.5 (3/2)

Possible values: 0-9e99 (infinity)

## `shuffle_freq`

How often the deck is shuffled. If this value is greater than one, the deck
will be shuffled after that many hands are played. If it is less than one, the
deck will be shuffled when that percentage of the deck is left.

Default value: 4

Possible values: 0-9e99 (note: if the shuffle frequency is too low, an
error will be raised when the deck runs out of cards)

## `min_bet`

Minimum bet required.

Default value: 5

Possible Values: 0-`max_bet

## `max_bet`

Maximum bet allowed.

Default value: 500

Possible values: `min_bet`-9e99

## `max_players`

Maximum number of players allowed in a game.

Default value: 10

Possible values: 1-9e99

## `insurance_allowed`

Whether or not a player is allowed to take insurance when the dealer shoes an ace.

Default value: True

Possible values: True, False

## `insurance_pct`

What share of a player's original bet they must pay to purchase insurance.

Default value: 0.5

Possible values: 0-1

## `insurance_payout`

If the player purchases insurance and the dealer has blackjack, the player will
receive this decimal percent of their bet back.

Default value: 1

Possible values: 0-9e99

## `surrender_allowed`

Whether or not the player is allowed to surrender a hand.

Default value: True

Possible values: True, False

NOTE: This parameter has not be implemented yet, therefore changing it will have
      no impact on game play

## `num_decks`

The number of decks the game will be played with

Default value: 8

Possible values: 1-9e99