# Default Game Parameters


## `soft_stand`

Whether or not the dealer must stand when they reach their stand threshold with a soft hand.

Default Values: True

Possible Values: True, False

Notes: N/A

## `stand_total`

The dealer must stand when their hand reaches this total or higher.

Default Values: 17

Possible Values: 4-21

Notes: N/A

## `double_after_split`

Whether or not a player can double down after they split a pair.

Default Values: True

Possible Values: True, False

Notes: N/A

## `payout`

Multiplicative payout for winning a hand.

Default Values: 1

Possible Values: 0-9e+99

Notes: N/A

## `blackjack_payout`

Multiplicative payout for a blackjack.

Default Values: 1.5

Possible Values: 0-9e+99

Notes: N/A

## `shuffle_freq`

How often the deck is shuffled

Default Values: 0.25

Possible Values: 0-9e+99

Notes: If this value is less than one, the deck will be shuffled when less than that percent of the deck remains.

## `min_bet`

Minimum bet required.

Default Values: 5

Possible Values: 0-max_bet

Notes: N/A

## `max_bet`

Maximum bet allowed.

Default Values: 500

Possible Values: min_bet-9e+99

Notes: N/A

## `max_players`

Maximum number of players allowed in a game.

Default Values: 10

Possible Values: 1-9e+99

Notes: N/A

## `insurance_allowed`

Boolean indicator for whether a player is allowed to buy insurance when the dealer shows an ace.

Default Values: True

Possible Values: True, False

Notes: N/A

## `insurance_pct`

If a player chooses to take insurance, the wager is for this portion of their original bet.

Default Values: 0.5

Possible Values: 0-1

Notes: N/A

## `insurance_payout`

If the player purchases insurance and the dealer has blackjack, the player will receive this decimal percent of their bet back.

Default Values: 1

Possible Values: 0-9e+99

Notes: N/A

## `surrender_allowed`

Boolean indicator for whether or not a player is allowed to surrender after receiving their hand.

Default Values: True

Possible Values: True, False

Notes: N/A

## `num_decks`

Number of decks used in the game.

Default Values: 8

Possible Values: 1-9e+99

Notes: N/A

## `surrender_after_split`

Boolean indicator for whether a player is allowed to buy insurance when the dealer shows an ace.

Default Values: False

Possible Values: True, False

Notes: N/A

## `max_split_hands`

This is the number of times a player many only split their hand in a single round of play.

Default Values: 3

Possible Values: 1-9e+99

Notes: Be warned that if you set this too high, there is the possibility that you go on a streak of split hands and run out of cards in the deck.

## `split_blackjack_payout`

Multiplicative payout for a blackjack after splitting your hand.

Default Values: 1

Possible Values: 0-9e+99

Notes: N/A

## `hit_split_aces`

boolean indicator for whether a player is allowed to take additional cards after splitting aces.

Default Values: False

Possible Values: True, False

Notes: N/A
