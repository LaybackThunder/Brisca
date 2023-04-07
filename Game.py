import pygwidgets
import random
from BriscaDeck import *

class Game():

    HAND_LIMIT = 3
    DECK_LOC = (860, 360)
    TRUMP_LOC = (750, 360)

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
        self.trumpCard.reveal() 
        self.trumpCard.setLoc(Game.TRUMP_LOC)
        self.trumpCard.setRotation(-90)

        self.trickList = [] # Where cards battle
        self.dealerPot = [] # When there is a tie, the dealer holds cards
        self.ghostHandList = [] # Holds cards for ghost player

        self.drawCardButton = pygwidgets.TextButton(window, (140, 840),
                                    'Draw', width=100, height=45)

        self.trickButton = pygwidgets.TextButton(window, (20, 840),
                                    'Trick', width=100, height=45)
        
        self.swapButton = pygwidgets.TextButton(window, (20, 780),
                                    'Swap', width=100, height=45)
        self.swapButton.disable()
        self.trickButton.disable()

    def battleStep(self):
        """
        Calculates which oTrickCard wins the battle step.
        Sets a turnPlayer by comparing the highest value card.
        Returns True or False for tie.
        """
        player1 = self.trickList[0]['oPlayer']
        player2 = self.trickList[1]['oPlayer']
        player1CardValue = self.trickList[0]['oCard'].getRankValue()
        player2CardValue = self.trickList[1]['oCard'].getRankValue()

        if player1CardValue > player2CardValue:
            print("-------You WIN!")
            player1.setTurnPlayerTrue() # Player1 will have the bool to draw firs
            player2.setTurnPlayerFalse()
            self.playerList = [player1] # Player arrangement decides who draws first
            tie = False
            
        elif player1CardValue < player2CardValue:
            print("-------You LOSE!")
            player2.setTurnPlayerTrue() # Player2 will have the bool to draw first
            player1.setTurnPlayerFalse()
            self.playerList = [player1] # Player arrangement decides who draws first
            tie = False

        else: # If players end in a tie: cards return to deck
            print("-------TIE/n")
            tie = True

        return tie # Return the value of Tie

    # Polymorphism section 
    def enterTrick(self, oPlayer):
        """Place card in the middle of the board and battle."""
        oTrickCard = oPlayer.enterTrick()
        trickIndex = len(self.trickList)
        # Prep for battle: identify card and owner
        playerAndCard = {'oPlayer': oPlayer, 'oCard': oTrickCard}
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))
        self.trickList.append(playerAndCard)
        
        # Battle step of the game
        if len(self.trickList) == 2:
            print("Battle!")
            tie = True
            while tie:
                tie = self.battleStep()
                if tie:
                    tie = False
                else:
                    # Transfer trickCards to potCards
                    self.setPotList()
            print("End of Battle!")

    def setPotList(self):
        """Gives turnPlayer the spoils of war. As in the winning cards."""
        cardsAndOwners = []
        for i in self.trickList.copy(): # Copy, because we are modifying list.
            index = self.trickList.index(i)
            cardAndOwner = self.trickList.pop(index)
            cardsAndOwners.append(cardAndOwner)
        self.playerList[0].setPotList(cardsAndOwners)    

    def getPotList(self):
        """Prints the name of every card in the turnPlayer's potList."""
        potList = self.playerList[0].getPotList()
        return potList

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
                    self.drawCard(oPlayer)

            # Check if player's card are clickable
            if oPlayer.handleEvent(event):
                self.trickButton.enable()
            else:
                self.trickButton.disable()
            
            # Check for trick button
            if self.trickButton.handleEvent(event):
                self.enterTrick(oPlayer)          

    def draw(self):
        """Display cards to screen"""
        # GUI components
        self.swapButton.draw()
        self.trickButton.draw()
        self.drawCardButton.draw()

        # Game elements
        if self.trumpCard:
            self.trumpCard.draw()
        
        if self.trickList: 
            for cardAndOwner in self.trickList:
                cardAndOwner['oCard'].draw()

        for player in self.playerList:
            player.draw()
        self.oDeck.draw()

        # for ghostCard in self.ghostHandList:
            # ghostCard.draw()