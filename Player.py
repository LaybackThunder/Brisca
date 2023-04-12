from Hand import *

class Player():

    def __init__(self, window):
        self.window = window
        self.turnPlayer = False
        self.playerId = 0 # testing
        self.potList = []
        self.oHand = Hand(window)

    def getTurnPlayer(self):
        print(f"Turn player's iD is {self.turnPlayerId}.") # testing
        return self.turnPlayer

    def setTurnPlayerTrue(self):
        if self.turnPlayer:
            print('Player is already turnPlayer (True)!')
        else:
            self.turnPlayer = True
    
    def setTurnPlayerFalse(self):
        if self.turnPlayer == False:
            print('Player is already NOT turnPlayer (False)!')
        else:
            self.turnPlayer = False 

    def setPotList(self, cardsAndOwners):
        """Retrive oCard from trickList and add them to potList."""
        # {'oPlayer': oPlayer, 'oCard': oTrickCard}
        for cardAndOwner in cardsAndOwners:
            oCard = cardAndOwner.pop('oCard')
            print(oCard.getName())
            self.potList.append(oCard)
    
    def getPotList(self):
        return self.potList

    # Polymorphism section

    def disableAllHandCards(self):
        self.oHand.disableAllHandCards()
    
    def enableAllHandCards(self):
        self.oHand.enableAllHandCards()

    def getHandEnableAllCardsBool(self):
        self.oHand.getHandEnableAllCardsBool()
        
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
        cardList = self.oHand.getCardsOnhand()
        return cardList

    def getSelectedObjCard(self):
        """This method tells us which card did the player select."""
        selectedCard = self.oHand.getSelectedObjCard()
        return selectedCard

    def drawCard(self, oCard=None):
        """
        Adds card to player's hand.
        If none; return no card error.
        """
        self.oHand.drawCard(oCard)

    def handleEvent(self, event):
        """Returns a bool if any card on hand was clicked."""
        oCardClicked = self.oHand.handleEvent(event)
        return oCardClicked
    
    def draw(self):
        """Display hand on screen."""
        self.oHand.draw()