from Deck import *

class Player():

    BEGINNING_HAND = 3

    def __init__(self):
        self.hand = []
    
    def drawCard(self, oDeck): # Should I call this getCard so that it matches the deck's method name?
        oCard = oDeck.getCard()
        return oCard

    def setHand(self, oCard):
        """Player puts card in their hand."""
        self.hand.append(oCard)
    
    def getHand(self):
        return self.hand


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
    handList = oPlayer.getHand()
    handList2 = oPlayer2.getHand()

    # Pront to verify players have cards on hand
    print("\nPlayer's hands\n")
    print("Player 1:")
    for oCard in handList:
        print(oCard.getName())

    print("\n-------")

    print("\nPlayer 2:")
    for oCard in handList2:
        print(oCard.getName())
    print()



"""Error Notes
1) Issue: Could not call setHand method, error would say missing 'self' when calling drawCard().
1) Resolve: Added deck as a parameter to drawCard() 

"""