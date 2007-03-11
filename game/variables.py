#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Define variables and constants used all over in the game."""

import os, sys

import pygame
from pygame.locals import *

GRAVITY = 0.25 # Move to level files?

# Change working directory so that the paths work correctly
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

DIR_GRAPH = os.path.abspath(os.path.join("data", "graphic"))
DIR_SOUND = os.path.abspath(os.path.join("data", "sound"))
DIR_MUSIC = os.path.abspath(os.path.join("data", "music"))
DIR_FONT = os.path.abspath(os.path.join("data", "font"))
DIR_LEVELS = os.path.abspath("levels")

# Used in game initiation. May be removed later
CAPTION = "PyDuel"
RESOLUTION = RES_WIDTH, RES_HEIGHT = (640, 480)
ICON = None # No icon right now

UP, RIGHT, DOWN, LEFT = range(4) # Directions

loadImg = lambda path: pygame.image.load(os.path.join(DIR_GRAPH, path)).convert()
loadImgPng = lambda path: pygame.image.load(os.path.join(DIR_GRAPH, path)).convert_alpha()

def loadImageFrames(filename, frameWidth, frameHeight, ammount, flip=False):
   """Takes a image containing ammount of frames in one row and returns a list of subsurfaces devided by frameWidth/Height, if flip is true it includes Horizontally flipped frames. the order of the flipped ones is inverted. """
   images = []
   images.append(loadImgPng(filename))
   if flip == True:
      images.append(pygame.transform.flip(loadImgPng(filename), True, False))
   frames = []
   for image in images:
      for i in range(ammount):
         rect = pygame.rect.Rect(i*frameWidth, 0, frameWidth, frameHeight)
         frame = image.subsurface(rect)
         frames.append(frame)

   return frames     
