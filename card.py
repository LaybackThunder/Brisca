import pygame
import pygwidgets

class Card():

    BACK_OF_CARD_IMAGE = pygame.image.load('images/back-side.jpg')
    
    def __init__(self, window, suit='Clubs', rank='2', value=0, trickValue=2):
        self.window = window
        self.window_rect = window.get_rect()
        self.clicked = False
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
        self.images_rect = self.images.getRect()
    
    def selectedCardEvent(self, event):
        """Checks if card was clicked."""
        if self.images.handleEvent(event):
            if self.clicked == False:
                print('Clicked! BUH!') # Because I can
                self.images.moveY(-25) # Move card 25 pixels to id selcted card
                self.clicked = True # To avoid moving it up for every click
                
            elif self.clicked:
                print('un clicked')
                self.images.moveY(25) # Return to original position
                self.clicked = False
            
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
    
    def setRotation(self, degrees):
        """Positive numbers are clockwise, negative numbers are counter-clockwise."""
        self.images.rotate(degrees)

    def draw(self):
        self.images.draw()
        