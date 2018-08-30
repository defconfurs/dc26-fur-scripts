print('Loading fonts\__init__.py...')

import gc
from os import listdir
from settings import emotefont, scrollfont

# Load all fonts from directory
fontdict = {}
for filename in listdir(__name__):
    if filename[:2] != '__' and filename[-3:] == '.py':
        classname = filename[:-3]
        if classname in [emotefont, scrollfont]:
            handle = __import__(__name__ + '.' + classname, globals(), locals(), ['font'], 0)
            # Build dictionary of font names and their respective dictionaries.
            fontdict[classname] = handle.font
            del handle
            print('  ' + classname + ' font loaded')
        else:
            print('  ' + classname + ' font not in use, skipped')
del classname, listdir, filename
gc.collect()
