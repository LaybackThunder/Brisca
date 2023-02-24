from Deck import *
from Card import *

class Player():

    BUFFER_BETWEEN_HAND_CARDS = 150 # Space between cards in player's hand
    GHOST_HAND_CARDS_TOP = 400 # Y coordinate; where ghost cards will go; top of screen
    PLAYER_HAND_CARDS_BOTTOM = 100 # Y coordinate; where player hand will go
    CARDS_LEFT = 350 # X coordinate; 1st card in the hand; buffer will be added 
    DISPLAY_STARTING_HANDS = 3
    MAX_HAND = 3

    def __init__(self, window, iD=None):
        self.hand = []
        self.pot = []
        self.turnPlayer = False
        self.window = window # Window is for card placement in player's hand

        # Calculate Player's card locations within the player's hand
        self.playerHandPosX = []
        leftToRight = Player.CARDS_LEFT # Starting card to the left of the player's hand
        # Calculate the x positions of all cards, once 
        for i in range(Player.DISPLAY_STARTING_HANDS): # 3 cards
            # Add the coresponding space for the oCard to inhabit
            self.playerHandPosX.append(leftToRight)
            # Space between cards in the player's hand
            leftToRight += Player.BUFFER_BETWEEN_HAND_CARDS 
    
    def drawCard(self, oDeck):
        """This gets a card from the top of the deck."""
        oCard = oDeck.getCard()
        return oCard

    def removeCardFromHand(self, cardIndex):    
        """Remove card from hand and returns."""
        remove = self.hand.pop(cardIndex)
        return remove

    def showHand(self):
        for card in self.hand:
            card.reveal()

    def setHand(self, oCard):
        """Player puts card in their hand."""
        self.hand.append(oCard)
    
    def getHand(self):
        """Returns a list format of the hand."""
        return self.hand
    
    def getHandPosX(self, oCardIndex):
        """Returns a list format of the hand."""
        return self.playerHandPosX[oCardIndex]

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