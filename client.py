# Brisca - pygame version
# Main program

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
from Game import *

# 2 - Define constants
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 900
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



# 4 - Load assets: image(s), sounds,  etc.
background = pygwidgets.Image(window, (0, 0),
                            'images/background.jpg')
newGameButton = pygwidgets.TextButton(window, (20, 840),
                            'New Game', width=100, height=45)

trickButton = pygwidgets.TextButton(window, (130, 840),
                            'Play trick', width=100, height=45)

quitButton = pygwidgets.TextButton(window, (970, 840),
                            'Quit', width=100, height=45)
trickButton.disable()

# 5 - Initialize variables
oPlayer = Player(window)
playerList = [oPlayer]
oGame = Game(window, playerList)
clickedCard = None


# 6 - Loop forever 
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()

        # Check for new game
        if newGameButton.handleEvent(event):
            oGame.reset()
            trickButton.disable()

        # Check the status of the player's cards
        playerList = oGame.getPlayers()
        for player in playerList:
            oCards = player.getHand()

            # Check if player has clicked or de_clicked any of their cards
            for oCard in oCards: 
                isCardClicked = oCard.handleEvent(event)

                if isCardClicked:
                    # You can battle
                    trickButton.enable()
                    clickedCard = oCard
                elif isCardClicked == False:
                    trickButton.disable()
                    clickedCard = None

        if trickButton.handleEvent(event): # If clicked when enabled
            print("Button click")
            clickedCard.disable() # Playe cannot click card anymore
            oGame.battleGroundLocation(oCard=clickedCard) # Sets card in the middle

            # Check that both players have cards ready to battle
                # If battle ready has two items; enter trick
                    # trick

    # 8 - Do any "per frame" actions

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw the window elements
    # Tell the game to draw itself
    oGame.draw()
    # Draw remaining user interface components
    newGameButton.draw()
    trickButton.draw()
    quitButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)
