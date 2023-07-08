

class Hand():

    # slot 0 is left side of hand. 
    # slot 1 is middle side of hand.
    # slot 2 is right side of hand.
    HAND_Y_LOC = 650
    HAND_LOCATION_DICT = {
         # HAND_SLOT_EXAMPLE:[card identifier in the hand, (CARD LOCATION ON SCREEN)]
         "HAND_SLOT0": (300, HAND_Y_LOC), 
         "HAND_SLOT1": (500, HAND_Y_LOC), 
         "HAND_SLOT2": (700, HAND_Y_LOC)
         }

    def __init__(self, window):
        self.window = window
        self.cardList = [] # Holds all the cards on hand
        self.iDCardSlots = [] # Remembers where cards are on hand; holds location ids
        self.oCard = None
        self.clickableHand = True
        self.oCardClicked = False

    def disableAllCardsOnHand(self):
        """Disables all cards on hand to avoid being click able.""" 
         
        self.clickableHand = False
    
    def enableAllCardsOnHand(self):
        """Enables all cards on hand to be click able.""" 

        self.clickableHand = True

    def getCardClick(self):
        """Returns a bool of card's click status."""
        return self.oCardClicked

    def setCardId(self, oCard):
        """
        Set card's id and add it to self.iDCardSlots; 
        holds location of cards id.  
        """
        
        iDCounter = 0
        try:
            # Initially both conditions will be false;

            # no cards on hand = no ids currently identified
            if self.iDCardSlots:
                    iDCounter = self.iDCardSlots.pop(0)
                    oCard.setCardId(iDCounter)    

            elif self.cardList:
                # The initial way to setting the first card of the game with an ID
                for i in range(len(self.cardList)): # If for loop is empty it won't loop
                    iDCounter += 1
                    oCard.setCardId(iDCounter)
        except:
             print(f"Check your lists and local variables for errors: \n\
                    iDCounter (Int): {iDCounter}\n\
                    iDcardSlots (List): {self.iDCardSlots}\n\
                    cardList (List): {self.cardList}\n")
             
    def addCardToHand(self, oCard):
         self.cardList.insert(oCard.getCardId(), oCard)

    def setHandCorrdinatesForDisplay(self, oCard):
        # Give card display coordinates based of card iD
        self.cardList[oCard.getCardId()].setLoc(
                    Hand.HAND_LOCATION_DICT["HAND_SLOT" + str(oCard.getCardId())]
                    )

    def _drawCard(self, oCard):
        """Adds card to player's hand. If none; return no card error."""
        
        oCard.reveal() # Reveal card to Player
        self.setCardId(oCard) # Give card an id; by defult oCard has an iD of 0
        self.addCardToHand(oCard) # Player has a card in hand via a list
        self.setHandCorrdinatesForDisplay(oCard) # Give card display coordinates based of card iD

    def getLengthCardsOnHand(self):
        """Returns the total number of cards on hand."""
        return len(self.cardList)

    def getCardsOnhand(self):
        """Returns cards on hand."""
        return self.cardList
    
    def getSelectedCardfromHand(self):
        """This method tells us which card did the player select."""
        try:
            selectedCard = self.oCard
            return selectedCard
        except:
            if self.oCard is None:
                print("Object is None Type.")
            else:
                 print("Unknown error: Check logic and/or syntax.")





# ----------------CURRENTLY WORKIN ON!-----------------------------

# currently refactoring.


# REVIEW popCardFromHand one more time!!!!!!!!!!!!!!!!!!!!

    def popCardFromHand(self):
        """This method retrives a card from the hand and returns the card."""
        try: 
            # Identify card's index.
            oCardIndex = self.cardList.index(self.oCard)
            # Use index to pop card object from the hand
            selectedCard = self.cardList.pop(oCardIndex)

            # Enables other cards on hand to be selected
            self.enableAllCardsOnHand()
            # Selected card is set, not clickled, a.k.a False
            self.setCardClickedToFalse(selectedCard)
            # retrives selected card's iD. 
            # Id is reassiged to a drawn or swaped card.
            self._retriveId(selectedCard)

            # Card left the hand
            return selectedCard

        except:
            if self.oCard is None:
                print("Object is None Type.")
    
        
     
# ----------------CURRENTLY WORKIN ON!-----------------------------
# Change _retriveID to match what it does which is retrive and sort iDcardSlots; should I, maybe? 

 
    def _retriveId(self, oCard):
        """
        Obtains an oCard's iD and assigns it to self.iDCardSlots.
        By re assigning old iDs we can tell new card where to go in the hand.
        iDCardSlots is sorted by numercial order: low to high values.
        """
        self.iDCardSlots.append(oCard.getCardId())
        self.iDCardSlots.sort() 

# ----------------CURRENTLY WORKIN ON!-----------------------------   


    def cardSwap(self, oCard):
            HAND_LOCATION_DICT = Hand.HAND_LOCATION_DICT
            # Set ID to car using ID card slots
            iDCounter = 0
            if self.iDCardSlots:
                    iDCounter = self.iDCardSlots.pop(0)
                    oCard.setCardId(iDCounter)
            
            # Add card to hand
            # By defult oCard has an iD of 0
            self.cardList.insert(oCard.getCardId(), oCard)

            # Rotate card to 0 degrees
            oCard.setRotation(90)

            # Give card display coordinates based of card iD
            self.cardList[oCard.getCardId()].setLoc(
                     HAND_LOCATION_DICT["HAND_SLOT" + str(oCard.getCardId())]
                     )

            # After card is swapped, make all cards clickable
            self.clickableHand = True
            self.oCardClicked = False
            self.oCard = None
            
    def enterTrick(self):
        """Place card in the middle of the board and wait to battle."""
        # We pop card from hand, return card
        oCardIndex = self.cardList.index(self.oCard)
        oTrickCard = self.cardList.pop(oCardIndex)
        self.clickableHand = True
        self.oCard = None
        self.oCardClicked = False
        # Snapshot the slot the card was in to add new card in that slot
        self._retriveId(oTrickCard)
        return oTrickCard

    # Polymorphism section 

    def setCardClickedToFalse(self, selectedCard):
            """Card set to not selected; GUI buttons do not interact with card no more."""
            selectedCard.setCardClickedToFalse()

    def handleEvent(self, event):
        """
        Returns a bool if any card on hand was clicked.
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

    