import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghost import Ghost

class GameController(object):

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
    
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
    
    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.pellets = PelletGroup("maze1.txt")
        self.ghost = Ghost(self.nodes.getStartTempNode(), self.pacman)
    
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()
    
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
    
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()