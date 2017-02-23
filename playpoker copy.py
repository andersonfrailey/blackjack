#  File: playpoker.py
#  Description: Simulate a game of 5 card draw
#  Student's Name: Anderson Frailey
#  Student's UT EID: ajf2329
#  Course Name: CS 313E 
#  Unique Number: 50597
#
#  Date Created: 9/20/15
#  Date Last Modified: 9/24/15


#import the random number generator
# this is needed to shuffle the cards into a random order

import random

class Card (object):
  RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

  SUITS = ('C', 'D', 'H', 'S')

  def __init__ (self, rank, suit):
    # each Card object consists of two attributes: a rank
    #    and a suit
    self.rank = rank
    self.suit = suit
    
  def __str__ (self):
    # print J, Q, K, A instead of 11, 12, 13, 14
    if self.rank == 14:
      rank = 'A'
    elif self.rank == 13:
      rank = 'K'
    elif self.rank == 12:
      rank = 'Q'
    elif self.rank == 11:
      rank = 'J'
    else:
      rank = self.rank
    return str(rank) + self.suit

  # you'll find the following methods to be useful:  they 
  #    allow you to compare Card objects

  def __eq__ (self, other):
    return (self.rank == other.rank)

  def __ne__ (self, other):
    return (self.rank != other.rank)

  def __lt__ (self, other):
    return (self.rank < other.rank)

  def __le__ (self, other):
    return (self.rank <= other.rank)

  def __gt__ (self, other):
    return (self.rank > other.rank)

  def __ge__ (self, other):
    return (self.rank >= other.rank)


class Deck (object):

  def __init__ (self):
    # self.deck is the actual deck of cards
    # create it by looping through all SUITS and RANKS
    #    and appending them to a list
    self.deck = []
    for suit in Card.SUITS:
      for rank in Card.RANKS:
        card = Card (rank, suit)
        self.deck.append (card)

  def shuffle (self):
    # the shuffle method in the random package reorders
    #    the contents of a list into random order
    random.shuffle (self.deck)

  def deal (self):
    # if the deck is empty, fail:  otherwise pop one
    #    card off and return it
    if len(self.deck) == 0:
      return None
    else:
      return self.deck.pop(0)
      
class Poker (object):
  #
  # when you create an object of class Poker, you
  #    create a deck, shuffle it, and deal cards
  #    out to the players.
  #
  def __init__ (self, numHands):
    self.deck = Deck()              # create a deck
    self.deck.shuffle()             # shuffle it
    self.hands = []
    numCards_in_Hand = 5
    self.ranks = []
    self.totalPoints = []
    self.tieHands = []

    for i in range (numHands):
      # deal out 5-card hands to numHands players
      # you'd actually get shot if you dealt this
      #    way in a real poker game (5 cards to
      #    the first player, 5 to the next, etc.)
      hand = []
      for j in range (numCards_in_Hand):
        hand.append (self.deck.deal())
      self.hands.append (hand)

  def is_royal(self,hand):
    # Boolean for if it is a royal flush, find the suit of the royal flush
    royal = True
    cardRank = 14
    aimSuit = hand[0].suit
    # Loop through each card to see if it meets the criteria
    for i in range(0,len(hand)):
      if hand[i].rank == cardRank and hand[i].suit == aimSuit:
        cardRank = cardRank -1
      else:
        royal = False
        break
    # Return corresponding values
    if royal == True:
      points = 10 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points, 'Royal Flush', True
    else:
      return 0,'none',False

  def is_straight_flush(self,hand):
    # Boolean, find the high card and the suit
    strFlush = True
    cardRank = hand[0].rank
    aimSuit = hand[0].suit
    # Loop through to see if cards meet criteria
    for i in range (0,len(hand)):
      if hand[i].rank == cardRank and hand[i].suit == aimSuit:
        cardRank = cardRank - 1
      else:
        strFlush = False
        break
    if strFlush == True:
      points = 9 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points, 'Straight Flush', True
    else:
      return 0,'none',False
    
  def is_four(self,hand):
    # Check if there are four of a kind
    if hand[0].rank == hand[1].rank and hand[1].rank == hand[2].rank and hand[2].rank == hand[3].rank:
      points = 8 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points,'Four of a Kind',True
    elif hand[1].rank == hand[2].rank and hand[2].rank == hand[3].rank and hand[3].rank == hand[4].rank:
      points = 8 * 13**5 + hand[1].rank * 13**4 + hand[2].rank * 13**3 + hand[3].rank * 13**2 + hand[4].rank * 13 + hand[0].rank
      return points,'Four of a Kind',True
    else:
      return 0,'none',False

  def is_full(self,hand):
    # Check for triples and pairs
    if hand[0].rank == hand[1].rank and hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
      points = 7 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points,'Full House',True
    elif hand[0].rank == hand[1].rank and hand[2].rank == hand[3].rank and hand[3].rank == hand[4].rank:
      points = 7 * 13**5 + hand[2].rank * 13**4 + hand[3].rank * 13**3 + hand[4].rank * 13**2 + hand[0].rank * 13 + hand[1].rank
      return points,'Full House',True
    else:
      return 0,'none', False

  def is_flush(self,hand):
    # Check if all suits match
    if hand[0].suit == hand[1].suit and hand[1].suit==hand[2].suit and hand[2].suit == hand[3].suit and hand[3].suit==hand[4].suit:
      points = 6 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points,'Flush',True
    else:
      return 0,'none',False

  def is_straight(self,hand):
    # Find high card
    cardRank = hand[0].rank
    straight = True
    # Loop to see if there is a match
    for i in range (0,len(hand)):
      if hand[i].rank == cardRank:
        cardRank = cardRank -1
      else:
        straight = False
        break
    # Return necessary value
    if straight == True:
      points = 5 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points,'Straight',True
    else:
      return 0,'none',False

  def is_three(self,hand):
    # Check for possible triples
    if hand[0].rank == hand[1].rank and hand[1].rank == hand[2].rank:
      points = 4 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return 4,'Three of a Kind',True
    elif hand[1].rank == hand[2].rank and hand[2].rank == hand[3].rank:
      points = 4 * 13**5 + hand[1].rank * 13**4 + hand[2].rank * 13**3 + hand[3].rank * 13**2 + hand[0].rank * 13 + hand[4].rank
      return points,'Three of a Kind',True
    elif hand[2].rank == hand[3].rank and hand[3].rank == hand[4].rank:
      points = 4 * 13**5 + hand[2].rank * 13**4 + hand[3].rank * 13**3 + hand[4].rank * 13**2 + hand[0].rank * 13 + hand[1].rank
      return points,'Three of a Kind',True
    else:
      return 0,'none',False

  def is_two(self,hand):
    # Check for multiple pairs
    if hand[0].rank == hand[1].rank:
      if hand[2].rank == hand[3].rank:
        points = 3 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
        return points,'Two Pair',True
      elif hand[3].rank == hand[4].rank:
        points = 3 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[3].rank * 13**2 + hand[4].rank * 13 + hand[2].rank
        return points,'Two Pair',True
      else:
        return 0,'none',False
    elif hand[1].rank == hand[2].rank and hand[3].rank == hand[4].rank:
      points = 3 * 13**5 + hand[1].rank * 13**4 + hand[2].rank * 13**3 + hand[3].rank * 13**2 + hand[4].rank * 13 + hand[1].rank
      return points,'Two Pair',True
    else:
      return 0,'none',False

  def is_pair(self,hand):
    # Search for all possible pairs
    if hand[0].rank == hand[1].rank:
      points = 2 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points,'Pair',True
    elif hand[1].rank == hand[2].rank:
      points = 2 * 13**5 + hand[1].rank * 13**4 + hand[2].rank * 13**3 + hand[0].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
      return points,'Pair',True
    elif hand[2].rank == hand[3].rank:
      points = 2 * 13**5 + hand[2].rank * 13**4 + hand[3].rank * 13**3 + hand[0].rank * 13**2 + hand[1].rank * 13 + hand[4].rank
      return points,'Pair',True
    elif hand[3].rank == hand[4].rank:
      points = 2 * 13**5 + hand[3].rank * 13**4 + hand[4].rank * 13**3 + hand[0].rank * 13**2 + hand[1].rank * 13 + hand[2].rank
      return points,'Pair',True
    else:
      return 0,'none',False

  def is_high(self, hand):
    # Return high card
    points = 1 * 13**5 + hand[0].rank * 13**4 + hand[1].rank * 13**3 + hand[2].rank * 13**2 + hand[3].rank * 13 + hand[4].rank
    return points,'High Card',True

  def play (self):

    # List to store the hand rankings
    for i in range (len(self.hands)):
      # the method "sorted" returns a sorted list without
      #   altering the original list.  reverse = True
      #   makes it sort in decreasing order
      sortedHand = sorted (self.hands[i], reverse = True)
      hand = ''
      for card in sortedHand:
        hand = hand + str(card) + ' '
      print ('Hand ' + str(i + 1) + ': ' + hand)
      # Boolean for handFound
      handFound = False
      # While handFound is false, search for the hand
      if handFound == False:
        points, handRank, handFound = self.is_royal(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_straight_flush(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_four(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_full(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_flush(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_straight(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_three(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_two(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_pair(sortedHand)
      if handFound == False:
        points, handRank, handFound = self.is_high(sortedHand)
      # Append each hand's rank and the total points from it to respective lists
      self.ranks.append(handRank)
      self.totalPoints.append(points)
      
    print ('')
    for i in range(0,len(self.ranks)):
      print('Hand '+ str(i+1)+':', self.ranks[i])
    print ('')

    # Find the hand with the most points
    maxPoints = 0
    winner = 0
    for i in range (0,len(self.totalPoints)):
      if self.totalPoints[i] > maxPoints:
        maxPoints = self.totalPoints[i]
        winner = i
      elif maxPoints == self.totalPoints[i]:
        self.tieHands.append(i)
    if len(self.tieHands) == 0:
      print('Hand',str(winner+1), 'wins.')
    else:
      for i in range(0,len(self.tieHands)+1):
        print('Hand', str(i+1), 'ties.')


def main():

  numHands = int (input ('Enter number of hands to play: '))

  # need at least 2 players but no more than 6
  while (numHands < 2 or numHands > 6):
    numHands = int (input ('Enter number of hands to play: '))

  # create a Poker object:  create a deck, shuffle it, and
  # deal out the cards
  game = Poker (numHands)

  # play the game
  game.play()

main()
