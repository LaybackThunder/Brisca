import pygwidgets
import random
from BriscaDeck import *


class Game():

    HAND_LIMIT = 3
    DECK_LOC = (860, 360)
    TRUMP_LOC = (800, 360)

    GHOST_HAND_Y_LOCATION = 650
    GHOST_HAND_LOC_LIST = [(300, GHOST_HAND_Y_LOCATION), (500, GHOST_HAND_Y_LOCATION)]
    GHOST_OBJ_Card = None # ----> Ghost player on hold; code later

    TRICK_CARDS_LOC_Y = 360
    TRICK_LOCATION_LIST = [(250, TRICK_CARDS_LOC_Y), (500, TRICK_CARDS_LOC_Y)]

    def __init__(self, window, player, SUIT, BRISCA_DICT):
        """Initializing data and objects."""
        self.window = window
        self.oDeck = BriscaDeck(self.window, Game.DECK_LOC, SUIT, RANK_VALUE_DICT=BRISCA_DICT)
        self.playerList = [player]

        self.trumpCard = self.oDeck.drawCard()
        self.trickList = [] # Where cards battle
        self.dealerPot = [] # When there is a tie, the dealer holds cards
        self.ghostHandList = [] # Holds cards for ghost player
        self.oCardClicked = False

        self.drawCardButton = pygwidgets.TextButton(window, (140, 840),
                                    'Draw', width=100, height=45)

        self.trickButton = pygwidgets.TextButton(window, (20, 840),
                                    'Trick', width=100, height=45)
        self.trickButton.disable()
        self.trumpCard.reveal() 
        self.trumpCard.setLoc(Game.TRUMP_LOC)
        self.trumpCard.setRotation(-90)
    
    # Polymorphism section 
    def enterTrick(self, oPlayer):
        """Place card in the middle of the board."""
        oTrickCard = oPlayer.enterTrick()
        trickIndex = len(self.trickList)
        self.trickList.append(oTrickCard)
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))

        # Code latter the battle step of the game

    def drawCard(self, oPlayer):
        """Player draws a card."""
        if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:
            oCard = self.oDeck.drawCard()
            oPlayer.drawCard(oCard)
        else:
            print('Hand is full!')        

    def handleEvent(self, event):
        """Handles pygame events"""
        # If player is turnPlayer do below (code later)
        for oPlayer in self.playerList:

            # Check player draw
            if self.drawCardButton.handleEvent(event):
                    print('Draw button pressed.')
                    self.drawCard(oPlayer)

            # Check if player's card are clickable
            if oPlayer.handleEvent(event):
                self.trickButton.enable()
                    # Should selected card be returned?
            else:
                self.trickButton.disable()
            
            # Check for trick button
            if self.trickButton.handleEvent(event):
                print('Trick button pressed!')
                self.enterTrick(oPlayer)          

    def draw(self):
        """Display cards to screen"""
        # GUI components
        self.trickButton.draw()
        self.drawCardButton.draw()

        # Game elements
        if self.trumpCard:
            self.trumpCard.draw()
        if self.trickList:
            for oTrickCard in self.trickList:
                oTrickCard.draw()
        for player in self.playerList:
            player.draw()
        self.oDeck.draw()

        # for ghostCard in self.ghostHandList:
            # ghostCard.draw()