import pygame
import pygwidgets
from abc import ABC

# Card is now an abstract base class
class Card(ABC):

    BACK_OF_CARD_IMAGE = pygame.image.load('images/back-side.jpg')
    
    def __init__(self, window, cardName=None):
        self.window = window
        self.cardName = cardName
        fileName = "images/" + self.cardName + ".jpg"
        self.images = pygwidgets.ImageCollection(window, (0, 0),
                                                {'front': fileName,
                                                'back': Card.BACK_OF_CARD_IMAGE}, 'back')
        self.oCardClicked = False
        self.cardId = 0
    
    def getCardId(self):
        return self.cardId 

    def getOcardClicked(self):
        return self.oCardClicked
    
    def setCardId(self, iD):
        """Card remembers a number to recognize its place in the hand."""
        self.cardId = iD

    def setLoc(self, loc):
        self.images.setLoc(loc)
        
    def setRotation(self, degrees):
        """
        Positive numbers are clockwise, 
        negative numbers are counter-clockwise.
        """
        self.images.rotate(degrees)
    
    def getName(self):
        return self.cardName
        
    def getLoc(self):
        loc = self.images.getLoc()
        return loc
    
    def disable(self):
        """Disable the card's ability to be clicked."""
        self.images.disable()
    
    def enable(self):
        """Enable the card's ability to be clicked."""
        self.images.enable()

    def conceal(self):
        self.images.replace('back')
    
    def reveal(self):
        self.images.replace('front')

    def draw(self):
        """Display Image on screen."""
        self.images.draw()

    def cardSelected(self):
            self.images.moveY(-25) # Move card 25 pixels up the screen to id selcted card
    
    def deSelectCard(self):
            self.images.moveY(25) # Return to original position

    def handleEvent(self, event):
        """Returns a bool if card is clicked and moves upwards if the card was clicked."""
        if self.images.handleEvent(event):
            
            if self.oCardClicked == False:
                self.oCardClicked = True # To avoid moving it up for every click
                self.cardSelected() # Moves upwards
                return True
                
            elif self.oCardClicked: # It was de-selected (clicked again)
                self.oCardClicked = False # Now it can be clicked to move up
                self.deSelectCard() # Moves back to position
                return True





   
