"""
Script allowing the user to play along
"""

from game import Game
from deck import Deck
import play_utils


def deck_manager():
    play.deck.create_deck()
    play.deck.shuffle()


print "Welcome to the table"
decks = int(input('How many decks would you like to play with? '))
verbose = raw_input('Do you want stats? (y/n) ').lower()

# If they want stats, simulate a game
if verbose == 'y':
    sim = Game()
    print 'Collecting data'
    sim.sim_game(decks, 1, 10000)
    sim.data.convert()

# Create the Game class used to play
play = Game()
play.deck = Deck(decks)
deck_manager()
cut = len(play.deck) * .25
play.players = 1
playing = 'y'

# Play game until user decides to quit
while playing != 'n':
    # Check deck length
    if len(play.deck) <= cut:
        deck_manager()
    # Deal hand, print total and dealer up
    start_count = play.card_count
    play.deal_hand()
    # Total for probability calculation
    tot = play.players_list[0]['total']
    soft = play.players_list[0]['soft']
    print ('Delt: {}, {}'.format(play.players_list[0]['card one'],
                                 play.players_list[0]['card two']))
    if not soft:
        total = play.players_list[0]['total']
    else:
        large = play.players_list[0]['total']
        small = large - 10
        total = '{}/{}'.format(small, large)
    print 'Total: {}'.format(total)
    d_up = play.dealer['card one']
    print 'Dealer is showing: {}'.format(d_up)
    # Check probability of winning if player asks for it
    if verbose == 'y':
        p = play_utils.probability(sim.data.results_df, start_count, tot,
                                   d_up.rank)
        print 'Player wins or pushes this {} percent of the time'.format(p)
        # Probability of busting when hitting this hand, if total < 17
        if tot <= 17:
            b = play_utils.bust(sim.data.hit_df, play.card_count,
                                play.players_list[0]['total'], soft)
            print 'Player busts {} percent of the time hitting this'.format(b)
        else:
            print "Don't hit this"

    # Clear player list and dealer hand
    play.dealer = {'total': 0, 'soft': False, 'taken': 0}
    del play.players_list[:]
    playing = raw_input('Keep playing?(y/n) ').lower()
