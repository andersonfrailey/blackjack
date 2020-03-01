# Data Collection

Py21 collects data for each hand as well as the result every time a player
take a hit.

## Hand Data

* `blackjack`: boolean indicator for whether or not the player has blackjack
* `cards`: list of the rank of all the cards the player received
* `card_one_rank`: rank of the first card the player received
* `card_one_value`: value of the first card the player received
* `card_two_rank`: rank of the second card the player received
* `card_two_value`: value of the second card the player received
* `dealer_blackjack`: boolean indicator for whether or not the dealer had blackjack
* `dealer_total`: the dealer's total at the end of the round
* `dealer_up`: rank of the dealer's up card
* `end_bankroll`: the player's bankroll at the end of the round
* `from_split`: boolean indicator for whether or not the hand comes after the player
  split their starting hand
* `hand_id`: unique ID for the hand
* `insurance`: boolean indicator for whether or not the player took insurance
* `num_cards`: total number of cards in a player's hand at the end of the round
* `result`: result of the hand. Can be win, loss, or push
* `round_id`: unique ID for the round
* `soft`: boolean indicator for whether or not the player's total is soft
* `start_bankroll`: the player's bankroll at the start of the round
* `start_total`: the player's total from their first two cards
* `surrender`: boolean indicator for whether or not the hand was surrendered
* `total`: the player's final total
* `wager`: amount the player wagered on the hand

## Hit Data

* `action`: action the player took (this will always be HIT)
* `card_received_rank`: rank of the card received
* `card_received_value`: value of the card received
* `hand_id`: unique ID for the hand
* `new_total`: hand total after receiving the card
* `round_id`: unique ID for the round
* `soft`: boolean indicator for whether or not the hand was soft before the hit
* `start_count`: count of the deck before the player took the new card
* `start_other_count`: number of cards with a value not ten in the deck before the hit
* `start_ten_count`: number of cards with a value of ten in the deck before the hit
* `start_true_count`: true count before the player took the new card
* `start_total`: hand total before the hit