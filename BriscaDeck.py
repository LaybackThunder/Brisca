import random
from ABC_Deck import Deck # Module
from BriscaCard import *

class BriscaDeck(Deck):

    # Brisca Deck Constants
    SUIT_TUPLE = ('Swords', 'Coins', 'Cups', 'Clubs')
    # Deck example: '2' is rank, value is list [rankValue, rankPoints] of rank
    BRISCA_DICT = {
        '2':[2, 0], '3':[13, 10], 
        '4':[4, 0], '5':[5, 0], 
        '6':[6, 0], '7':[7, 0],
        'Jack':[10, 2], 'Knight':[11, 3], 
        'King':[12, 10], 'Ace':[14, 11]
        }
        
    def __init__(self, window, loc):

        self.startingDeckList = []
        self.playingDeckList = []
    
        # Create a deck
        for suit in BriscaDeck.SUIT_TUPLE:
            for rank, value in BriscaDeck.BRISCA_DICT.items():
                oCard = BriscaCard(window, suit, rank, rankValue=value[0], rankPoints=value[1])
                self.startingDeckList.append(oCard)

        # Playing deck is shuffled
        self.shuffle()

        # Deck's location on the display is added
        for oCard in self.playingDeckList:
            oCard.setLoc(loc)
    
    def isThereADeck(self):
        """Returns bool after identifying if there is a deck or not."""
        if len(self.playingDeckList) > 0:
            return True
        else:
            return False 

    def shuffle(self):
        # Copy the starting deck and save it in the playing deck list
        self.playingDeckList = self.startingDeckList.copy()
        # Conceal all cards before you shuffle
        for oCard in self.playingDeckList:
            oCard.conceal()
        # shuffle using the random module
        random.shuffle(self.playingDeckList)

    def drawCard(self):
        """ Card is drawn from the deck: 
            Returns an obj Card or None if there are no more cards.
        """
        # Checks to see if there are any cards
        if len(self.playingDeckList) == 0:
            return None
        # Returns one card from the top of the deck
        else:
            oCard = self.playingDeckList.pop()
            return oCard
    
    def addCardToDeck(self, oCard, loc):
        """conceal oCard and Put it back into the deck"""
        oCard.conceal()
        oCard.setLoc(loc)
        self.playingDeckList.append(0, oCard)

    def draw(self):
        """Display every card on screen"""
        for oCard in self.playingDeckList:
            oCard.draw()