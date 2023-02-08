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
    
    def getHand(self):
        return self.hand
    
    def setPot(self, oCard):
        self.pot.append(oCard)

    def getPot(self):
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
    for oCard in range(3): 
        oCard = oPlayer.drawCard(oDeck)
        oPlayer.setHand(oCard)

        oCard = oPlayer2.drawCard(oDeck)
        oPlayer2.setHand(oCard)

    # Obtain Hand info 
    ply1HandList = oPlayer.getHand()
    ply2HandList = oPlayer2.getHand()

    # Pront to verify players have cards on hand
    print("\nPlayer's hands\n")
    print("Player 1:")
    for oCard in ply1HandList:
        print(oCard.getName())

    print("\n-------")

    print("\nPlayer 2:")
    for oCard in ply2HandList:
        print(oCard.getName())
    print()

    # Compare player cards
    for oCard in range(3): # Trick will loop 3 times

        # Compares player's hands; the higest value card wins
        if oPlayer.hand[0].getTrickValue() > oPlayer2.hand[0].getTrickValue():
            # Player 1 gets to add cards in pot
            potCards = [oPlayer.hand.pop(0), oPlayer2.hand.pop(0)]
            for oCard in potCards: # one item or the whole list?
                oPlayer.setPot(oCard)

        else:
            # Player 2 gets to add cards in pot
            potCards = [oPlayer.hand.pop(0), oPlayer2.hand.pop(0)]
            for oCard in potCards: # one item or the whole list?
                oPlayer2.setPot(oCard)
    
    ply1Pot = oPlayer.getPot()
    ply2Pot = oPlayer2.getPot()

    print("\nPlayer's pots\n")
    print("Player 1:")
    for oCard in ply1Pot:
        print(oCard.getName())

    print("\n-------")

    print("\nPlayer 2:")
    for oCard in ply2Pot:
        print(oCard.getName())
    print()



"""Error Notes
1) Issue: Could not call setHand method, error would say missing 'self' when calling drawCard().
1) Resolve: Added deck as a parameter to drawCard() 

"""

"""Errors to fix
1) Make sure pot distribution is based on who has the highest value card.
    Make sure that if trick ends in a tie to disregard the cards into a discard pile list. 
"""