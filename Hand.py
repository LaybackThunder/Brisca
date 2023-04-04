

class Hand():
    # Index 0 is left side of hand. 
    # Index 1 is middle side of hand.
    # Index 2 is right side of hand.
    HAND_Y_LOC = 650
    HAND_LOCATION_DICT = {
         # "HAND_SLOT_EXAMPLE":[card identifier in the hand, (CARD LOCATION ON SCREEN)]
         "HAND_SLOT0": (300, HAND_Y_LOC), 
         "HAND_SLOT1": (500, HAND_Y_LOC), 
         "HAND_SLOT2": (700, HAND_Y_LOC)
         }

    def __init__(self, window):
        self.window = window
        self.cardList = [] # Holds all the cards on hand
        self.iDCardSlots = [] # Remembers where cards are on hand
        self.oCard = None
        self.enableAllCards = True
        self.oCardClicked = False

    def drawCard(self, oCard):
        """
        Adds card to player's hand.
        If none; return no card error.
        """
        if oCard == None:
            print("No card was added.")
        else:
            HAND_LOCATION_DICT = Hand.HAND_LOCATION_DICT
            # Reveal card to Player
            oCard.reveal() 

            # Set ID to car using ID card slots
            iDCounter = 0
            if self.iDCardSlots:
                    iDCounter = self.iDCardSlots.pop(0)
                    oCard.setCardId(iDCounter)    
            else:
                # The initial way to setting cards up with an ID
                for i in range(len(self.cardList)): # If for loop is empty it won't loop
                    iDCounter += 1
                    oCard.setCardId(iDCounter) 
            
            # Add card to hand
            # By defult oCard has an iD of 0
            self.cardList.insert(oCard.getCardId(), oCard)

            # Give card display coordinates based of card iD
            self.cardList[oCard.getCardId()].setLoc(
                     HAND_LOCATION_DICT["HAND_SLOT" + str(oCard.getCardId())]
                     )

    def playCardFromHand(self, oCard):
        """
        Removes card from player's hand.
        If none; return no card error.
        else; return card.
        """
        if oCard == None:
            print("No card were removed.")
        else:
            oCardIndex = self.cardList.index(oCard)
            return self.cardList.pop(oCardIndex)

    def getLengthCardsOnHand(self):
        """Returns the total number of cards on hand."""
        return len(self.cardList)

    def getCardsOnhand(self):
        """Returns cards on hand."""
        return self.cardList

    def enterTrick(self):
        """Place card in the middle of the board."""
        # We pop card from hand, return card
        oCardIndex = self.cardList.index(self.oCard)
        oTrickCard = self.cardList.pop(oCardIndex)
        self.enableAllCards = True
        self.oCardClicked = False # Not sure if needed
        self.oCard = None # Not sure if needed

        # Snapshot the slot the card was in
        self._retriveId(oTrickCard)
        
        return oTrickCard

    def _retriveId(self, oCard):
        """Obtains the oTrickCard's iD and assigns it to self.iDCardSlots"""
        self.iDCardSlots.append(oCard.getCardId())
        self.iDCardSlots.sort() 

    # Polymorphism section 
    def handleEvent(self, event):
        """
        Returns a bool if any card on hand was clicked.
        Disable all cards not selected. 
        Enables all cards once selected card is deselcted.
        """
        # Check if cards can be clicked
        if self.enableAllCards:
            for oCard in self.cardList:
                if oCard.handleEvent(event): # Has card been clicked now?
                            self.oCard = oCard # Remember Ocard
                            self.oCardClicked = self.oCard.getOcardClicked() # Assign click (True)
                            self.enableAllCards = False
                            return self.oCardClicked # Return value and exit method

        # Check is the clicked card has be declicked         
        else:
            if self.oCard.handleEvent(event):
                        self.oCardClicked = self.oCard.getOcardClicked()
                        #print(self.oCardClicked)
                        self.enableAllCards = True
                        self.oCard = None

        # Return value and exit method
        return self.oCardClicked     
    
    def draw(self):
        """Display cards on screen."""
        for oCard in self.cardList:
            oCard.draw()

    