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
            
        elif player1CardValue < player2CardValue:
            print("-------You LOSE!")
            player2.setTurnPlayerTrue() # Player2 will have the bool to draw first
            player1.setTurnPlayerFalse()
            self.playerList = [player1] # Player arrangement decides who draws first

        else: # If players end in a tie: cards return to deck
            print("-------TIE/n")
            tie = True

    # Polymorphism section 
    def enterTrick(self, oPlayer) :
        """Place card in the middle of the board and battle."""

        # Retrieve player's card and trickList index
        oTrickCard = oPlayer.enterTrick()
        trickIndex = len(self.trickList)
        # Prep for battle: identify card and owner
        playerAndCard = {'oPlayer': oPlayer, 'oCard': oTrickCard}
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))
        self.trickList.append(playerAndCard)

        # Enter battle phase
        if len(self.trickList) == 2:

            # Compare player's trump cards to the main trump card
            isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == self.trumpCard.getSuit()
            isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == self.trumpCard.getSuit()
            print("Battle!\n")

            # A player has a trump card
            if isPlayer1Trump and isPlayer2Trump: 
                self.battleStep()
            
            # Both players have a trump card 
            elif isPlayer1Trump or isPlayer2Trump:   
                if isPlayer1Trump:
                    print("-------You WIN!\n")
                    self.trickList[0]['oPlayer'].setTurnPlayerTrue() # Player 1 is turn player
                    self.trickList[1]['oPlayer'].setTurnPlayerFalse()
                    self.playerList = [self.trickList[0]['oPlayer']] # Test 
                else:
                    print("-------You LOSE!")
                    self.trickList[1]['oPlayer'].setTurnPlayerTrue() # Player 2 is turn player
                    self.trickList[0]['oPlayer'].setTurnPlayerFalse()
                    self.playerList = [self.trickList[1]['oPlayer']] # Test 
            
            # No one has a trump card, the 1st card on the board leads as trump
            else:
                trumpCard = self.trickList[0]['oCard']
                # Compare player's leading trump cards to the main trump card
                isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == trumpCard.getSuit()
                isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == trumpCard.getSuit()

                if isPlayer1Trump and isPlayer2Trump:
                    self.battleStep()

                else:
                    if isPlayer1Trump:
                        print("-------You WIN!\n")
                        self.trickList[0]['oPlayer'].setTurnPlayerTrue() # Player 1 is turn player
                        self.trickList[1]['oPlayer'].setTurnPlayerFalse()
                        self.playerList = [self.trickList[0]['oPlayer']] # Test 
                    else:
                        print("-------You LOSE!")
                        self.trickList[1]['oPlayer'].setTurnPlayerTrue() # Player 2 is turn player
                        self.trickList[0]['oPlayer'].setTurnPlayerFalse()
                        self.playerList = [self.trickList[1]['oPlayer']] # Test
                    
            # Transfer trickCards to winner's potCards
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
        oCard = self.oDeck.drawCard()
        oPlayer.drawCard(oCard)

    def handleEvent(self, event):
        """Handles pygame events and buttons"""
        for oPlayer in self.playerList:

            # If your hand isn't full you can't battle for now (TEST)
            # Check if player can draw
            if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:
                # But if the player clicks a card, for testing it can battle
                if self.trickList:
                    self.drawCardButton.disable()
                else:
                    self.drawCardButton.enable() 
            else:
                self.drawCardButton.disable()

            # Draw button enabled for testing when game starts
            if self.drawCardButton.handleEvent(event):
                self.drawCard(oPlayer) 

            # Gameplay options after a card is selected
            if oPlayer.handleEvent(event):
                self.trickButton.enable()

                if self.isCardSwappable(oPlayer):
                    self.swapButton.enable()
                else:
                    self.swapButton.disable()

            # Gameplay options after a card is deselected
            else:
                # Battle (trick) ability unavailable
                self.trickButton.disable()
                self.swapButton.disable()
            
            if self.swapButton.handleEvent(event):
                self.cardSwap(oPlayer)
            
            # Check for trick button
            if self.trickButton.handleEvent(event):
                self.enterTrick(oPlayer)
                


    def isCardSwappable(self, oPlayer):
        """
        Function access the player's selected card and compares it with the trump card.
        The method Returns a bool.
        """
        selectedCard = oPlayer.getSelectedCardfromHand()
        if selectedCard is None:
            print("NONE TYPE!")
        else:
            if selectedCard.getSuit() == self.trumpCard.getSuit(): # Same String?
                if selectedCard.getRankValue() == 7 and self.trumpCard.getRankValue() > 7:
                    return True
                elif selectedCard.getRankValue() == 2 and self.trumpCard.getRankValue() <= 7: 
                    return True
                else:
                    return False

    def cardSwap(self, oPlayer):
        """Action to swap the trump card to for a hand card."""
        
        theSwapToHandCard = self.trumpCard # Old trump
        self.trumpCard = oPlayer.popCardFromHand() # New Trump
        # print(type(self.trumpCard))
        # New Trump attributres
        self.trumpCard.setLoc(Game.TRUMP_LOC)
        self.trumpCard.setRotation(-90)

        # New card on hand
        oPlayer.cardSwap(theSwapToHandCard)

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