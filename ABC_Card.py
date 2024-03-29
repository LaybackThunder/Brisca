import pygame
import pygwidgets
from abc import ABC

# Card is an abstract base class design for a generic playing card.
class Card(ABC):

    BACK_OF_CARD_IMAGE = pygame.image.load('images/back-side.jpg')
    
    def __init__(self, window, cardName=None):
        """Initialize playing card attributes and passing it window properties."""
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
    
    def setCardId(self, iDCounter):
        """Card remembers a number to recognize its place in the hand."""
        self.cardId = iDCounter

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
        """Display image on screen."""
        self.images.draw()

    def cardSelected(self):
            """Card moves up 25 pixels."""
            self.images.moveY(-25) # Move card 25 pixels up the screen to id selcted card
    
    def deSelectCard(self):
            """Card moves down 25 pixels."""
            self.images.moveY(25) # Return to original position

    def setCardClickedToFalse(self):
        self.oCardClicked = False

    def handleEvent(self, event):
        """
        Returns a bool if card is clicked or unclicked.
        Card moves upwards if the card was clicked.
        When card is unclicked, it moves downwards. 
        """
        if self.images.handleEvent(event):
            if self.oCardClicked == False:
                self.oCardClicked = True # To avoid moving it up for every click
                self.cardSelected() # Moves upwards
                return True
                    
            elif self.oCardClicked: # It was de-selected (clicked again)
                self.oCardClicked = False # Now it can be clicked to move up
                self.deSelectCard() # Moves back to position (downwards)
                return True





   
