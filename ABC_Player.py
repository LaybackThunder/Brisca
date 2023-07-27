from abc import ABC, abstractmethod

# Card is now an abstract base class
class ABC_Player(ABC):

    def __init__(self, window, turnplayer, isPlayerHuman, oHand):
        self.window = window
        # Add playerId in the future to identify host and players.
        self.turnPlayer = turnplayer
        self.potList = []
        self.isPlayerHuman = isPlayerHuman # Bool, true = Yes, false = no
        self.oHand = oHand

    def isObjHumanOrRobot(self):
        """Returns true for human or false for robot."""
        return self.isPlayerHuman

    def getTurnPlayer(self):
        """Return player ID"""
        #print(f"Turn player's iD is {self.turnPlayerId}.") # testing
        return self.turnPlayer

    def setTurnPlayerTrue(self):
        if self.turnPlayer:
            pass
        else:
            self.turnPlayer = True
    
    def setTurnPlayerFalse(self):
        if self.turnPlayer == False:
            pass
        else:
            self.turnPlayer = False 

    def setPotList(self, oCards): # Does not print
        """Retrive oCard from trickList and add them to the player's potList."""

        while oCards:
            oCard = oCards.pop(0)
            print(oCard.getName())
            self.potList.append(oCard)
    
    def getPotList(self):
        return self.potList

    # Polymorphism section

    def disableAllCardsOnHand(self):
        self.oHand.disableAllCardsOnHand()
    
    def enableAllCardsOnHand(self):
        self.oHand.enableAllCardsOnHand()
        
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
        cardList = self.oHand.getCardsOnHand()
        return cardList

    def getSelectedCardfromHand(self):
        """This method tells us which card did the player select."""
        selectedCard = self.oHand.getSelectedCardfromHand()
        return selectedCard
    
    def getCardClick(self):
        """Returns a bool of card's click status."""
        oCardClick = self.oHand.getCardClick()
        return oCardClick

    def _popCardFromHand(self):
        """
        This method retrives a card from the hand and returns the selected.
        """
        oCard = self.oHand._popCardFromHand()
        return oCard

    def _trumpSwap(self, oCard):
        """Action to swap the trump card for a 7 or 2 hand card."""
        self.oHand._trumpSwap(oCard)

    def drawCard(self, oCard):
        """Adds card to player's hand. If none; return no card error."""
        self.oHand._drawCard(oCard)

    def draw(self):
        """Display hand on screen."""
        self.oHand.draw()