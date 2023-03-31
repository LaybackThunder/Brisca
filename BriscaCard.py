import pygame
import pygwidgets
from ABC_Card import Card

class BriscaCard(Card):
    BACK_OF_CARD_IMAGE = pygame.image.load('images/back-side.jpg')
    
    # Created defult values in init method to get the ghost player to work    
    def __init__(self, window, suit='Clubs', rank='2', rankValue=2, rankPoints=0):
        
        self.suit = suit
        self.rank = rank 
        self.rankValue = rankValue
        self.rankPoints = rankPoints
        briscaCardName = rank + " of " + suit
        super().__init__(window, cardName=briscaCardName)
    
    def getSuit(self):
        return self.suit
    
    def getRank(self):
        return self.rank

    def getRankValue(self):
        return self.rankValue
    
    def getRankPoints(self):
        return self.rankPoints