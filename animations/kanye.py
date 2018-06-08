"""Kanye Glasses"""

import dcfurs
import random

class kanye:
  interval = 300
  kanye = [0x3ffff, 0, 0x3ffff, 0, 0x3ffff, 0, 0x3ffff]

  def draw(self):
    dcfurs.set_frame(self.kanye)
