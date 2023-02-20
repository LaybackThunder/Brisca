from Deck import *
from Card import *

class Player():

    BEGINNING_HAND = 3

    def __init__(self, iD=None):
        self.hand = []
        self.playerHandPosX = []
        self.pot = []
        self.playerId = iD # Identify if its player 1(int=0) or 2(int=1)
        self.turnPlayer = False
    
    def drawCard(self, oDeck):
        """This gets a card from the top of the deck."""
        oCard = oDeck.getCard()
        return oCard

    def removeCardFromHand(self, index):    
        """Remove card from hand."""
        discard = self.hand.pop(index)
        return discard

    def setHand(self, oCard):
        """Player puts card in their hand."""
        self.hand.append(oCard)
    
    def getHand(self):
        """Returns a list format of the hand."""
        return self.hand
    
    def setHandPosX(self, PosX):
        """Player puts card in their hand."""
        self.playerHandPosX.append(PosX)
    
    def getHandPosX(self):
        """Returns a list format of the hand."""
        return self.playerHandPosX

    def setPot(self, oCard):
        """Add the spoils of battle in your pot pile."""
        self.pot.append(oCard)

    def getPot(self):
        """Returns a list format of the pot."""
        return self.pot
    
    def removeCardFromPot(self, oCard=-1):
        """Removes the last card in the player's pot by defult."""
        discard = self.pot.pop(oCard)
        return discard

    def setPlayerId(self, iD):
        self.playerId = iD

    def getPlayerId(self):
        return self.playerId

    def setTurnPlayer(self, bool):
        """Sets player's right to be turnPlayer or not."""
        self.turnPlayer = bool
    
    def getTurnPlayer(self):
        """Returns True or False if current player is turn player."""

# Test player
if __name__ == "__main__":

    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oDeck = Deck(window) # Instatiate Deck
    # Instantiate Players
    oPlayer = Player()
    oPlayer2 = Player()

    # Each player draws one card before the other player continues to draw
    for i in range(3): 
        oCard = oPlayer.drawCard(oDeck)
        oPlayer.setHand(oCard)

        oCard = oPlayer2.drawCard(oDeck)
        oPlayer2.setHand(oCard)

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
            potCards = [oPlayer.removeCard(0), oPlayer2.removeCard(0)]
            # Add cards into pot
            for oCard in potCards.copy():
                oCard = potCards.pop(0)
                oPlayer.setPot(oCard)

        elif oPlayer.hand[0].getTrickValue() < oPlayer2.hand[0].getTrickValue():
            print("-------Player 2 wins")

            # Remove the 1st card from each player's hand
            potCards = [oPlayer.removeCard(0), oPlayer2.removeCard(0)]
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