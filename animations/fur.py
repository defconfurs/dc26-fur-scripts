"""Furry Face Simulator 
Features:
  * Will randomly blink every 10 - 20 seconds if no large-scale movements happen
  * Will track eyes with small nudges in up / down, left / right tilts
  * Will wink left/right if tilted too far
  * Will close eyes if held upside down
"""

import dcfurs
import badge
import random

class fur:
  interval = 45 
  ticks_per_sec = int(1000 / interval)
  pupils = [[3,2],[3,15]]
  standardFace = [[0,1],[0,2],[0,3],[0,14],[0,15],[0,16],[1,0],[1,4],[1,13],[1,17],[2,0],[2,4],[2,6],[2,11],[2,13],[2,17],[3,0],[3,4],[3,6],[3,8],[3,9],[3,11],[3,13],[3,17],[4,0],[4,4],[4,7],[4,10],[4,13],[4,17],[5,0],[5,4],[5,13],[5,17],[6,1],[6,2],[6,3],[6,14],[6,15],[6,16]]
  blinkFace = [[2,1],[2,2],[2,3],[2,6],[2,11],[2,14],[2,15],[2,16],[3,0],[3,4],[3,6],[3,8],[3,9],[3,11],[3,13],[3,17],[4,0],[4,7],[4,10]]
  winkleftFace = [[0,14],[0,15],[0,16],[1,13],[1,17],[2,1],[2,2],[2,3],[2,6],[2,11],[2,13],[2,17],[3,0],[3,4],[3,6],[3,8],[3,9],[3,11],[3,13],[3,17],[4,7],[4,10],[4,13],[4,17],[5,13],[5,17],[6,14],[6,15],[6,16]]
  winkrightFace = [[0,1],[0,2],[0,3],[1,0],[1,4],[2,0],[2,4],[2,6],[2,11],[2,14],[2,15],[2,16],[3,0],[3,4],[3,6],[3,8],[3,9],[3,11],[3,13],[3,17],[4,0],[4,4],[4,7],[4,10],[5,0],[5,4],[6,1],[6,2],[6,3]]
  last_blink = 0
  next_blink = 0
  stop_blink = 0

  def __init__(self):
    self.reset_fbuf()
    self.counter = 0
    self.next_blink = random.randint(self.ticks_per_sec * 10, self.ticks_per_sec * 20)

  def reset_fbuf(self):
    self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]

  def face(self):
    faceBuf = self.standardFace
    (tx, ty, tz) = badge.imu.filtered_xyz()
    self.reset_fbuf()
    if ty < -32:
      faceBuf = self.winkrightFace
      self.last_blink = 0
    elif ty > 32:
      faceBuf = self.winkleftFace
      self.last_blink = 0
    elif tx < -64:
      faceBuf = self.blinkFace
      self.last_blink = 0
    elif self.stop_blink > 0:
      self.stop_blink -= 1
      faceBuf = self.blinkFace
    elif self.last_blink > self.next_blink:
      faceBuf = self.blinkFace
      self.last_blink = 0
      self.stop_blink = random.randint(int(self.ticks_per_sec * .2), int(self.ticks_per_sec * .45))
      self.next_blink = random.randint(int(self.ticks_per_sec * 10), int(self.ticks_per_sec * 20))
    else:
      for xy in range(0,len(self.pupils)):
        move_y = 0
        move_x = 0
        if ty < -8:
          move_y = -1
        elif ty > 8:
          move_y = 1
        if tz < -8:
          move_x = 1
        elif tz > 8:
          move_x = -1
        self.onPixel(self.pupils[xy][0] + move_x, self.pupils[xy][1] + move_y)
    for xy in range(0,len(faceBuf)):
      self.onPixel(faceBuf[xy][0],faceBuf[xy][1])
    self.last_blink += 1

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
