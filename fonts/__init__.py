print('Loading fonts\__init__.py...')

import os

fontdict = dict()
for module in os.listdir(__name__):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    handle = __import__(__name__ + '.' + module[:-3], globals(), locals(), ['font'], 0)
    fontdict[module[:-3]] = handle.font
    print('  ' + module[:-3] + ' font loaded')
del handle, module, os
