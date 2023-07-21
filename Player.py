from ABC_Player import *
from HumanHand import *

class Player(ABC_Player):
    """Class simulates a human player."""

    def __init__(self, window, isTurnPlayer, isPlayerHuman):
        self.oHand = HumanHand(window)
        super().__init__(window, isTurnPlayer, isPlayerHuman, self.oHand)
    
    def handleEvent(self, event):
        """Returns a bool if any card on hand was clicked."""
        oCardClicked = self.oHand.handleEvent(event)
        return oCardClicked
    
