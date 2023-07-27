from ABC_Hand import *
from BriscaCard import *


"""Currently:
Figure out how to modify the handleEvent().   
"""

class AIHand(ABC_Hand):

    # Class variables
    HAND_Y_LOC = 5

    def __init__(self, window):
        """Initialize hand attributes."""
        self.ghostHandList = []
        self.HAND_LOCATION_DICT = {
                                # g.e. [HAND_SLOTX is location iD key, (CARD LOCATION ON SCREEN) is value]
                                "HAND_SLOT0": (300, AIHand.HAND_Y_LOC), # slot 0 is left side of hand. 
                                "HAND_SLOT1": (500, AIHand.HAND_Y_LOC), # slot 1 is middle side of hand.
                                "HAND_SLOT2": (700, AIHand.HAND_Y_LOC)  # slot 2 is right side of hand.
                                }
        super().__init__(window, self.HAND_LOCATION_DICT)
    
    def _drawCard(self, oCard):
        """Draw a card from the deck and place it in the hand."""

        self.addCardToHand(oCard) # Player has the real oCard in hand via a list to play in a trick
        oGhostCard = BriscaCard(self.window) # Create a generic card as a oGhostCard
        self.setCardId(oGhostCard) # Give oGhostCard an id; by defult oGhostCard has an iD of 0
        self.addGhostCardToHand(oGhostCard) # Add ghost card to hand to be displayed by the draw method
        self.setHandCorrdinatesForDisplay(oGhostCard) # Give oGhostCard display coordinates based of card iD 

    def setCardId(self, oCard):
            """
            Set a new id to oCard which maps a location for it to land in the hand.  
            """
            iDCounter = 0
            try:
                # Initially both conditions will be false;
                # no cards on hand = no ids currently identified
                if self.iDCardSlots:
                        iDCounter = self.iDCardSlots.pop(0)
                        oCard.setCardId(iDCounter)    

                elif self.cardList and self.ghostHandList:
                    # The initial way to setting the 2nd card of the game with an ID
                    for i in range(len(self.ghostHandList)): # If for loop is empty it won't loop
                        iDCounter += 1
                        oCard.setCardId(iDCounter)
            except:
                print(f"Check your lists and local variables for errors: \n\
                        iDCounter (Int): {iDCounter}\n\
                        iDcardSlots (List): {self.iDCardSlots}\n\
                        cardList (List): {self.cardList}\n")

    def addGhostCardToHand(self, oGhostCard):
        self.ghostHandList.insert(oGhostCard.getCardId(), oGhostCard)

    def setHandCorrdinatesForDisplay(self, oGhostCard):
        # Give card display coordinates for the hand based of card iD
        # print(f"The index of oCard is {oCard.getCardId()}")

        self.ghostHandList[oGhostCard.getCardId()].setLoc(
                    self.HAND_LOCATION_DICT["HAND_SLOT" + str(oGhostCard.getCardId())]
                    )

    def draw(self):
        """Display cards on screen.
        # NOTE: Will the ghost card appears as the trick 
        card or will it be the card in the handList?
        """
        for oCard in self.ghostHandList:
            oCard.draw() # Draw back of card
            
    # Experimenting with method
    def _popCardFromHand(self):
        """
        This method retrives a card from the hand and returns the selected card 
        as the new trump card or for selcted card to enter a trick.
        """

        # ----------------------- working --------------------------------------------

        print(self.ghostHandList) # --------- THIS shows ghost hand is empty
        selectedghostCard = self.ghostHandList.pop(0) # ---- AI pops after no more cards on hand. ISSUE!
        
        # ----------------------- working --------------------------------------------





        self.retriveCardId(selectedghostCard) # Obtain selected card's iD; Id is reassiged to a drawn or swaped card.
        selectedCard = self.cardList.pop(0) # Use index to pop oCard from the hand
        return selectedCard # selectedCard left the hand; (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ peace the fuck out!
