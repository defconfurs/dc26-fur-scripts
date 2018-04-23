"""Kanye Glasses"""

import dcfurs
import random

class kanye:
  interval = 300
  ticks_per_sec = int(1000 / interval)
  kanye = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[0,15],[0,16],[2,0],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11],[2,12],[2,13],[2,14],[2,15],[2,16],[2,17],[4,0],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[4,7],[4,8],[4,9],[4,10],[4,11],[4,12],[4,13],[4,14],[4,15],[4,16],[4,17],[6,1],[6,2],[6,3],[6,4],[6,5],[6,12],[6,13],[6,14],[6,15],[6,16]]

  def __init__(self):
    self.reset_fbuf()
    self.next_blink = random.randint(self.ticks_per_sec * 10, self.ticks_per_sec * 20)

  def reset_fbuf(self):
    self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]

  def face(self):
    faceBuf = self.kanye
    self.reset_fbuf()
    for xy in range(0,len(faceBuf)):
      self.onPixel(faceBuf[xy][0],faceBuf[xy][1])

  def onPixel(self,y,x):
    self.fbuf[y][x] = 255

  def redrawDisplay(self):
    for y in range(0,len(self.fbuf)):
      row = self.fbuf[y]
      for x in range(0, len(row)):
        dcfurs.set_pixel(x, y, row[x])

  def draw(self):
    self.face()
    self.redrawDisplay()
