import pygame
import random
from ABC_Deck import Deck
from BriscaCard import *

class BriscaDeck(Deck):
        
    def __init__(self, window, loc, SUIT, RANK_VALUE_DICT):

        self.startingDeckList = []
        self.playingDeckList = []
    
        # Create a deck
        for suit in SUIT:
            for rank, value in RANK_VALUE_DICT.items():
                oCard = BriscaCard(window, suit, rank, rankValue=value[0], rankPoints=value[1])
                self.startingDeckList.append(oCard)

        # Playing deck is shuffled
        self.shuffle()

        # Deck's location on the display is added
        for oCard in self.playingDeckList:
            oCard.setLoc(loc)

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
            Returns an obj Card or False (no more cards).
        """
        # Checks to see if there are any cards
        if len(self.playingDeckList) == 0:
            print('Ha! No more cards, go and get a life!')
            return False
        # Returns one card from the top of the deck
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

# Print Test BriscaDeck
if __name__ == "__main__":

    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500

    SUIT_TUPLE = ('Swords',)
    # Example: '2' is rank, value is list [pointsValue, trcikValue]
    BRISCA_DICT = {'2':[0, 2], '3':[0, 13], '4':[0, 4], '5':[0, 5],
                        '6':[0, 6], '7':[0, 7], 'Jack':[2, 10],
                        'Knight':[3, 11], 'King':[4, 12], 'Ace':[11, 14]}

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oDeck = BriscaDeck(window, (0,0), SUIT_TUPLE, BRISCA_DICT)

    for i in range(1, 10):
        oCard = oDeck.drawCard()
        print(f"Name: {oCard.getName()}, Rank: {oCard.getRankValue()}, Rank Points: {oCard.getRankPoints()}")