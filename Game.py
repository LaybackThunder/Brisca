import pygwidgets
from Deck import *
from Card import *

class Game():
    # Class Variables
    HAND_CARD_OFFSET = 20 # player's cards buffer between each other
    PLAYER2_HAND_CARDS_TOP = 400
    PLAYER1_HAND_CARDS_BOTTOM = 100
    CARDS_LEFT = 75
    DISPLAY_STARTING_HANDS = 6
    MAX_HAND = 3
    

    def __init__(self, window):
        """Initisialize attributes."""
        self.window = window
        self.oDeck = Deck(self.window)
        self.potScore = 0
        self.potScoreText = pygwidgets.DisplayText(window, (450, 164),
                                        f'Pot Score: {self.potScore}',
                                        fontSize=36, textColor=(255, 255, 255))
        
        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                        f'', width=900, justified='center'
                                        fontSize=36, textColor=(255, 255, 255))
        
        # Sounds go here
            # Card shuffle
            # Win sound
            # Lost sound
        
        # Calculating Players card positions within the player's hand
        self.cardXPositionList = [] # Both players can share X position
        thisLeft = Game.CARDS_LEFT # Starting card to the left of hand
        # Calculate the x positions of all cards, once
        for cardNum in range(Game.DISPLAY_STARTING_HANDS): # six cards
            self.cardXPositionList.append(thisLeft)
            thisLeft += Game.HAND_CARD_OFFSET
        
        self.reset() # start a round of the game
    
    def reset(self):
        pass

        