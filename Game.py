import pygwidgets
import pyghelpers
from BriscaDeck import *

class Game(): # Object Manager

    # Class variables
    TIMER_LENGTH = 2
    HAND_LIMIT = 3
    DECK_LOC = (860, 220)
    TRUMP_LOC = (750, 220)
    TRICK_CARDS_LOC_Y = 230
    # TRICK_LOCATION_LIST cordinates (x, y)
    TRICK_LOCATION_LIST = [(250, TRICK_CARDS_LOC_Y), 
                           (500, TRICK_CARDS_LOC_Y)]

    def __init__(self, window, players):
        """Initializing attributes."""
        
        self.window = window
        self.oDeck = BriscaDeck(self.window, Game.DECK_LOC)
        
        self.playerList = players
        self.trumpCard = self.oDeck.drawCard()
        self.trumpCard.reveal() 
        self.trumpCard.setLoc(Game.TRUMP_LOC)
        self.trumpCard.setRotation(-90)
        self.isPlayer1Trump = False
        self.isPlayer2Trump = False
        self.enterBattleStep = False
        self.trickCount = 0
        self.penultimate_trick = 16 # It takes 16 tricks to disable the swap feature
        self.trickList = [] # Where cards battle
        self.dealerPot = [] # Dealer transfers trick cards to the trick winner
        self.isGameOver = False
        self.areHandsEmpty = []
        self._initUIElements(self.window)

        self.oCountDownTimer = pyghelpers.CountDownTimer(Game.TIMER_LENGTH)
        self.timerRunning = False   

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

    def _playersDrawPahse(self, human):
        """Iterate playerList till all players have drawn.
        The order on who draws first is determine by who is turnPlayer.
        TurnPlayer draws first, then the player that follows.
        Repeat till all players have 3 cards.
        """

        #  Create a local var to feed it a copy of playerList, 
        #  to indicate who should draw first.
        drewPlayers = []
        
        # Draw untill all player have drawn
        while self.playerList:

            # Strip player from list to draw 
            oPlayer = self.playerList.pop(0)
            
            # Human actions only!
            if oPlayer.isObjHumanOrRobot() == human:

                # Checks conditions to enable or disable automatic draw
                self._checkIfPlayerCanDraw(oPlayer) 

            # AI actions only!
            else:

                # AI can draw a card if possible
                self._checkIfAIPlayerCanDraw(oPlayer) 
            
            # pop players to exit while loop after all players have drawn
            popDrewPlayer = oPlayer
            drewPlayers.append(popDrewPlayer)
        
        # Add player back to playerList
        while drewPlayers:
            popedPlayer = drewPlayers.pop(0)
            self.playerList.append(popedPlayer)
        
        # All player have drawn

    def handleEvent(self, event):
        """ Draw event, players' events & update points event
        Human & AI behavior behavior.
        Player draw automaticaly.
        For humans: method handles mouse and keyboard events when triggering card behavior.
        Fo AI: It checks if it has cards on hand and directly plays the most left card in its hand.
        """

        human = True
        self._playersDrawPahse(human) # Draw before you choose to enter a trick

        # Players choose which card to enter a trick with
        for oPlayer in self.playerList[:]: 

            # Human actions only!
            if oPlayer.isObjHumanOrRobot() == human and oPlayer.getTurnPlayer():
                self._humanHandleEvents(oPlayer, event)

            # AI actions only!
            else:
                if oPlayer.getTurnPlayer(): # If AI is turn player then it can play.
                    self._AIHandleEvents(oPlayer)

        if len(self.trickList) == 2: # Are all players ready?
            if not self.timerRunning:
                self.oCountDownTimer.start() # Start cool down to see cards on the table
                self.timerRunning = True

        else:
            print("Waiting other player.")
        
        if self.oCountDownTimer.ended(): # When time is up, functionality runs as normal
            self.timerRunning = False
            self.enterTrick() # We stop the game to be able to see cards on the board.     

        # Update human player's points on his screen
        self.pointsUIUpdate()
        
        # Is it game over?
        self._checkForGameOver()


    def draw(self):
        """Display elements to screen."""

        # GUI components
        self.swapButton.draw()
        self.trickButton.draw()
        self.humanPlayerPointsDisplay.draw()

        # Display the game's cards
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

        # Players can see their cards while waiting to enter a trick.
        for oPlayer in self.playerList:
            oPlayer.draw()

        self.oDeck.draw()

        if self.isGameOver:
            self.gameOverDisplay.draw()
            self.winnerScoreDisplay.draw()

# ----------------------- UI Events -------------------------------
    def _updateUI(self):
        """Update Player's game UI elemnets."""

        self.pointsUIUpdate()

    def pointsUIUpdate(self):
        """Method tells 'self.humanPlayerPointsDisplay' to update the human points in the window."""

        for player in self.playerList:

            if player.isObjHumanOrRobot():
                self.humanPlayerPointsDisplay.setValue(f"Points: {player.getPoints()}")

    def _initUIElements(self, window):
        """Init all UI elements"""

        self.trickButton = pygwidgets.TextButton(window, (20, 630), 'Trick', 
                                                 width=100, height=45)
        # This is the swap trump button
        self.swapButton = pygwidgets.TextButton(window, (20, 580), 'Swap Trump', 
                                                width=100, height=45)
        self.swapButton.disable()
        self.trickButton.disable()
      
        # Human UI points display (None = defult values)
        self.humanPlayerPointsDisplay = pygwidgets.DisplayText(window, loc=(140, 590), 
                                                                value=f'Points: 0', 
                                                                fontName=None, fontSize=24, 
                                                                width=None, height=None, 
                                                                textColor=(255, 215, 0), # Gold color
                                                                backgroundColor=None, justified='left', 
                                                                nickname=None)
        # Game Over display
        self.gameOverDisplay = pygwidgets.DisplayText(window, loc=(450, 360), 
                                                                value='Game Over', 
                                                                fontName=None, fontSize=48, 
                                                                width=None, height=None, 
                                                                textColor=(255, 215, 0), # Gold color
                                                                backgroundColor=None, justified='center', 
                                                                nickname=None)
        # Winner Score Display 
        self.winnerScoreDisplay = pygwidgets.DisplayText(window, loc=(210, 460), 
                                                                value='', 
                                                                fontName=None, fontSize=48, 
                                                                width=None, height=None, 
                                                                textColor=(255, 215, 0), # Gold color
                                                                backgroundColor=None, justified='left', 
                                                                nickname=None)

# ----------------------- Game Over stuff -------------------------------
    def check4Winner(self):

        playerAndPoints = {}
        players = []

        for oPlayer in self.playerList:
            playerAndPoints = {}
            playerAndPoints['isPlayerHuman'] = oPlayer.isObjHumanOrRobot()
            playerAndPoints['maxPoints'] = oPlayer.getPoints()
            players.append(playerAndPoints)
        
        trunPlayerPoints = players[0]['maxPoints']
        followOnPlayerPoints = players[1]['maxPoints']

        # Compare's player's points
        if trunPlayerPoints > followOnPlayerPoints:
            if players[0]['isPlayerHuman']:
                print(f"The turn player is Human")
                return f"Human Player is the WINNER with {trunPlayerPoints} points!"
        
            else:
                print(f"The turn player is Robot")
                return f"Robot player is the WINNER with {trunPlayerPoints} points!"

        else:
            if players[1]['isPlayerHuman']:
                print(f"The follow on player is Human")
                return f"Human Player is the WINNER with {followOnPlayerPoints} points!"
        
            else:
                print(f"The follow on player is Robot")
                return f"Robot player is the WINNER with {followOnPlayerPoints} points!!"
        
    def _checkForGameOver(self):
        """Verify that players have played their last card.
        And check who is the winner.
        """
        
        for oPlayer in self.playerList:
            # Iterrate and check if hands are empty
            cardsOnHand = oPlayer.getCardsOnHand()
            self.areHandsEmpty.append(cardsOnHand)
        
        # If both hands have zero cards on hand then trigger game over.
        if len(self.areHandsEmpty[0]) == 0 and len(self.areHandsEmpty[1]) == 0:
            print("Game over")
            self.isGameOver = True # set other elemnets to be drawn on screen
            self.winnerScoreDisplay.setValue(self.check4Winner()) # Sets the winner to be displayed on screen.

# ----------------------- AI Player handleEvent stuff -------------------------------
    def _AIHandleEvents(self, oPlayer):
            """Method helper to give Ai instructions to do specific actions."""
            
            # AI enters trick if it has cards on hand
            self._checkIfAIPlayerCanTrick(oPlayer)

    def _checkIfAIPlayerCanDraw(self, oPlayer):
        """
        Checks conditions to enable or disable automatic drawing.
        Conditions influence card behavior.
        """

        if oPlayer.getLengthCardsOnHand() < Game.HAND_LIMIT:

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
        
        if len(aIHasCardsLeft) == Game.HAND_LIMIT:
            # AI has enter the battle arena of death! Muahahaha!
            self._preEnterTrick(oPlayer)
            
        elif len(aIHasCardsLeft) == 0:
            pass # No cards on hand
        
        # If cards are less then MAX and there are no more cards to draw
        elif len(aIHasCardsLeft) < Game.HAND_LIMIT and self.trumpCard == None:
            self._preEnterTrick(oPlayer)
            
            
        
# ----------------------- Human Player handleEvent stuff -------------------------------
    def _humanHandleEvents(self, oPlayer, event):
        """Method helper to house human actions."""
              
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
                print("Human drew.")

            else: # You can't draw, because their is no deck and trump
                oPlayer.enableAllCardsOnHand() # Allows player to play (click) any cards on hand

                # Card is selected ; disable all hand cards
                oCardClick = oPlayer.getCardClick()    
                if oCardClick: 
                    oPlayer.disableAllCardsOnHand()
                         
        else: # After HAND_LIMIT is reached automatic drawing is disabled
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
        """Checks which buttons got click by the player."""

        # Check for swap button
        if self.swapButton.handleEvent(event):
            self._trumpSwap(oPlayer)
            
        # Check for trick button
        if self.trickButton.handleEvent(event): 
            self._preEnterTrick(oPlayer) # Enter the battle arena of death! Muahahaha!
            self.trickCount += 1 # Need it to track trump swap feature

# ---------------------------- Enter Trick for battle (Main Trick Methods) -----------------------------------
    def enterTrick(self):
        """Place card in the middle of the board and battle."""

        # Player and card set-up into the trickList in the self._preEnterTrick(oPlayer)
        # Then they enter the trick if there are two players in the trickList

        print("Beginning of Trick!")
        self._battlePhase()
        print("End of Trick!")

        # Dealer obtains trick cards
        self.dealerGetWinnings()

        # Add players back to playerList
        self.reAddPlayerstoPlayerList()

        # CHECKING WHO IS TURN PLAYER AFTER A ROUND
        print(self.playerList) 

        # Dealer(Game class) gives cards and calculates turnPlayer's turn
        self.setPotList()
 
    def _preEnterTrick(self, oPlayer):
        """Prepare player's card to enter battle"""

        trickIndex = len(self.trickList) # Get trickList index to identify location on the board
        oTrickCard = oPlayer.enterTrick() # Retrieve player's choosen card to enter battle (trick) 
        # Set location using trickIndex to map trick card on the board 
        oTrickCard.setLoc((Game.TRICK_LOCATION_LIST[trickIndex]))

        # Identify player and its choosen card for battle
        playerAndCard = {'oPlayer': oPlayer, 
                         'oCard': oTrickCard}
        
        # Pop player from playerList
        transferPlayer = self.popPlayerFromPlayerList(playerAndCard)
        self.addPlayerToTrickList(transferPlayer)   # Add player to trickList trickList
        self.revealCard(transferPlayer)             # Reveal oPlayer's card.
        self.setTurnPlayerFalse(transferPlayer)     # End player's turn by changing it's turnPlayer var to False
        self.setNewTurnPlayer()                     # Pending player can now play their turn
        # Players fight in the battlePhase()

    def dealerGetWinnings(self):
        """Dealer obtains players trick cards.
        refPlayerAndCard means that we are referencing to the object(dict)
        """

        for i in self.trickList[:]:
            # the i is a dict ['oPlayer': oPlayer, 'oCard': oBriscaCard]
            trickCardTransfer = i.pop('oCard')
            self.dealerPot.append(trickCardTransfer)

    def reAddPlayerstoPlayerList(self):
        """Add playesr back to the playerList to starts a new round"""

        # Loop till there are no more trickPlayers in the trickList.
        while self.trickList:
            trickPlayerTransfer = self.trickList.pop(0)
            oPlayer = trickPlayerTransfer['oPlayer']
            self.playerList.append(oPlayer)

    def setPotList(self):
        """Gives turnPlayer the spoils of war, as in the winner gets the cards."""

        oCards = []
        turnPlayer = self.playerList[0]

        while self.dealerPot:
            oCard = self.dealerPot.pop(0)
            # print(f"The {oCard.getName()} is in the {self.playerList[0]} pot.")
            # oCard is inside a dictionary
            oCards.append(oCard) 
    
        # Turn player adds their winnings from the last trick they played.
        turnPlayer.setPotList(oCards)
        # Calculate turnPlayer's points
        self.updatePlayerScore(turnPlayer)

# ------------------------ _preEnterTrick methods ----------------
    def popPlayerFromPlayerList(self, playerAndCard):
        """We pop the player. Then return the parameter as it came."""

        i = self.playerList.index(playerAndCard['oPlayer'])
        self.playerList.pop(i)
        return playerAndCard

    def revealCard(self, playerAndCard):
        """Now you can see the front side of the card."""

        playerAndCard['oCard'].reveal()

    def addPlayerToTrickList(self, playerAndCard):
        """Adds player's to 
        the trick list and other wait for a trick to begin or battle.
        """

        # Add playerAndCard to the trick list to do battle
        self.trickList.append(playerAndCard)

    def setTurnPlayerFalse(self, playerAndCard):
        """Curent turnPlayer ended their turn.
        Set current turnPlayer to False to symbolize that they ended their turn.
        Make pending player turnPlayer.
        """
        playerAndCard['oPlayer'].setTurnPlayerFalse() 

    def setNewTurnPlayer(self):
        """Once all players are not in playerList we exit the method with pass."""

        if self.playerList:
            self.playerList[0].setTurnPlayerTrue()
        else:
            pass

# ------------------------ _battlePhase methods ------------------
    def _battlePhase(self):
            """This method calculates battle points in the trick."""

            # Retrive trumnp values per player
            self.compareTrumpCard() 
            # Id the winner of the trick
            self._identifyTrickWinner()
            self.resetPlayerTrumps()
   
    def compareTrumpCard(self):
        """Identifying which player has a trump card."""

        # If there is a trump card on the game board 
        if self.trumpCard != None:
            # Compare player's trump cards to the main trump card; True or False
            self.isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == self.trumpCard.getSuit()
            self.isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == self.trumpCard.getSuit()

            print("----------------------Player's trump:----------------------")
            print(f"The player 1's {self.trickList[0]['oCard'].getName()} its trump is set to {self.isPlayer1Trump}.")
            print(f"The player 2's {self.trickList[1]['oCard'].getName()} its trump is set to {self.isPlayer2Trump}\n.")

            # Check if their both false; 
            if self.isPlayer1Trump == False and self.isPlayer2Trump == False:
                # leading card in the trickList is the leading trump card
                self.leadingTrumpCard()
                
        else: # else make the leading card in the trickList the trump card
            self.leadingTrumpCard()
    
    def leadingTrumpCard(self):
        """First card in the trickList becomes trump card."""
        
        trumpCard = self.trickList[0]['oCard']
        print("----------------------Not trump card in trick!----------------------")
        print(f"The leading trump card instead is {trumpCard.getName()}\n")
        self.isPlayer1Trump = self.trickList[0]['oCard'].getSuit() == trumpCard.getSuit()
        self.isPlayer2Trump = self.trickList[1]['oCard'].getSuit() == trumpCard.getSuit()

    def _identifyTrickWinner(self):
        """Identify which player won and sets it as the trunPlayer (True)."""

        self.caluculateTrump()        
        if self.enterBattleStep: # Both players have a trump
            print("Entered battle step")
            self.battleStep()

    def caluculateTrump(self):
        """Check if a player can win using a trump card or enter battleStep()"""

        # Both players have a trump card
        if self.isPlayer1Trump and self.isPlayer2Trump: 
            self.enterBattleStep = True

        # A player has a trump card
        elif self.isPlayer1Trump or self.isPlayer2Trump:
            print("trump battle:\n")   
            
            if self.isPlayer1Trump:    
                self.trickList[0]['oPlayer'].setTurnPlayerTrue() # Player 1 is turn player
                self.trickList[1]['oPlayer'].setTurnPlayerFalse()
                print(f"Leading player WINs with the {self.trickList[0]['oCard'].getName()}!")
                print(f"Follow on player LOST with the {self.trickList[1]['oCard'].getName()}!\n")
               
            else:
                self.trickList[1]['oPlayer'].setTurnPlayerTrue() # Player 2 is turn player
                self.trickList[0]['oPlayer'].setTurnPlayerFalse()
                print(f"Leading player LOST with the {self.trickList[0]['oCard'].getName()}!")
                print(f"Follow on player WINs with the {self.trickList[1]['oCard'].getName()}!\n")
                self.trickList.reverse() # This makes player 2 become player 1 for the next round

    def battleStep(self):
        """Calculates which is the highest oTrickCard value between the players."""
        player1 = self.trickList[0]['oPlayer'] # player1 is turn player
        player2 = self.trickList[1]['oPlayer'] # player2 is follow on player
        self.calculateTrick(player1, player2)

    def calculateTrick(self, player1, player2):
        """
        Calculate which card has the highest point value.
        Player1 is turn player. Player2 is follow on player.
        Winner is set as turnPlayer.
        """
        print("Both players have trump card:\n")

        player1CardValue = self.trickList[0]['oCard'].getRankValue()
        player2CardValue = self.trickList[1]['oCard'].getRankValue()

        if player1CardValue > player2CardValue:
            print(f"{self.trickList[0]['oPlayer']} with {self.trickList[0]['oCard'].getName()} WINs with a value of {player1CardValue}!")
            print(f"{self.trickList[1]['oPlayer']} with {self.trickList[1]['oCard'].getName()} LOST with a value of {player2CardValue}!\n")
            # If last trick don't make new turn player
            
            player1.setTurnPlayerTrue() # Player1 will have the bool to draw first
            player2.setTurnPlayerFalse()
                
        else:
            # If last trick don't make new turn player

            print(f"{self.trickList[1]['oPlayer']} with {self.trickList[1]['oCard'].getName()} WINs with a value of {player2CardValue}!")
            print(f"{self.trickList[0]['oPlayer']} with {self.trickList[0]['oCard'].getName()} LOST with a value of {player1CardValue}!\n")
            player2.setTurnPlayerTrue() # Player2 will have the bool to draw first
            player1.setTurnPlayerFalse()
            self.trickList.reverse() # This makes player 2 become player 1 for the next round
        
        self.enterBattleStep = False # Reset enterBattleStep because the battle finished

    def resetPlayerTrumps(self):
        self.isPlayer1Trump = False
        self.isPlayer2Trump = False

    def updatePlayerScore(self, turnPlayer):
        """If the player is human update it's score."""

        turnPlayer.claculatePotCards()

        if turnPlayer.isObjHumanOrRobot():
            print(f"Your points total to {turnPlayer.getPoints()}")