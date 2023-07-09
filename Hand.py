

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
        self.oCardClicked = False # Used in parallel with oCard's self.oCardClicked.


    def disableAllCardsOnHand(self):
        """Disables all cards on hand to avoid being click able.""" 
        self.clickableHand = False
    
    def enableAllCardsOnHand(self):
        """Enables all cards on hand to be click able.""" 
        self.clickableHand = True

    def getCardClick(self):
        """Returns a bool of card's click status."""
        return self.oCardClicked
    
    def addCardToHand(self, oCard):
         self.cardList.insert(oCard.getCardId(), oCard)
    
    def setHandCorrdinatesForDisplay(self, oCard):
        # Give card display coordinates based of card iD
        self.cardList[oCard.getCardId()].setLoc(
                    Hand.HAND_LOCATION_DICT["HAND_SLOT" + str(oCard.getCardId())]
                    )




    def enterTrick(self):
        """
            Take card from hand. 
            Returns an oCard to be a trick card; a card that will battle. 
        """
        oTrickCard = self._popCardFromHand()
        self.oCard = None

        return oTrickCard




    def getLengthCardsOnHand(self):
        """Returns the total number of cards on hand."""
        return len(self.cardList)

    # Has a Note
    def getCardsOnHand(self):
        """Returns a list of cards on hand."""
        # NOTE: This method is connected to Player class,
        # but Game cass is not using it.
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

    def retriveCardId(self, oCard):
            """
            Get the oCard's iD and assigns it to self.iDCardSlots.
            By re assigning old iDs we can tell new card where to go in the hand.
            iDCardSlots is sorted by numercial order to avoid erros.
            """
            self.iDCardSlots.append(oCard.getCardId())
            self.iDCardSlots.sort() 

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




    def _popCardFromHand(self):
        """
        This method retrives a card from the hand and returns the selected card 
        as the new trump card or for selcted card to enter a trick.
        """
        try: 
            oCardIndex = self.cardList.index(self.oCard) # Identify card's index.
            selectedCard = self.cardList.pop(oCardIndex) # Use index to pop oCard from the hand

            self.enableAllCardsOnHand() # Enables other cards on hand to be selected
            self.setCardClickedToFalse(selectedCard) # Selected card is set to unclickled, a.k.a False
            self.retriveCardId(selectedCard) # Obtain selected card's iD; Id is reassiged to a drawn or swaped card.
            
            return selectedCard # Card left the hand; (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ peace the fuck out!

        except:
            if self.oCard is None:
                print("Object is None Type.")




    def _trumpSwap(self, oCard):
        """Takes trump card and adds it to the hand."""
            
        HAND_LOCATION_DICT = Hand.HAND_LOCATION_DICT

        self.setCardId(oCard) # Set id cordinates for the swaped trump card  
        self.addCardToHand(oCard) # Add swaped trump card to hand
        oCard.setRotation(90) # Rotate trump card upside-up to match the other cards in hand
        self.setHandCorrdinatesForDisplay(self, oCard) # Give card display coordinates mapped by card iD
        self.enableAllCardsOnHand() # After card is swapped, make all cards in hand clickable
        self.setCardClickedToFalse(oCard) # The oCard place holder, has been unclicked
        self.oCard = None # Empty place holder       
            
    def _drawCard(self, oCard):
        """Adds card to player's hand. If none; return no card error."""
        
        oCard.reveal() # Reveal card to Player
        self.setCardId(oCard) # Give card an id; by defult oCard has an iD of 0
        self.addCardToHand(oCard) # Player has a card in hand via a list
        self.setHandCorrdinatesForDisplay(oCard) # Give card display coordinates based of card iD

    # Polymorphism section 

    # Has a Note
    def setCardClickedToFalse(self, selectedCard):
            """Card set to not selected; GUI buttons do not interact with card no more."""
            #NOTE: self.oCardClicked is ued to tell the handleEvent how to haddle button configurations.

            selectedCard.setCardClickedToFalse() # Tells oCard that it is false
            self.oCardClicked = False # Tells hand that oCard has been set to false

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

    