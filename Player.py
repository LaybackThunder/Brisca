from Deck import *
from Card import *

class Player():

    def __init__(self, window, iD=None):
        self.hand = [] # oCards go here
        self.playerHandPosX = None # oCards location are here
        self.pot = []
        self.potScore = 0
        self.turnPlayer = False
        self.window = window # Window is for card placement in player's hand 
    
    def selectACard(self, event):
        """Returns a bool and the card index"""
        for index in range(len(self.hand.copy())): # Index of Obj inside hand
                isSelected = {
                    'bool': self.hand[index].selectedCard(event) # Check if object card has bee selected
                    } 
                if isSelected['bool']:
                    isSelected.update({'cardIndex': index})
                    return isSelected

    def cardSelected(self, cardIndex):
        """Retunrs oCard after being removed from the player's hand."""
        oCard = self.removeCardFromHand(cardIndex)
        return oCard

    def drawCard(self, oDeck):
        """This gets a card from the top of the deck and puts it in player's hand."""
        oCard = oDeck.getCard() # Draw
        oCard.reveal() # Show
        self.setHand(oCard) # In player's hand

    def removeCardFromHand(self, cardIndex):    
        """Remove card from hand and returns."""
        remove = self.hand.pop(cardIndex)
        return remove

    def removeCardFromPot(self, oCard=-1):
        """Removes the last card in the player's pot by defult."""
        discard = self.pot.pop(oCard)
        return discard

    def showHand(self):
        for card in self.hand:
            card.reveal()

    def setHand(self, oCard):
        """Player puts card in their hand."""
        self.hand.append(oCard)
    
    def setCardLoc(self, cardIndex, loc):
        """Set the cards image location to player's hand."""
        oCard = self.hand[cardIndex]
        oCard.setLoc(loc)

    def setPot(self, oCard):
        """Add the spoils of battle in your pot pile."""
        self.pot.append(oCard)

    def setPotScore(self, points=0, gameReset=False):
        if gameReset:
            self.potScore = 0
        else:
            self.potScore += points

    def setTurnPlayer(self, bool):
        """Sets player's right to be turnPlayer or not."""
        self.turnPlayer = bool

    def getHand(self):
        """Returns a list format of the hand."""
        return self.hand

    def getPot(self):
        """Returns a list format of the pot."""
        return self.pot
        
    def getPotPoints(self):
        return self.potScore

    def getTurnPlayer(self):
        """Returns True or False if current player is turn player."""
        return self.turnPlayer

# Test player
if __name__ == "__main__":

    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oDeck = Deck(window) # Instatiate Deck
    # Instantiate Players
    oPlayer = Player(window)
    oPlayer2 = Player(window)

    # Each player draws one card before the other player continues to draw
    for i in range(3): 
        oCard = oPlayer.drawCard(oDeck)

        oCard = oPlayer2.drawCard(oDeck)

    # Obtain Hand info 
    ply1HandList = oPlayer.getHand()
    ply2HandList = oPlayer2.getHand()

    # Print to verify players have cards on hand
    print("\nPlayer's hands\n")

    print("Player 1:")
    for oCard in ply1HandList:
        print(oCard.getName())

    print("\n-------\n")

    print("Player 2:")
    for oCard in ply2HandList:
        print(oCard.getName())

    print("\n|||||||||||||||||||||||||||||||||||\n")

    # Compare player cards --------------------------
    for trick in range(3): # Trick will loop 3 times

        # Compares player's hands; the higest value card wins
        if oPlayer.hand[0].getTrickValue() > oPlayer2.hand[0].getTrickValue():
            print("-------Player 1 wins")

            # Remove the 1st card from each player's hand
            potCards = [oPlayer.removeCardFromHand(0), oPlayer2.removeCardFromHand(0)]
            # Add cards into pot
            for oCard in potCards.copy():
                oCard = potCards.pop(0)
                oPlayer.setPot(oCard)

        elif oPlayer.hand[0].getTrickValue() < oPlayer2.hand[0].getTrickValue():
            print("-------Player 2 wins")

            # Remove the 1st card from each player's hand
            potCards = [oPlayer.removeCardFromHand(0), oPlayer2.removeCardFromHand(0)]
            # Add cards into pot
            for oCard in potCards.copy():
                oCard = potCards.pop(0)
                oPlayer2.setPot(oCard)
            
    ply1Pot = oPlayer.getPot()
    ply2Pot = oPlayer2.getPot()

    print("\nPlayer's pots\n")

    print("Player 1:")
    for oCard in ply1Pot:
        print(oCard.getName())

    print("\n-------\n")

    print("Player 2:")
    for oCard in ply2Pot:
        print(oCard.getName())
    print()



"""Error Notes
1) Issue: Could not call setHand method, error would say missing 'self' when calling drawCard().
1) Resolution: Added deck as a parameter to drawCard() 

2) Issue: Make sure pot distribution is based on who has the highest value card.
2) Resolution: potCards list iteration was not working until I was using a copy of itself.

"""