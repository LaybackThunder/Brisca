from ABC_Hand import *

class HumanHand(ABC_Hand):
    """This class simulates a human player's hand."""

    HAND_Y_LOC = 450

    def __init__(self, window):
        """Initialize hand attributes."""
        self.HAND_LOCATION_DICT = {
                                # g.e. [HAND_SLOTX is location iD key, (CARD LOCATION ON SCREEN) is value]
                                "HAND_SLOT0": (300, HumanHand.HAND_Y_LOC), # slot 0 is left side of hand. 
                                "HAND_SLOT1": (500, HumanHand.HAND_Y_LOC), # slot 1 is middle side of hand.
                                "HAND_SLOT2": (700, HumanHand.HAND_Y_LOC)  # slot 2 is right side of hand.
                                }
        super().__init__(window, self.HAND_LOCATION_DICT)

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