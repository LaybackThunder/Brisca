from ABC_Hand import *


"""Currently:
Figure out how to modify the handleEvent().   
"""

class AIHand(ABC_Hand):

    # Class variables
    HAND_Y_LOC = 200

    def __init__(self, window):
        """Initialize hand attributes."""
        self.HAND_LOCATION_DICT = {
                                # g.e. [HAND_SLOTX is location iD key, (CARD LOCATION ON SCREEN) is value]
                                "HAND_SLOT0": (300, AIHand.HAND_Y_LOC), # slot 0 is left side of hand. 
                                "HAND_SLOT1": (500, AIHand.HAND_Y_LOC), # slot 1 is middle side of hand.
                                "HAND_SLOT2": (700, AIHand.HAND_Y_LOC)  # slot 2 is right side of hand.
                                }
        super().__init__(window, self.HAND_LOCATION_DICT)
    

    def automateCardClick(self):
        """Ai selects the first card in the list from left to right."""
        pass

    def handleEvent(self, event):
        print("Robot Hand event")
        pass  