#def popCardFromHand(self):
"""
    def popCardFromHand(self):
        # This method retrives a card from the hand and returns the value.
        if self.oCard is None:
              print("Object is None Type.")
        else:
            # Identify card's index & us it to retrive card bject from the hand.
            oCardIndex = self.cardList.index(self.oCard)
            selectedCard = self.cardList.pop(oCardIndex)

            # Card is not selected any more.
            selectedCard.setCardClickedToFalse()

            # Other cards on hand can be clicked.
            self.enableAllCards = True

            # retrives selected card's iD for iD reassigment when drawing a card.
            self._retriveId(selectedCard)

            # Card left the hand
            return selectedCard 
"""

a = 1
b = a
a = 2

print(b)
print(a)