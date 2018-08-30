print('Loading animations\__init__.py...')

import gc
from os import listdir
import sys
import ujson
import dcfurs

## Dynamically import all the python files we can find.
for filename in listdir(__name__):
    if filename[:2] != '__' and filename[-3:] == '.py':
        classname = filename[:-3]
        __import__(__name__ + '.' + classname, globals(), locals(), [classname], 0)
        print('  ' + classname + ' Python animation loaded')
del classname, filename
gc.collect()

## Template class for JSON-encoded animations.
class __jsonanim__:
    def __init__(self):
        fh = open(self.path, 'r')
        self.framenum = 0
        self.js = ujson.load(fh)
        self.intensity = bytearray([0, 2, 3, 4, 6, 9, 12, 17, 24, 34, 47, 66, 92, 130, 182, 255])
        fh.close()
        self.draw()

    def drawframe(self, frame):
        self.interval = int(frame['interval'])
        x = 0
        y = 0
        for ch in frame['frame']:
            if ch == ':':
                x = 0
                y = y + 1
            else:
                dcfurs.set_pixel(x, y, self.intensity[int(ch, 16)])
                x = x + 1

    def draw(self):
        self.drawframe(self.js[self.framenum])
        self.framenum = (self.framenum + 1) % len(self.js)

## Dynamically load and generate animation classes from JSON files.
for filename in listdir(__name__):
    if filename[:2] != "__" and filename[-5:] == ".json":
        classname = filename[:-5]
        globals()[classname] = type(classname, (__jsonanim__,), {'path', '/flash/animations/' + filename})
        print('  ' + classname + ' JSON animation loaded')
del filename, classname, listdir

## Return a list of all animation classes.
def all():
    results = []
    package = sys.modules[__name__]
    for name in dir(package):
        if name[:2] != "__" and name != 'all':
            module = getattr(package, name)
            if isinstance(module, type):
                results.append(module)
            elif name in dir(module) is not None:
                results.append(getattr(module, name))
    return results
