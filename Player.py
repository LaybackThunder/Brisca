from Deck import *

class Player():

    BEGINNING_HAND = 3

    def __init__(self):
        self.hand = []
        self.pot = []
    
    def drawCard(self, oDeck): # Should I call this getCard so that it matches the deck's method name?
        oCard = oDeck.getCard()
        return oCard

    def setHand(self, oCard):
        """Player puts card in their hand."""
        self.hand.append(oCard)
    
    def removeCard(self, index):
        """Removes card from hand"""
        card = self.hand.pop(index)
        return card
    
    def showHand(self):
        """Returns a list format of the hand."""
        return self.hand
    
    def setPot(self, oCard):
        """Add the spoils of battle in your pot pile."""
        self.pot.append(oCard)

    def getPot(self):
        """Returns a list format of the pot."""
        return self.pot



# Test player
if __name__ == "__main__":

    WINDOW_WIDTH = 100
    WINDOW_HEIGHT = 100

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
    ply1HandList = oPlayer.showHand()
    ply2HandList = oPlayer2.showHand()

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
    for i in range(3): # Trick will loop 3 times

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