import pygwidgets
from Deck import *
from Card import *
from Player import *

class Game():
    # Class Variables
    HAND_CARD_OFFSET = 20 # player's cards buffer between each other
    PLAYER2_HAND_CARDS_TOP = 400 # Y coordinate
    PLAYER1_HAND_CARDS_BOTTOM = 100 # Y coordinate
    CARDS_LEFT = 75 # X coordinate
    DISPLAY_STARTING_HANDS = 3
    MAX_HAND = 3
    
    def __init__(self, window):
        """Initisialize attributes."""
        self.window = window
        self.oDeck = Deck(self.window)
        self.oPlayer1 = Player(1)
        self.oPlayer2 = Player(0)
        self.playerList = [self.oPlayer1, self.oPlayer2]
        self.potScore = 0
        self.potScoreText = pygwidgets.DisplayText(window, (450, 164),
                                        f'Pot Score: {self.potScore}',
                                        fontSize=36, textColor=(255, 255, 255))
        
        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                        f'', width=900, justified='center'
                                        fontSize=36, textColor=(255, 255, 255))
        
        # Sounds go here
            # Card shuffle
            # Win sound
            # Lost sound
        
        # Calculating Players card positions within the player's hand
        self.cardXPositionList = []
        thisLeft = Game.CARDS_LEFT # Starting card to the left of hand

        # Calculate the x positions of all cards, once 
        for cardNum in range(Game.DISPLAY_STARTING_HANDS): # 3 cards
            self.cardXPositionList.append(thisLeft)
            thisLeft += Game.HAND_CARD_OFFSET 
        # Both players can share X position
        self.player1CardXPositionList = self.cardXPositionList.copy()
        self.player2CardXPositionList = self.cardXPositionList.copy()
        
        # Game decides who goes first at random before game starts
        self.highestCardWinds()
        
    def reset(self):
        """This method is called when a new round starts"""
        # play shuffle sound
        oDeck.shuffle() # shuffle deck
        
        # deal cards to players
        for oPlayer in self.playerList: # LEFT OFF ----> Check how cards are delt toplayers

            # take one card from deck
            oCard = self.oDeck.getCard()

            # set card coordinates per player hand location is...
            if oPlayer.getTurnPlayer:  # If player is turnPlayer do or die!
                oPlayer.setHand(oCard) # Set card in oPlayer's hand
                if oPlayer.getPlayerId() == 0: # Set card coordinates for oPlayer1
                    cardLocX = self.player1CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM)
                else:                          # Set card coordinates for oPlayer2
                    cardLocX = self.player2CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)
            else:                      # If player is not turnPlayer you be gug2go!
                oPlayer.setHand(oCard)
                if oPlayer.getPlayerId() == 0:
                    cardLocX = self.player1CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER1_HAND_CARDS_BOTTOM)
                else:
                    cardLocX = self.player2CardXPositionList.pop(0)
                    oCard.setLoc(cardLocX, Game.PLAYER2_HAND_CARDS_TOP)

        # show player card
        # hide player2 cards
    
    def highestCardWinds(self):
        # highestCardWins method
            # Loop player list
                # player draws
            # Do all players have a card?
                # False:
                    # Loop till all players have one card each
                # True:
                    # Players compare cards
                        # If one is greater than the other
                            # Greater player is turnPlayer
                            # Card returns to deck

                        # else: its a tie, tie is set to True
                        # Card returns to deck
                        # Shuffle deck
                    # While tie
                        # Loop player list
                            # player draws
                        # Do all players have a card?
                            # False:
                                # Loop till all players have one card each
                            # True:
                                # Players compare cards
                                    # If one is greater than the other
                                        # Greater player is turnPlayer
                                        # tie is set to false
                        # if tie == False:
                            # break 
                    # Cards return to deck
        self.reset()# start a round of the game
        pass