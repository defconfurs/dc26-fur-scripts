"""Seizure"""

import dcfurs
import random

class seizure:
  interval = 10
  value = 8 
  ticks_per_sec = int(1000 / interval)

  values = [0, 1, 24, 40, 56, 72, 88, 104, 120, 136, 152, 168, 184, 200, 216, 232, 248]

  def __init__(self):
    self.reset_fbuf()
    self.next_blink = random.randint(self.ticks_per_sec * 10, self.ticks_per_sec * 20)

  def reset_fbuf(self):
    self.fbuf = [bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18),bytearray(18)]

  def face(self):
    self.reset_fbuf()
    for y in range(0, 7):
      for x in range(0, 18):
        self.onPixel(y, x)
    n = random.randint(-5, 5)
    self.value += n
    if self.value < 0:
      self.value = 0
    elif self.value >= len(self.values) - 1:
      self.value = len(self.values) - 1

  def onPixel(self,y,x):
    self.fbuf[y][x] = self.values[self.value]

  def redrawDisplay(self):
    for y in range(0,len(self.fbuf)):
      row = self.fbuf[y]
      for x in range(0, len(row)):
        dcfurs.set_pixel(x, y, row[x])

  def draw(self):
    self.face()
    self.redrawDisplay()
