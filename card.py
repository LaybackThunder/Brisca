import pygame
import pygwidgets

class Card():

    BACK_OF_CARD_IMAGE = pygame.image.load('images/back-side.jpg')
    
    def __init__(self, window, suit, rank, value, trickValue):
        self.window = window
        self.suit = suit
        self.rank = rank
        self.cardName = rank + " of " + suit
        self.value = value
        self.trickValue = trickValue
        fileName = "images/" + self.cardName + ".jpg"
        # Set some starting location; use setLoc below to change
        self.images = pygwidgets.ImageCollection(window, (0, 0),
                                                {'front': fileName,
                                                'back': Card.BACK_OF_CARD_IMAGE}, 'back')
    
    def conceal(self):
        self.images.replace('back')
    
    def reveal(self):
        self.images.replace('front')
    
    def getName(self):
        return self.cardName
    
    def getValue(self):
        return self.value

    def getTrickValue(self):
        return self.trickValue

    def getSuit(self):
        return self.suit
    
    def getRank(self):
        return self.rank
    
    def setLoc(self, loc):
        self.images.setLoc(loc) # call the setLoc method of the ImageCollection
    
    def getLoc(self): # get the location from the ImageCollection
        loc = self.images.getLoc()
        return loc

    def draw(self):
        self.images.draw()
        