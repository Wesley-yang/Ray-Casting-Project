import pygame
import sys, os

from States import level_select
from States import menu
from States import gameplay
from States import pause
from States import level_complete
from States import highscore_menu


class StateController:

    def __init__(self):
        pygame.init()
        self.screenWidth = 500
        self.screenHeight = 500
        self.screen = pygame.display.set_mode((self.screenWidth,self.screenHeight))

        self.quit = False
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.stateDict = {"menu": menu.Menu(self.screen),
                          "level select":level_select.LevelSelect(self.screen),
                          "gameplay": gameplay.Gameplay(self.screen),
                          "level complete":level_complete.LevelCompleteMenu(self.screen),
                          "pause":pause.Pause(self.screen),
                          "highscore menu":highscore_menu.HighscoreMenu(self.screen)}
        self.activeState = self.stateDict["menu"]
        self.persistentVar = {"restart": True, "levelNum": 1}
        self.activeState.startup(self.persistentVar)

    def gameloop(self):
        """
        the main loop for the game, most of the game's runtime will be spent in here
        Calls the aciveState's getEvent (for event handling)
        Calls the activeSate's update   (for game logic)
        Calls the aciveState's draw     (to draw everything to the screen)
        """
        while not self.quit:
            dt = self.clock.tick(self.FPS)
            nextState = self.stateDict[self.activeState.nextState]
            if self.activeState == nextState:  # if the activeState is unchanged
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.activeState.exit()
                        self.quit = True
                    self.activeState.getEvent(event)
                self.activeState.update(dt)
                self.activeState.draw()

                pygame.display.update()
            else: # if the activeState needs to be changed
                self.persistentVar = self.activeState.exit()
                self.activeState = nextState
                self.activeState.startup(self.persistentVar)


A = StateController()
A.gameloop()
