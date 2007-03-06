#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from engine import Game, Scene
from level import LevelLoader
from player import Player
from variables import *

import pygame
from pygame.locals import *

class Duel(Scene):
   """The main game scene. Where the players fight against eachother."""
   
   def __init__(self, game):
      Scene.__init__(self, game)
      
      playerOne = Player(loadImgPng("red.png"), (K_a, K_d, K_w, K_s))
      playerTwo = Player(loadImgPng("blue.png"), (K_LEFT, K_RIGHT, K_UP, K_DOWN))
      
      self.players = pygame.sprite.Group(playerTwo, playerOne)
      self.levelLoader = LevelLoader()
      self.loadLevel(1) # First level
   
   def loadLevel(self, levelNumber):
      self.levelNumber = levelNumber
      index = self.levelNumber-1 # index in list is minus one
      self.level = self.levelLoader.load(self.levelLoader.__class__.levels[index]) # use level list from level loader's class
   
   def event(self, event):
      pass

   def loop(self):
      pygame.event.pump()
      keyInput = pygame.key.get_pressed()
      self.players.update(keyInput, self.level)
   
   def update(self):
      self.players.clear(self.game.screen, self.background)
      self.players.draw(self.game.screen)
        
   def draw(self):
      self.level.draw(self.game.screen)
      self.players.draw(self.game.screen)

def main():
   # Change working directory so that the paths work correctly
   os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
   
   pyduel = Game(RESOLUTION, CAPTION, ICON)
   firstScene = Duel(pyduel)
   pyduel.start(firstScene) # Start the game with a new Duel scene
   raise SystemExit, 0

if __name__ == "__main__":
   main()
