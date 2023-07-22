import pygwidgets
from BriscaDeck import *

class Game():

    # Class variables
    HAND_LIMIT = 3
    DECK_LOC = (860, 220)
    TRUMP_LOC = (750, 220)
    TRICK_CARDS_LOC_Y = 230
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
        self.trickButton = pygwidgets.TextButton(window, (20, 630), 'Trick', 
                                                 width=100, height=45)
        # This is the swap trump button
        self.swapButton = pygwidgets.TextButton(window, (20, 580), 'Swap Trump', 
                                                width=100, height=45)
        self.swapButton.disable()
        self.trickButton.disable()
   
    def getPotList(self):
        """Prints the name of every card in the turnPlayer's potList."""
        potList = self.playerList[0].getPotList()
        print(potList) 

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

    def draw(self):
        """Display elements to screen."""

        # GUI components
        self.swapButton.draw()
        self.trickButton.draw()

        # Game elements
        if self.trumpCard == None:
            pass
        else:
            self.trumpCard.draw()
        
        if self.trickList: # Player's can see their cards in the trick zone.
            for cardAndOwner in self.trickList:
                # Without line of code below the player's can see their hands when in a trick
                cardAndOwner['oPlayer'].draw()
                # Player's can see their trick card
                cardAndOwner['oCard'].draw()

        for oPlayer in self.playerList:
            oPlayer.draw()

        self.oDeck.draw()

        # for ghostCard in self.ghostHandList:
            # ghostCard.draw()

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
    

# Currently working here!
 
    def handleEvent(self, event):
        """Depending on human vs AI behavior defers.
       For humans: Mmethod Handles mouse and keyboard events when triggering card behavior.
       Fo AI: It checks if it has cards on hand and directly plays a card.
        """

        human = True

        for oPlayer in self.playerList[:]:
     
            # Is current player AI or human?
            if oPlayer.isObjHumanOrRobot() == human and oPlayer.getTurnPlayer():
                # Human actions only!
                print("--Human inside loop--")
                self._humanHandleEvents(oPlayer, event)

            elif oPlayer.isObjHumanOrRobot() != human and oPlayer.getTurnPlayer() == True:
                # is Ai turn player?
                print("--Robot is now turn player--")
                self._AIHandleEvents(oPlayer)
   
# ------------------------------------ Work In progress --------------------------         
    
    def _AIHandleEvents(self, oPlayer):
        """Method helper to give Ai instructions to do specific actions."""
        
        # AI can draw a card if possible
        self._checkIfAIPlayerCanDraw(oPlayer) 
        # AI enters trick if it has cards on hand
        self._checkIfAIPlayerCanTrick(oPlayer)





# ----------------------- AI Player handleEvent stuff -------------------------------'
    def _checkIfAIPlayerCanDraw(self, oPlayer):
        """
        Checks conditions to enable or disable automatic drawing.
        Conditions influence card behavior.
        """

        if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:
            print("In")

            if self.trickList: 
                # As long as one card is in the trick list, skip block
                pass

            if self.trumpCard != None: 
                # As long as there is a trump card drawing is possible
                self.drawCard(oPlayer) # draw automatically

                if oPlayer.isObjHumanOrRobot() == False:
                    print("Robot drew")
                         
    def _checkIfAIPlayerCanTrick(self, oPlayer):
        """Code checks if AI has any cards on hand.
        If AI has cards on hand it can pick a card.
        """
        # Does AI have any cards left in its hand?
        aIHasCardsLeft = oPlayer.getCardsOnHand()
        
        # 
        if aIHasCardsLeft == Game.HAND_LIMIT:
            # Enter the battle arena of death! Muahahaha!
            self.enterTrick(oPlayer)
        
        elif len(aIHasCardsLeft) < Game.HAND_LIMIT and self.trumpCard == None:
            self.enterTrick(oPlayer)
        
        elif aIHasCardsLeft == False:
            print("No cards on hand.")


# ----------------------- Human Player handleEvent stuff -------------------------------
    def _humanHandleEvents(self, oPlayer, event):
        """Method helper to house human actions."""

        # Checks conditions to enable or disable automatic draw
        self._checkIfPlayerCanDraw(oPlayer)               
        # Checks for GUI behaviour after a card is selected or deselected.
        self._clickOnCard(oPlayer, event)
        # Checks which buttons where clicked to induct an action.  
        self._checkForButtonClick(oPlayer, event)

    def _checkIfPlayerCanDraw(self, oPlayer):
        """
        Checks conditions to enable or disable automatic drawing.
        Conditions influence card behavior.
        """

        if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:

            if self.trickList: 
                # As long as one card is in the trick list, skip block
                pass

            elif self.trumpCard != None: 
                # As long as there is a trump card drawing is possible
                self.drawCard(oPlayer) # draw automatically
                oPlayer.disableAllCardsOnHand() # Keeps player from triggering a card's behavior when clicked

            else: # You can't draw, because their is no deck and trump
                oPlayer.enableAllCardsOnHand() # Allows player to play (click) any cards on hand

                # Card is selected ; disable all hand cards
                oCardClick = oPlayer.getCardClick()    
                if oCardClick: 
                    oPlayer.disableAllCardsOnHand()
                         
        else: # After HAND_LIMIT is reached automatic drawing is disabled
            # print("You have reach you hand limit")
            oPlayer.enableAllCardsOnHand() # Allows player to play (click) any cards on hand

            # Card is selected ; disable all hand cards
            oCardClick = oPlayer.getCardClick()    
            if oCardClick: 
                oPlayer.disableAllCardsOnHand()

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

    def _checkForButtonClick(self, oPlayer, event):
        """Checks for what buttons got click."""

        # Check for swap button
        if self.swapButton.handleEvent(event):
            self._trumpSwap(oPlayer)
            
        # Check for trick button
        if self.trickButton.handleEvent(event): 
            self.enterTrick(oPlayer) # Enter the battle arena of death! Muahahaha!
            self.trickCount += 1 # -------------------------TEST for single player


# ---------------------------- Enter Trick for battle (Main Trick Methods) -----------------------------------
    def enterTrick(self, oPlayer):
        """Place card in the middle of the board and battle."""

        # Player and card set-up into the trickList
        self._preEnterTrick(oPlayer) 

        # Enter battle phase if there are two players in the trickList
        if len(self.trickList) == 2:
            self._battlePhase()
            print("End of Battle!")

            # Transfer trickCards to winner's pot (potCards)
            self.setPotList() # ---------------------------------------> Currently working here
            print("Winner got the spoils of WAR!")

            # Add players back to playerList
            self.reAddPlayerstoPlayerList() 

            for player in self.playerList: # Check if the player's are in the player List
                print(f"{player.isObjHumanOrRobot()} is in the playerList.")
 
        else:
            print("Waiting")

    def _preEnterTrick(self, oPlayer):
        """Prepare player's card to enter battle"""
        # NOTE: Turn player is removed from player list.

        trickIndex = len(self.trickList) # Get trickList index to identify location on the board
        oTrickCard = oPlayer.enterTrick() # Retrieve player's choosen card to enter battle (trick) 
        # Set location using trickIndex to map trick card on the board 
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))

        # Identify player and its choosen card for battle
        playerAndCard = {'oPlayer': oPlayer, 
                         'oCard': oTrickCard}
        
        # Pop player from playerList
        transferPlayer = self.popPlayerFromPlayerList(playerAndCard)
        # Add player to trickList trickList
        self.addPlayerToTrickList(transferPlayer)
        # End player's turn by chnaging it's turnPlayer var to False
        self.setTurnPlayerFalse(transferPlayer)
        # Pending player can now play their turn
        self.setNewTurnPlayer()

        # Players fight in the battlePhase()
    
    def _battlePhase(self):
            """This method identifies who is the winner of the trick"""

            # Retrive trumnp values per player
            trumpValuesListPerPlayer = self.compareTrumpCard() 
            # Id the winner of the trick
            self._identifyTrickWinner(trumpValuesListPerPlayer[0], 
                                          trumpValuesListPerPlayer[1])


# ------------------------ _preEnterTrick methods ----------------
    def popPlayerFromPlayerList(self, playerAndCard):
        """We pop the player. Then return the parameter as it came."""
        i = self.playerList.index(playerAndCard['oPlayer'])
        self.playerList.pop(i)
        return playerAndCard

    def addPlayerToTrickList(self, playerAndCard):

        # Add playerAndCard to the trick list to do battle
        self.trickList.append(playerAndCard)

    def setTurnPlayerFalse(self, playerAndCard):
        """Curent turnPlayer ended their turn.
        Set current turnPlayer to False to symbolize that they ended their turn.
        Make pending player turnPlayer.
        """
        playerAndCard['oPlayer'].setTurnPlayerFalse() 

    def setNewTurnPlayer(self):
        self.playerList[0].setTurnPlayerTrue()
        

# ------------------------ _battlePhase methods ------------------
    # Checks who one the battlePhase()
    def _identifyTrickWinner(self, isPlayer1Trump, isPlayer2Trump):
        """
        Identify which player won and sets them to trunPlayer (True).
        Player1 is turn player.
        Player2 is follow on player.
        """
        print("Battle!\n")
        self.caluculateTrump(isPlayer1Trump, isPlayer2Trump)

    # Check if player's card is a trump using True or False
    def compareTrumpCard(self):
        """Return a list with bool values 
        identifying if player's have a trump card or not.
        """

        # If there is a trump card on the game board 
        if self.trumpCard != None:
            # Compare player's trump cards to the main trump card; True or False
            isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == self.trumpCard.getSuit()
            isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == self.trumpCard.getSuit()

        # else make the leading card in the trickList the trump card 
        else:
            trumpCard = self.trickList[0]['oCard']
            # Compare player's leading trump cards to the main trump card
            isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == trumpCard.getSuit()
            isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == trumpCard.getSuit()

        trumpValuesListPerPlayer = [isPlayer1Trump, isPlayer2Trump]

        return trumpValuesListPerPlayer 

    # Check if a player can win using a trump card or enter battleStep()
    def caluculateTrump(self, isPlayer1Trump, isPlayer2Trump):

        # Both players have a trump card
        if isPlayer1Trump and isPlayer2Trump: 
            self.battleStep()

        # A player has a trump card
        elif isPlayer1Trump or isPlayer2Trump:   
            if isPlayer1Trump:
                print("-------You WIN!\n")
                self.trickList[0]['oPlayer'].setTurnPlayerTrue() # Player 1 is turn player
                self.trickList[1]['oPlayer'].setTurnPlayerFalse()

            else:
                print("-------You LOSE!")
                self.trickList[1]['oPlayer'].setTurnPlayerTrue() # Player 2 is turn player
                self.trickList[0]['oPlayer'].setTurnPlayerFalse()
                self.trickList.reverse() # This makes player 2 become player 1 for the next round

    # If both players have the same trump card you've entered battleStep()
    def battleStep(self):
        """Calculates which is the highest oTrickCard value between the players."""
        player1 = self.trickList[0]['oPlayer'] # player1 is turn player
        player2 = self.trickList[1]['oPlayer'] # player2 is follow on player
        self.calculateTrick(player1, player2)

    # After entering battleStep() compare card values. Highest rank wins
    def calculateTrick(self, player1, player2):
        """
        Calculate which card has the highest point value.
        Player1 is turn player. Player2 is follow on player.
        Winner is set as turnPlayer.
        """
        player1CardValue = self.trickList[0]['oCard'].getRankValue()
        player2CardValue = self.trickList[1]['oCard'].getRankValue()

        if player1CardValue > player2CardValue:
            print("-------You WIN!")
            player1.setTurnPlayerTrue() # Player1 will have the bool to draw firs
            player2.setTurnPlayerFalse()
                
        else:
            print("-------You LOSE!")
            player2.setTurnPlayerTrue() # Player2 will have the bool to draw first
            player1.setTurnPlayerFalse()
            self.trickList.reverse() # This makes player 2 become player 1 for the next round

    # The winner gets the spoils of WAR
    def setPotList(self):
        """Gives turnPlayer the spoils of war, as in the winner gets the cards.
        I didn't use a while loop to iterate, because I wasn't going to...
        remove
        """

        oCards = []
        for i in self.trickList[:]:
            index = self.trickList.index(i)
            oCard = self.trickList[index].pop(['oCard'])
            oCards.append(oCard)

        self.playerList[0].setPotList(oCards)  

    # Add playesr back to the playerList to starts a new round
    def reAddPlayerstoPlayerList(self):
        """re-add players back to playerList. 
        This means that players will be able to draw and battle again.
        Make trick (battle) winner turn player, that player will draw and play frist.
        """

        # Loop till there are no more trickPlayers in the trickList.
        while self.trickList:
            trickPlayer = self.trickList[0].pop(['oPlayer'])
            self.playerList.append(trickPlayer)
