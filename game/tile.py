#!/usr/bin/env python
# -*- coding: utf-8 -*-

from variables import *

import pygame
from pygame.locals import *

class SurroundingTiles(object):
   """Help class. Holds variables for surrounding (and center) tiles."""
   
   def __init__(self, rect, scene):
      self.forRect = rect
      self.getFunc = scene.level.get # Function used to fetch tiles
      self.setCenter()
      self.setSides()
      self.setCorners()
      
   def setCenter(self):
      rect = self.forRect
      self.center = self.getFunc((rect.centerx, rect.centery))
      
   def setSides(self):
      rect = self.forRect
      self.left = self.getFunc((rect.left, rect.centery))
      self.right = self.getFunc((rect.right, rect.centery))
      self.top = self.getFunc((rect.centerx, rect.top))
      self.bottom = self.getFunc((rect.centerx, rect.bottom))
      
   def getSides(self):
      return (self.top, self.right, self.bottom, self.left) # Return in clockwise order
   
   def setCorners(self):
      rect = self.forRect
      self.topLeft = self.getFunc((rect.left, rect.top))
      self.topRight = self.getFunc((rect.right, rect.top))
      self.bottomLeft = self.getFunc((rect.left, rect.bottom))
      self.bottomRight = self.getFunc((rect.right, rect.bottom))
   
   def getCorners(self):
      # Return in clockwise order, starting with topleft (maybe should be topright)
      return (self.topLeft, self.topRight, self.bottomRight, self.bottomLeft)

class Tile(pygame.sprite.Sprite):
   """Generic tile class. Don't use this directly, inherit from this one.
   
   If you're making a tile for the "normal" layer, inherit from NormalTile instead.
   """

   WIDTH, HEIGHT = (20, 20) # Width and height of tiles

   # Tile defaults. Refers to index in tiles array
   default = 0
   ladderDefault = 11
   itemDefault = 12

   # Available tiles.
   # Format: (classname's prefix, dict with arguments passed to class)
   tiles = [("None", {}),
            ("Normal", {"image": "tile-ground-middle.png"}),
            ("Normal", {"image": "tile-ground-left.png"}),
            ("Normal", {"image": "tile-ground-right.png"}),
            ("Normal", {"image": "tile-ground-bottom.png"}),
            ("Background", {"image": "tile-tree-bottom.png"}),
            ("Background", {"image": "tile-tree-top.png"}),
            ("Background", {"image": "tile-bush.png"}),
            ("Cloud", {"image": "tile-ground-cloud-middle.png"}),
            ("Cloud", {"image": "tile-ground-cloud-left.png"}),
            ("Cloud", {"image": "tile-ground-cloud-right.png"}),
            ("Ladder", {"image": "tile-ladder.png"}),
            ("HealthItem", {"image": "tile-item-health.png"}),
            ("AmmoItem", {"image": "tile-item-ammo.png"})]
   
   def __init__(self, level, cords, image, *args):
      pygame.sprite.Sprite.__init__(self)
      
      self.level = level # The level the tile is in
      self.image = loadImgPng(os.path.join(self.level.theme, image)) # Lazy loading of images
      self.newPos(cords)
   
   def newPos(self, cords):
      """Change position of tile in map. Column and row position. Also sets self.rect"""
      self.col, self.row = cords
      self.rect = pygame.Rect(Tile.WIDTH*self.col, Tile.HEIGHT*self.row, Tile.WIDTH, Tile.HEIGHT)

class NormalTile(Tile):
   """The normal (ground) tile. Is not walkable by default.
   
   Inherit from this tile if you're using the tile in the "normal" layer.
   """
   
   def __init__(self, level, cords, image):
      Tile.__init__(self, level, cords, image)
      
      self.isWalkable = False
      self.isCloud = False
      # Child tiles
      self.ladder = None
      self.item = None

class NoneTile(NormalTile):
   """The none tile have no image and is walkable. Used in places where there isn't any other tile."""
   
   def __init__(self, level, cords):
      pygame.sprite.Sprite.__init__(self) # Don't use NormalTile.__init__() because it loads an image.
      
      # Have to set some vars manually
      self.level = level
      self.image = None
      self.newPos(cords)
      self.isWalkable = True
      self.isCloud = False
      self.ladder = None
      self.item = None

class BackgroundTile(NormalTile):
   """The background tiles have an image, but are walkable."""

   def __init__(self, level, cords, image):
      NormalTile.__init__(self, level, cords, image)
      
      self.isWalkable = True

class CloudTile(NormalTile):
   """Cloud tiles can be entered from any direction, except from the top."""
   
   def __init__(self, level, cords, image):
      NormalTile.__init__(self, level, cords, image)
      
      self.isWalkable = True
      self.isCloud = True
      
class LadderTile(Tile): # Ladder tiles is not in "normal" layer, so inherit from Tile
   """Ladder tiles can be climbed on."""
   
   def __init__(self, level, cords, image):
      Tile.__init__(self, level, cords, image)

class ItemTile(Tile):
   """Item tile's can be health, points and other items the player can pick up.
   
   Inherit from this one, and define the walkedOn() method.
   """
   
   def __init__(self, level, cords, image):
      Tile.__init__(self, level, cords, image)
   
   def walkedOn(self, player):
      """Called when player walks on item"""
      self.removeFromLevel() # By default just remove
      return True
      
   def removeFromLevel(self):
      # so classes that inherits don't have to define
      # however they can override this method, or skip to call it
      
      self.level.get((self.col, self.row), True).item = None # Remove from it's parent tile
      self.kill() # remove from all groups
      
class HealthItemTile(ItemTile):

   HEALTH = 25

   def __init__(self, level, cords, image):
      ItemTile.__init__(self, level, cords, image)
   
   def walkedOn(self, player):
      if player.health >= MAX_HEALTH: return False # only pick up, if health is not full
      self.removeFromLevel()
      player.health = min(HealthItemTile.HEALTH + player.health, MAX_HEALTH) # MAX if new health > MAX
      return True
      
class AmmoItemTile(ItemTile):

   AMMO = 20

   def __init__(self, level, cords, image):
      ItemTile.__init__(self, level, cords, image)
   
   def walkedOn(self, player):
      if player.weapon.ammo >= player.weapon.MAX_AMMO: return False # only pick up, if ammo is not full
      self.removeFromLevel()
      player.weapon.ammo = min(AmmoItemTile.AMMO + player.weapon.ammo, player.weapon.maxAmmo) # MAX if new ammo > MAX
      return True
