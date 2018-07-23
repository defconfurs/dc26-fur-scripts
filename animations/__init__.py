
from animations.scroll import scroll
from animations.fur import fur
from animations.kanye import kanye
from animations.dos import dos
from animations.worm import worm
from animations.rain import rain
from animations.cylon import cylon
from animations.emotes import emotes
from animations.life import life
from animations.pong import pong
from animations.maze import maze

## Dynamically import all the python files we can find.
#import os
#files = os.listdir("/flash/animations")
#for filename in files:
#    if filename[:2] != "__" and filename[-3:] == ".py":
#        classname = filename[:-3]
#        print(classname)
#        x = __import__("animations." + classname, globals(), locals(), [classname], 0)
#        globals()[classname] = getattr(x, classname)

## Generate a list of all animation classes
import sys
def all():
    results = []
    module = sys.modules['animations']
    for name in dir(module):
        x = getattr(module, name)
        if isinstance(x, type) and name[:2] != "__":
            results.append(x)
    return results

## Convert a string-encoded frame into a bytearray suitable for rendering.
def str2frame(str):
    fbuf = []
    for row in str.split(':'):
        fbrow = bytearray(len(row))
        for x in range(len(row)):
            ch = row[x]
            fbrow[x] = int(ch, 16) << 4
        fbuf.append(fbrow)
    return fbuf

## Wrapper class for JSON-encoded animations
import dcfurs
import ujson
import os
class __jsonanim__:
    def __init__(self):
        fh = open(self.path, "r")
        self.framenum = 0
        self.js = ujson.load(fh)
        fh.close()
        self.draw()

    def drawframe(self, frame):
        self.interval = int(frame['interval'])
        y = 0
        for row in frame['frame'].split(':'):
            buf = bytearray(len(row))
            for x in range(len(row)):
               buf[x] = int(row[x], 16) << 4
            dcfurs.set_row(y, buf)
            y = y+1

    def draw(self):
        self.drawframe(self.js[self.framenum])
        self.framenum = (self.framenum + 1) % len(self.js)

## Dynamically generate animation classes from JSON files.
files = os.listdir("/flash/animations")
for filename in files:
    if filename[:2] != "__" and filename[-5:] == ".json":
        classname = filename[:-3]
        globals()[classname] = type(classname, (__jsonanim__,), {'path', "/flash/animations/" + filename})

## Generate a list of all animation classes
import sys
def all():
    results = []
    module = sys.modules['animations']
    for name in dir(module):
        x = getattr(module, name)
        if isinstance(x, type) and name[:2] != "__":
            results.append(x)
    return results
