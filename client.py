# Brisca - pygame version
# Main program

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import pygwidgets
from Game import *

# 2 - Define constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.
background = pygwidgets.Image(window, (0, 0),
                            'images/background.jpg')
newGameButton = pygwidgets.TextButton(window, (20, 530),
                            'New Game', width=100, height=45)
quitButton = pygwidgets.TextButton(window, (600, 530),
                            'Quit', width=100, height=45)

# 5 - Initialize variables
oPlayer = Player(window)
playerList = [oPlayer, oPlayer]
oGame = Game(window, playerList)

# 6 - Loop forever 
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()

        if newGameButton.handleEvent(event):
            oGame.reset()
            playerList = oGame.highestCardWins(event, playerList)

    # 8 - Do any "per frame" actions

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw the window elements
    # Tell the game to draw itself
    oGame.draw()
    # Draw remaining user interface components
    newGameButton.draw()
    quitButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)
