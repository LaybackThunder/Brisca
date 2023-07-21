from ABC_Hand import *

class HumanHand(ABC_Hand):
    """This class simulates a human player's hand."""

    HAND_Y_LOC = 460

    def __init__(self, window):
        """Initialize hand attributes."""
        self.HAND_LOCATION_DICT = {
                                # g.e. [HAND_SLOTX is location iD key, (CARD LOCATION ON SCREEN) is value]
                                "HAND_SLOT0": (300, HumanHand.HAND_Y_LOC), # slot 0 is left side of hand. 
                                "HAND_SLOT1": (500, HumanHand.HAND_Y_LOC), # slot 1 is middle side of hand.
                                "HAND_SLOT2": (700, HumanHand.HAND_Y_LOC)  # slot 2 is right side of hand.
                                }
        super().__init__(window, self.HAND_LOCATION_DICT)

    def _drawCard(self, oCard):
        """Adds card to player's hand. If none; return no card error."""
        
        oCard.reveal() # Reveal card to Player
        self.setCardId(oCard) # Give card an id; by defult oCard has an iD of 0
        self.addCardToHand(oCard) # Player has a card in hand via a list
        self.setHandCorrdinatesForDisplay(oCard) # Give card display coordinates based of card iD          

    def setHandCorrdinatesForDisplay(self, oCard):
        # Give card display coordinates for the hand based of card iD
        # print(f"The index of oCard is {oCard.getCardId()}")

        self.cardList[oCard.getCardId()].setLoc(
                    self.HAND_LOCATION_DICT["HAND_SLOT" + str(oCard.getCardId())]
                    )
        
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

                elif self.cardList:
                    # The initial way to setting the 2nd card of the game with an ID
                    for i in range(len(self.cardList)): # If for loop is empty it won't loop
                        iDCounter += 1
                        oCard.setCardId(iDCounter)
            except:
                print(f"Check your lists and local variables for errors: \n\
                        iDCounter (Int): {iDCounter}\n\
                        iDcardSlots (List): {self.iDCardSlots}\n\
                        cardList (List): {self.cardList}\n")

    def handleEvent(self, event):
        """ Returns a bool if any card on hand was clicked.
        Disable all cards not selected. 
        Enables all cards once selected card is deselcted.
        """
       
        # Check if cards can be clicked
        if self.clickableHand:
            for oCard in self.cardList:
                if oCard.handleEvent(event): # Has card been clicked now?
                            self.oCard = oCard # Remember Ocard
                            self.oCardClicked = self.oCard.getOcardClicked() # Assign click (True)
                            self.clickableHand = False
                            return self.oCardClicked # Return value and exit method
        elif self.oCard == None: # oCard is none at the begining of the code's run.
             pass
        else:
            if self.oCard.handleEvent(event):
                        self.oCardClicked = self.oCard.getOcardClicked()
                        self.clickableHand = True
                        self.oCard = None

        # Return value and exit method
        return self.oCardClicked     
    
    def draw(self):
        """Display cards on screen."""
        for oCard in self.cardList:
            oCard.draw()