import pygwidgets
from BriscaDeck import *

class Game():

    # Class variables
    HAND_LIMIT = 3
    DECK_LOC = (860, 360)
    TRUMP_LOC = (750, 360)
    TRICK_CARDS_LOC_Y = 360
    # TRICK_LOCATION_LIST cordinates (x, y)
    TRICK_LOCATION_LIST = [(250, TRICK_CARDS_LOC_Y), 
                           (500, TRICK_CARDS_LOC_Y)]

    def __init__(self, window, players, SUIT, BRISCA_DICT):
        """Initializing attributes."""
        self.window = window
        self.oDeck = BriscaDeck(self.window, Game.DECK_LOC, 
                                SUIT, RANK_VALUE_DICT=BRISCA_DICT)
        
        self.playerList = players # -----> Adding players to list. NEW!
        
        self.trumpCard = self.oDeck.drawCard()
        self.trumpCard.reveal() 
        self.trumpCard.setLoc(Game.TRUMP_LOC)
        self.trumpCard.setRotation(-90)
        self.trickCount = 0 # ------------------------------------------------------------ TEST for single player
        self.penultimate_trick = 4 # ------------------------------------------------------TEST for single player
        self.trickList = [] # Where cards battle
        self.dealerPot = [] # When there is a tie, the dealer holds cards
        # self.drawCardButton = pygwidgets.TextButton(window, (140, 840), 'Draw', width=100, height=45)
        self.trickButton = pygwidgets.TextButton(window, (20, 840), 'Trick', 
                                                 width=100, height=45)
        # This is the swap trump button
        self.swapButton = pygwidgets.TextButton(window, (20, 780), 'Swap Trump', 
                                                width=100, height=45)
        self.swapButton.disable()
        self.trickButton.disable()

    def battleStep(self):
        """
        Calculates which oTrickCard wins the battle step.
        Sets a turnPlayer by comparing the highest value card.
        """
        player1 = self.trickList[0]['oPlayer'] # player1 is turn player
        player2 = self.trickList[1]['oPlayer'] # player2 is follow on player
        self.calculateTrick(player1, player2)

    def calculateTrick(self, player1, player2):
        """
        Calculate which card has the highest point value.
        Player1 is turn player.
        Player2 is follow on player.
        """
        player1CardValue = self.trickList[0]['oCard'].getRankValue()
        player2CardValue = self.trickList[1]['oCard'].getRankValue()

        if player1CardValue > player2CardValue:
            print("-------You WIN!")
            player1.setTurnPlayerTrue() # Player1 will have the bool to draw firs
            player2.setTurnPlayerFalse()
            self.playerList = [player1] # Player arrangement decides who draws first
                
        else:
            print("-------You LOSE!")
            player2.setTurnPlayerTrue() # Player2 will have the bool to draw first
            player1.setTurnPlayerFalse()
            self.playerList = [player1] # Player arrangement decides who draws first

        #else: # If players end in a tie: cards return to deck
            #print("-------TIE/n")
            #tie = True

    def _clickOnCard(self, oPlayer, event):
        """When a card gets clicked or declicked it offers a few game mechanics."""

        # GUI options after a card is selected
        if oPlayer.handleEvent(event):          
            self.trickButton.enable()

            # Is current selected card swappable and is not the penultimate trick? 
            if self.isTrumpCardSwappable(oPlayer) and self.trickCount <= self.penultimate_trick: # TEST for single player
                    self.swapButton.enable()
            else:
                self.swapButton.disable()

        # GUI options after a card is deselected
        else:
            # Battle (trick) ability unavailable
            self.trickButton.disable()
            self.swapButton.disable()

    # Polymorphism section

    def _preEnterTrick(self, oPlayer):
        """Prepare player's card to enter battle"""

        trickIndex = len(self.trickList) # Get trickList index to identify location on the board
        oTrickCard = oPlayer.enterTrick() # Retrieve player's choosen card to enter battle (trick)
        # Identify player and its choosen card for battle
        playerAndCard = {'oPlayer': oPlayer, 
                         'oCard': oTrickCard} 

        # Set location using trickIndex to map trick card on the board 
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))

        # Add playerAndCard to the trick list to do battle
        self.trickList.append(playerAndCard)

    def compareTrumpCard(self):
        """Check player's cards and id which is a trump card."""
        
        if self.trumpCard != None:
            # Compare player's trump cards to the main trump card
            isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == self.trumpCard.getSuit()
            isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == self.trumpCard.getSuit()
        else:
            trumpCard = self.trickList[0]['oCard']
            # Compare player's leading trump cards to the main trump card
            isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == trumpCard.getSuit()
            isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == trumpCard.getSuit()

        trumpValuesListPerPlayer = [isPlayer1Trump, isPlayer2Trump]

        return trumpValuesListPerPlayer 

    def identifyWinningTrumpCard(self, isPlayer1Trump, isPlayer2Trump):
        """
        Identify which card is the 1st trump card on the board.
        Player1 is turn player.
        Player2 is follow on player.
        """
        print("Battle!\n")

        # Both players have a trump card
        if isPlayer1Trump and isPlayer2Trump: 
            self.battleStep()

        # A player has a trump card
        elif isPlayer1Trump or isPlayer2Trump:   
            if isPlayer1Trump:
                print("-------You WIN!\n")
                self.trickList[0]['oPlayer'].setTurnPlayerTrue() # Player 1 is turn player
                self.trickList[1]['oPlayer'].setTurnPlayerFalse()
                self.playerList = [self.trickList[0]['oPlayer']] # Test 
            else:
                print("-------You LOSE!")
                self.trickList[1]['oPlayer'].setTurnPlayerTrue() # Player 2 is turn player
                self.trickList[0]['oPlayer'].setTurnPlayerFalse()
                self.playerList = [self.trickList[1]['oPlayer']] # Test 

    def _battlePhase(self):
        """This method identifies who is the winner of the trick"""

        trumpValuesListPerPlayer = self.compareTrumpCard()
        self.identifyWinningTrumpCard(trumpValuesListPerPlayer[0], trumpValuesListPerPlayer[1])

    def setPotList(self):
        """Gives turnPlayer the spoils of war, as in the winner gets the cards."""
        # While loop is used, because we are modifying a list
        cardsAndOwners = []
        while self.trickList:
            cardAndOwner = self.trickList.pop(0)
            cardsAndOwners.append(cardAndOwner)
        self.playerList[0].setPotList(cardsAndOwners)  

    def getPotList(self):
        """Prints the name of every card in the turnPlayer's potList."""
        potList = self.playerList[0].getPotList()
        return potList

    def isTrumpCardSwappable(self, oPlayer):
        """
        Function access the player's selected card and compares it with the trump card.
        The method Returns a bool.
        """
        selectedCard = oPlayer.getSelectedCardfromHand()
        if self.trumpCard == None:
            return False

        elif selectedCard.getSuit() == self.trumpCard.getSuit():
            if selectedCard.getRankValue() == 7 and self.trumpCard.getRankValue() > 7:
                return True
            elif selectedCard.getRankValue() == 2 and self.trumpCard.getRankValue() <= 7: 
                return True
            else:
                return False

    def _checkForButtonClick(self, oPlayer, event):
        """Checks for what buttons got click."""

        # Check for draw button
        #if self.drawCardButton.handleEvent(event):
            #self.drawCard(oPlayer) 
            #if oPlayer.getLengthCardsOnHand() == Game.HAND_LIMIT:
                # Enable all cards if hand is full
                #oPlayer.enableAllCardsOnHand()

        # Check for swap button
        if self.swapButton.handleEvent(event):
            self._trumpSwap(oPlayer)
            
        # Check for trick button
        if self.trickButton.handleEvent(event):
            self.enterTrick(oPlayer) # Enter the battle arena of death! Muahahaha!
            self.trickCount += 1 # -------------------------TEST for single player

    def handleEvent(self, event):
        """Handles mouse and keyboard events when triggering card behavior."""

        for oPlayer in self.playerList:    
            # Checks conditions to enable or disable draw button
            self._checkIfPlayerCanDraw(oPlayer)
            # Checks for GUI behaviour after a card is selected or deselected.
            self._clickOnCard(oPlayer, event)
            # Checks which buttons where clicked to induct an action.  
            self._checkForButtonClick(oPlayer, event)    

    def _trumpSwap(self, oPlayer):
        """Action to swap the trump card with hand card."""
        
        swapTrump2Hand = self.trumpCard # Old trump
        newTrump = oPlayer._popCardFromHand() # New Trump
        self.trumpCard = newTrump # set new trump

        # New Trump attributres
        self.trumpCard.setLoc(Game.TRUMP_LOC)
        self.trumpCard.setRotation(-90)

        # New card on hand
        oPlayer._trumpSwap(swapTrump2Hand)

    def enterTrick(self, oPlayer):
        """Place card in the middle of the board and battle."""

        self._preEnterTrick(oPlayer) # Player and card set-up

        # Enter battle phase if there are two cards in the trick list
        if len(self.trickList) == 2:
            self._battlePhase()
            self.setPotList() # Transfer trickCards to winner's pot (potCards)
            print("End of Battle!")

    def draw(self):
        """Display elements to screen."""

        # GUI components
        self.swapButton.draw()
        self.trickButton.draw()
        #self.drawCardButton.draw()

        # Game elements
        if self.trumpCard == None:
            pass
        else:
            self.trumpCard.draw()
        
        if self.trickList: 
            for cardAndOwner in self.trickList:
                cardAndOwner['oCard'].draw()

        for player in self.playerList:
            player.draw()
        self.oDeck.draw()

        # for ghostCard in self.ghostHandList:
            # ghostCard.draw()



    def _checkIfPlayerCanDraw(self, oPlayer):
        """
        Checks conditions to enable or disable draw button.
        Conditions influence card behavior.
        """

        if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:
            if self.trickList: 
                # As long as one card is in the battle phase, draw is disabled
                #self.drawCardButton.disable()
                print("You can't draw, because of the trick.")

            elif self.trumpCard != None: 
                # As long as there is a trump card drawing is possible
                # self.drawCardButton.enable()
                self.drawCard(oPlayer) # draw automatically
                # Keeps player from triggering a card's behavior when clicked
                oPlayer.disableAllCardsOnHand()  
                
                
            else: # When deck is empty and there is no trump card to draw, do below
                # self.drawCardButton.disable() # Desibale draw button
                print("You can't draw, because of their is no deck and trump.")
                oPlayer.enableAllCardsOnHand() # Allows player to play (click) any cards on hand

                # Card is selected ; disable all hand cards
                oCardClick = oPlayer.getCardClick()    
                if oCardClick: 
                    oPlayer.disableAllCardsOnHand()
                         
        else: # After HAND_LIMIT is reached draw button is disabled
            # self.drawCardButton.disable() 
            print("You have reach you hand limit")
            oPlayer.enableAllCardsOnHand() # Allows player to play (click) any cards on hand

    def drawCard(self, oPlayer):
        """Player draws a card."""

        # Assigned oCard the top card from the deck.
        oCard = self.oDeck.drawCard()
        
        # Deck is empty, draw the trump card as your last card.
        if oCard == None:
            oCard = self.trumpCard
            self.trumpCard = None
            oCard.setRotation(90)
            oPlayer.drawCard(oCard)

        else: # Deck is not empty, player drew a card from it.
            oPlayer.drawCard(oCard)






