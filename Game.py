import pygwidgets
from Deck import *
from Card import *
from Player import *

class Game():
    # Class Variables
    PLAYER_HAND_CARDS_BOTTOM = 100 # Y coordinate; where player hand will go
    GHOST_HAND_CARDS_TOP = 400 # Y coordinate; where ghost cards will go; top of screen
    BUFFER_BETWEEN_HAND_CARDS = 150 # Space between cards in player's hand
    CARDS_LEFT = 350 # X coordinate; 1st card in the hand; buffer will be added 
    MAX_HAND = 3
    DISPLAY_STARTING_HANDS = 3
    DECK_LOCATION = (600, 500)
    
    def __init__(self, window, playerList):
        """Initisialize attributes."""
        self.window = window
        self.oDeck = Deck(self.window)
        self.trumpCard = None
        self.dealerPot = []
        self.ghostHandList = [] # Holds place holder cards for ghost player
        self.playerList = playerList # LIST is given by client
        self.potScore = 0
        self.potScoreText = pygwidgets.DisplayText(window, (450, 164),
                                        f'Pot Score: {self.potScore}',
                                        fontSize=36, textColor=(255, 255, 255))
        
        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                        f'', width=900, justified='center',
                                        fontSize=36, textColor=(255, 255, 255))
        
        # Calculate player & ghost card locations for their hands on the game's board
        self.handPosXList = []
        leftToRight = Game.CARDS_LEFT # Starting card to the left of the player's hand
        # Calculate the x positions of all cards, once 
        for i in range(Game.DISPLAY_STARTING_HANDS): # 3 cards
            # Add the coresponding space for the oCard to inhabit
            self.handPosXList.append(leftToRight)
            # Space between cards in the player's hand
            leftToRight += Game.BUFFER_BETWEEN_HAND_CARDS

        # Players now have knowledge of where to place their cards on the board
        for playerIndex in range(len(self.playerList.copy())):
            self.playerList[playerIndex].setHandPosX(self.handPosXList)

        # Card shuffle sound
        self.cardShuffleSound = pygame.mixer.Sound("sounds/cardShuffle.wav")
        # Win sound
        self.winnerSound = pygame.mixer.Sound("sounds/ding.wav")
        # Lost sound
        self.loserSound = pygame.mixer.Sound("sounds/loser.wav")     

        # Game resets
        self.reset()
        
    def draw(self): # draw image to screen.
        """Tell each card to draw an image of itself"""
        for oCard in self.cardList:
            oCard.draw()

        self.potScoreText.draw()
        self.messageText.draw()

    # Dealer 
    def setDealerPot(self, playersAndCards):
        """
        Appends object Cards to dealerPot list after a trick tie.
        Player obj is not appeneded back.
        """
        potCards = []

        for i in range(len(playersAndCards.copy())):
            dict = playersAndCards.pop(0)
            card = dict.pop('card')
            potCards.append(card)
        for oCard in potCards:
            self.dealerPot.append(oCard)
    
    def getDealerPot(self):
        """This method is used by setPot Transfer """
        return self.dealerPot
    
    def dealerPotTransfer(self, player=None):
        """The dealerPot gives all it's cards to the player's pot or to the deck."""

        if player != None: # Give cards to player
            dealerPot = self.getDealerPot.copy() # Itterate using a copy of the list
            for card in dealerPot:
                card = self.dealerPot.pop(0) # Remove items using real list
                player.setPot(card)

        else: # Return cards to deck
            dealerPot = self.getDealerPot.copy()
            for cardIndex in range(len(dealerPot)):
                card = self.dealerPot.pop(cardIndex)
                self.oDeck.returnCardToDeck(card)

    def trickWinner(self, playersAndCards):
        """Give trick winner the pot cards."""

        # Place the cards in a list
        potCards = [playersAndCards[0]['card'], playersAndCards[1]['card']]
        # Add cards into winning player's pot
        for card in potCards.copy():
            card = potCards.pop(0)
            # The trick winner is rearranged in the player list as 1st item
            self.playerList[0].setPot(card)
        
        if self.dealerPot: # If there are cards in the dealer list, give them all to player1
                self.dealerPotTransfer(self.playerList[0]) # Player has all the dealer cards in their pot

    # Trump
    def showTrumpCard(self, oCard):
        oCard.reveal()

    def setTrump(self, oCard):
        self.trumpCard = oCard

    # Pre-game
    def reset(self):
        """
        This method is called when a new round starts. 
        Resets: deck, pots, points
        """
        # Reset every Player's pot points
        for playerIndex in range(len(self.playerList.copy())): # playerList Iteration
            self.playerList[playerIndex].setPotScore(gameReset=True)

        # Remove any cards in every player's pot and put it back int the deck
        for playerIndex in range(len(self.playerList.copy())): # playerList Iteration
            playerPotLen = self.playerList[playerIndex].getPot()
            for cardIndex in range(len(playerPotLen)): # potCards iteration
                  oCard = self.playerList[playerIndex].removeCardFromPot(cardIndex) # Pop card object using the index
                  self.oDeck.returnCardToDeck(oCard, loc=Game.DECK_LOCATION) # oCard object is placed back in the deck

        # Remove any cards in dealer's pot and put it back int the deck
        if self.getDealerPot(): # is it true that there are cards?
            self.dealerPotTransfer()

        # Decide which player becomes turnPlayer when game resets
        self.highestCardWins()

        self.cardShuffleSound.play() # play shuffle sound
        self.oDeck.shuffle() # shuffle new deck

        # Pick a Trump card
        oCard = oDeck.getCard() 
        self.setTrump(oCard)
        # Trump location under the deck
        self.trumpCard.setLoc(Game.DECK_LOCATION)
        self.trumpCard.setRotate(90) # 90 degrees rotation
        # Reveal trump card
        self.showTrumpCard(self.trumpCard)  

        # Deck's location
        self.oDeck.setLoc(Game.DECK_LOCATION)
                
        # Deal cards to players before the game starts
        for i in range(Game.MAX_HAND): # Players draw up to 3 cards
                
            didTurnPlayerDraw = False # Tells none turn player to avoid drawing till turn player has drawn
            keepDrawing = True # Keep drawing till all players have drawn
            while keepDrawing:
                
                for playerIndex in range(len(self.playerList.copy())): 

                    # If player is turnPlayer draw!
                    if self.playerList[playerIndex].getTurnPlayer and not didTurnPlayerDraw:  
                        self.playerDrawsACard(playerIndex)
                        self.playerList[playerIndex].showHand() # Player can see their hand
                        didTurnPlayerDraw = True
                    
                    # player draw if turnPlayer drew first!
                    elif didTurnPlayerDraw: 
                        self.playerDrawsACard(playerIndex)
                        self.playerList[playerIndex].showHand()
                        keepDrawing = False # Exit while loop

                    # Set card coordinates for ghost 'player' hand 
                    # PLACE HOLDERS ARE EMPTY CARDS with a back image
                    # Ghost player remembers card's posX
                    currentGhostHand = self.ghostHandList.copy() # Get list
                    cardIndex = len(currentGhostHand) # How long is the list?
                    cardLocX = self.cardXPositionList[cardIndex] # Get x-coordinates
                    oGhostCard = Card() # Instantiate a card
                    # Set ghost player's card posX to the end of list
                    self.ghostHandList.append({'cardLocX': cardLocX, 'ghostCard': oGhostCard})
                    # Add coordinates to player's card                    
                    oGhostCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP) 

        # Start game
        self._briscaGame()

    def highestCardWins(self):
        """
        When players enter the game room the dealer gives each player a card.
        Player with the highest card value wins to be turnPlayer=True.
        Player's var turnPlayer is False by defult.
        """
        print('highestCardWin - Enter method')

        self.cardShuffleSound.play() # play shuffle sound
        self.oDeck.shuffle() # shuffle new deck
        
        tie = False
    
        if not tie: 
            # Place holder to identify to whom the card belongs too
            playersAndCards = []

            """-----------------WORKING ON THIS SECTION------------------------------"""
            # Each player draws one card each
            for playerIndex in range(len(self.playerList.copy())): # Pick player index
                self.playerDrawsACard(playerIndex)
                self.ghostDrawsACard(playerIndex)
            
            for playerIndex in range(len(self.playerList.copy())): # Pick player index
                oCard = self.playerList[playerIndex].selectCard() # player selects their card

                playersAndCards.append(
                    {'player': self.playerList[playerIndex], 
                     'card': oCard,
                     'Loc': oCard.getLoc()
                    }
                    )

            # Players compare the card's trickValue and decide who will be turn player   
            tie = self.compareCards(playersAndCards) # Returns and checks for tie

            # ----> use "playersAndCards" to figure out the cards to be removed
            # Example: {'player': oPlayer, 'card': oCard, 'Loc': (x, y)}
            # ----> Don't forget to update the cards posX in player!

            # Remove the 1st card from each player's hand and pass it back to deck
            for playerIndex in range(len(self.playerList.copy())): # Check every player
                # Remove card from player's hand
                oCard = self.playerList[playerIndex].removeCardFromHand(0) # Remove card
                self.oDeck.returnCardToDeck(oCard, loc=(600, 500)) # Card returns to deck concealed 

                # Work with the tie section too -------------------------------------
            """-----------------WORKING ON THIS SECTION------------------------------"""

        while tie:
            # Place holder to identify to whom the card belongs too
            playersAndCards = []

            # Each player draws one card each
            for playerIndex in range(len(self.playerList.copy())): # Pick player index
                self.playerDrawsACard(playerIndex)
                self.playerList[playerIndex].showHand()
                # Pause the game for 3 seconds
                playerCard = self.playerList[index].getHand()
                playersAndCards.append(
                    {'player': self.playerList[index], 'card': playerCard[0]}
                    )

            # Players compare the card's trickValue and decide who will be turn player   
            tie = self.compareCards(playersAndCards) # Returns and checks for tie

            # Remove the 1st card from each player's hand and pass back to deck
            for index in range(len(self.playerList.copy())):
                oCard = self.playerList[index].removeCardFromHand(0) # Remove card from player's hand
                self.oDeck.returnCardToDeck(oCard) # Card returns to deck

            # If true shuffle deck after cards return deck after
            if tie:
                self.oDeck.shuffle() 

        print('highestCardWin - exit method')

    def selectCard(self, event):
        """
        String based logic gates "Cancel", "Re-select" "Accept"
        Player will be asked to select a card from their hand.
        Once player clicks card they can 
            - Cancel card selection (stay in loop)
            - Re-select card (Currently in loop)
            - Accept card selection (exit loop) 
        """
        pass    

    def playerStatus():
        """
        After player selects a card,
        They will be asked to
            - Enter trick
            - Swap trump card
            - Quit game
        """
        pass

    def _briscaGame(self):
        """The logic of the game loop"""
        pass

    def playerDrawsACard(self, playerIndex):
        """Players draw a card and remembers card's posX."""
        # Player draws one card and sets card in their hand
        self.playerList[playerIndex].drawCard(self.oDeck)
        
        # Set coordinates for player card's X position
        currentPlayerHand = self.playerList[playerIndex].getHand() # Get list
        cardIndex = len(currentPlayerHand) # How long is the list?
        cardLocX = self.handPosXList[cardIndex] # Get the x-coordinates allowed by Game class

        # Tell card its location and show it to client
        self.playerList[playerIndex].setCardLoc(
            self, cardIndex, loc=(cardLocX, Game.PLAYER_HAND_CARDS_BOTTOM)
            )

    def ghostDrawsACard(self, playerIndex):
        """Players draw a card and remembers card's posX."""
        # Player draws one card and sets card in their hand
        oGhostCard = Card()
        self.ghostHandList.append(oGhostCard)
        
        # Set coordinates for ghost player card's X position
        currentPlayerHand = self.playerList[playerIndex].getHand() # Get list
        cardIndex = len(currentPlayerHand) # How long is the list?
        cardLocX = self.handPosXList[cardIndex] # Get the x-coordinates allowed by Game class

        # Tell card its location and show backside of card to client
        self.ghostHandList[cardIndex].setLoc(loc=(cardLocX, Game.GHOST_HAND_CARDS_TOP))

    def trumpHandSwap(self):
        """Swap one card in the player's hand for the trump card."""
        pass

    def trick(self, playersAndCards):
            """
            Players have chosen their cards for battle; now they fight for supremacy, but mostly points.
            If tie, cards are placed with the dealer pot; after a tie, which ever player wins the following trick
            obtains all the dealer pot cards, uuh nice!
            """
            # playersAndCards is a list nesing a dictionary with the players and their corresponding cards
            # E.g. playersAndCards = [{'player': oPlayer, 'card': oCard}]

            # Compare player's trump cards to the main trump card
            isPlayer1Trump = playersAndCards[0]['card'].getSuit() == self.trumpCard.getSuit()
            isPlayer2Trump = playersAndCards[1]['card'].getSuit() == self.trumpCard.getSuit()

            if isPlayer1Trump and isPlayer2Trump: # Both players have a trump card | No tie can HAPPEN!
                # Compares player's cards: the higest value card wins; turn player is selected and 
                self.compareCards(playersAndCards) # turn player is rearranged as 1st iteam in the playerList   

            elif isPlayer1Trump or isPlayer2Trump: # A player has a trump card | No tie can HAPPEN!
                if isPlayer1Trump:
                    # Player1 is turnPlayer, player 2 is false by defult
                    playersAndCards[0]['player'].setTurnPlayer(True) 
                    # Player arrangement decides who draws first
                    self.playerList = [playersAndCards[0]['player'], playersAndCards[1]['player']] 
                else:
                    # Player2 is turnPlayer, player 1 is false by defult
                    playersAndCards[1]['player'].setTurnPlayer(True) 
                    # Player arrangement decides who draws first
                    self.playerList = [playersAndCards[1]['player'], playersAndCards[0]['player']] 

            else: # No player has a trump card, a tie can happen using trickValues.
                tie = self.compareCards(playersAndCards)

                if tie: # Tie
                    # Give dealer your pot cards till tie is resolved
                    self.setDealerPot(playersAndCards) # Trick cards are in dealer's possetion 

                    while tie:
                        playersAndCards = [] # Parameter var is empty
                        # Players select another card from their hands
                        for player in self.playerList:
                            card = self.selectCard(player) 
                            playersAndCards.append({'player': player, 'card': card})

                        # Players compare cards and decide who will be turn player   
                        tie = self.compareCards(playersAndCards) # Check for tie

                        if tie: # Give dealer your pot cards till tie is resolved
                            self.setDealerPot(playersAndCards)
                        
                        else: # Not tie
                            print('Tie is False insde the while loop!')

                else: # Not tie
                    print('Not a tie out side the while loop.')
            
            # After one logic gate has a been checked the Winner gets the chicken dinner. 
            self.trickWinner(playersAndCards) 

    def compareCards(self, playersAndCards):
            """
            Sets a turnPlayer by comparing the highest value card.
            Arrange player list; winner is first item on playerList.
            Returns True or False for tie.
            """
            # playersAndCards is a list nesing a dictionary with the player's iD and corresponding cards
            # E.g. playersAndCards = [{'player: oPlayer, 'card': oCard}]

            player1CardValue = playersAndCards[0]['card'].getTrickValue()
            player2CardValue = playersAndCards[1]['card'].getTrickValue()
            playersAndCards[0]['card'].reveal()
            playersAndCards[1]['card'].reveal()

            if player1CardValue > player2CardValue:
                print("-------You WIN!")
                playersAndCards[0]['player'].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                self.playerList = [playersAndCards[0]['player'], playersAndCards[1]['player']] # Player arrangement decides who draws first
                tie = False
            
            elif player1CardValue < player2CardValue:
                print("-------You LOSE!")
                playersAndCards[1]['player'].setTurnPlayer(True) # Player1 is turnPlayer, player 2 is false by defult
                self.playerList = [playersAndCards[1]['player'], playersAndCards[0]['player']] # Player arrangement decides who draws first
                tie = False

            else: # If players end in a tie: cards return to deck
                print("Tie")
                tie = True

            return tie # Return the value of Tie

    

"""
Todo list: 
2) Re-check writen methods one more time for logoc consistency.
    *DID
    - Modified highestCardWins, creat compareCards method
    - Add comments in the reset() and arrange highestCardWins() in the reset method
    - Modify a lot of shit in the Game class between highestCardWins(), compareCards() and trick().
    - Clean trick() and fix logic
    - Check, fix and clean highestCardWin()
    - Check, fix and clean reset()
    - Add 'playerList' parameter to Game class init magic method. 
    - Add set and get HandPosX methods to Player class.
    - Write playerDrawsACard method in Game class. Work on the players drawn a card method
    - Check to see if players draw a card method can be used across the class to sub stitudes other code.
    - Create place holders for client's opponent

5) Look for 'WORKING ON THIS SECTION' to check what Iam doing!
6) Figure the other empty methods out.
7) If there is no deck, draw trump card.
8) Whatever needs to happen next lol!
9) Where ever a card moves to make sure to update card's image coordinates for player and ghost
"""