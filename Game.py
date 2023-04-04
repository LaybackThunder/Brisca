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

    # Doesn't work yet
    def battleStep(self, cardsAndOwners):
        """
        Calculates which oTrickCard wins the battle step.
        Sets a turnPlayer by comparing the highest value card.
        Arrange player list; winner is first item on playerList.
        Returns True or False for tie.
        """
        # playersAndCards is a list nesing a dictionary with the player's iD and corresponding cards
        # E.g. playersAndCards = [{'player: oPlayer, 'card': oCard}]

        player1CardValue = cardsAndOwners[0]['card'].getTrickValue()
        player2CardValue = cardsAndOwners[1]['card'].getTrickValue()
        cardsAndOwners[0]['card'].reveal()
        cardsAndOwners[1]['card'].reveal()

        if player1CardValue > player2CardValue:
            print("-------You WIN!")
            cardsAndOwners[0]['player'].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
            self.playerList = [cardsAndOwners[0]['player'], cardsAndOwners[1]['player']] # Player arrangement decides who draws first
            tie = False
            
        elif player1CardValue < player2CardValue:
            print("-------You LOSE!")
            cardsAndOwners[1]['player'].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
            self.playerList = [cardsAndOwners[1]['player'], cardsAndOwners[0]['player']] # Player arrangement decides who draws first
            tie = False

        else: # If players end in a tie: cards return to deck
            print("Tie")
            tie = True

        return tie # Return the value of Tie

    # Polymorphism section 
    def enterTrick(self, oPlayer):
        """Place card in the middle of the board."""
        oTrickCard = oPlayer.enterTrick()
        trickIndex = len(self.trickList)

        """LEFT OFF!"""
        cardAndOwner = {'oCard': oTrickCard, 'oPlayer': oPlayer}

        self.trickList.append(cardAndOwner)
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))

        # Battle step of the game
        if len(self.trickList) == 2:
            print("Battle!")

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
                    # Should selected card be returned?
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
        
        # HOW WILL I DRAW THE CARDS IN THE TRICK DICT?
        if self.trickList: 
            for cardAndOwner in self.trickList:
                cardAndOwner['oCard'].draw()

        for player in self.playerList:
            player.draw()
        self.oDeck.draw()

        # for ghostCard in self.ghostHandList:
            # ghostCard.draw()