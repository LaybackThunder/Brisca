# Brisca - pygame version
# Main program

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
from Player import *
from PlayerAi import *
from Game import *

# 2 - Define constants
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 680
FRAMES_PER_SECOND = 30 

# 3 - Initialize the world
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
background = pygwidgets.Image(window, (0, 0),
                                'images/background.jpg')

newGameButton = pygwidgets.TextButton(window, (880, 630),
                                    'New Game', width=100, height=45)

quitButton = pygwidgets.TextButton(window, (990, 630),
                                    'Quit', width=100, height=45)

# ---------------------------------------------------------------------------

# 5 - Initialize variables
oAiPlayer = PlayerAi(window, isTurnPlayer=False, isPlayerHuman=False)
oPlayer = Player(window, isTurnPlayer=True, isPlayerHuman=True) 
oPlayers = [oPlayer, oAiPlayer]
oGame = Game(window, oPlayers)

# ---------------------------------------------------------------------------
# 6 - Loop forever 
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Quit Event
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()
        
        # Check for new game
        if newGameButton.handleEvent(event):
            oAiPlayer = PlayerAi(window, isTurnPlayer=False, isPlayerHuman=False)
            oPlayer = Player(window, isTurnPlayer=True, isPlayerHuman=True)
            oPlayers = [oPlayer, oAiPlayer]
            oGame = Game(window, oPlayers)
        
        # Check events to play game
        oGame.handleEvent(event)

    # 8 - Do any "per frame" actions
    oGame._updateUI()

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw the window elements
    newGameButton.draw()
    quitButton.draw()
    oGame.draw() # Draw Game elements

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)