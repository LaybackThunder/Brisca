import pygame
import pygwidgets

class Card():

    BACK_OF_CARD_IMAGE = pygame.image.load('images/back-side.jpeg')
    
    def __init__(self, window, suit, rank, trickValue, pointValue):
        self.window = window
        self.suit = suit
        self.rank = rank
        self.cardName = f"{rank} of {suit}"
        self.trickValue = trickValue
        self.pointValue = pointValue