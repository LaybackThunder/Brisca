import pygame
import pygwidgets
from Hand import *

class Player():

    def __init__(self, window):
        self.window = window
        self.turnPlayer = False
        self.potList = []
        self.oHand = Hand(window)

    def getTurnPlayer(self):
        return self.turnPlayer

    def setTurnPlayerTrue(self):
        if self.turnPlayer:
            print('Player is already turnPlayer (True)!')
        else:
            self.turnPlayer = True
    
    def setTurnPlayerFalse(self):
        if self.turnPlayer == False:
            print('Player is already NOT turnPlayer (False)!')
        else:
            self.turnPlayer = False 

    # Polymorphism section
    def enterTrick(self):
        """Place card in the middle of the board."""
        # Asks had to give card, return card.
        oTrickCard = self.oHand.enterTrick()
        return oTrickCard

    def getLengthCardsOnHand(self):
        """Returns the total number of cards on hand."""
        xLenghtOfCardsOnHand = self.oHand.getLengthCardsOnHand()
        return xLenghtOfCardsOnHand

    def getCardsOnHand(self):
        """Returns cards on hand."""
        cardList = self.oHand.getCardsOnhand()
        return cardList

    def drawCard(self, oCard=None):
        """
        Adds card to player's hand.
        If none; return no card error.
        """
        self.oHand.drawCard(oCard)

    def playCardFromHand(self, oCard=None):
        """
        Removes card from player's hand.
        If none; return no card error.
        else; return card.
        """
        self.oHand.playCardFromHand(oCard)

    def handleEvent(self, event):
        """Returns a bool if any card on hand was clicked."""
        oCardClicked = self.oHand.handleEvent(event)
        return oCardClicked
    
    def draw(self):
        """Display hand on screen."""
        self.oHand.draw()