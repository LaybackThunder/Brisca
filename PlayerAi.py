from ABC_Player import *
from AiHand import AIHand # There was an error because after import I had "Hand"

class PlayerAi(ABC_Player):
    """Class simulates a human player."""

    def __init__(self, window, isTurnPlayer, isPlayerHuman):
        self.oHand = AIHand(window)
        super().__init__(window, isTurnPlayer, isPlayerHuman, self.oHand)