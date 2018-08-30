import dcfurs
import fonts
from settings import emotefont
from random import choice

## Some canned emotes that you might find interesting.
def awoo():
    dcfurs.set_row(0, 0x11226)
    dcfurs.set_row(1, 0x2aa29)
    dcfurs.set_row(2, 0x2aaa9)
    dcfurs.set_row(3, 0x1114f)
    dcfurs.set_row(4, 0x00009)
    dcfurs.set_row(5, 0x00009)
    dcfurs.set_row(6, 0x00000)

def beep():
    dcfurs.set_row(0, 0x0e6ce)
    dcfurs.set_row(1, 0x12b52)
    dcfurs.set_row(2, 0x126d2)
    dcfurs.set_row(3, 0x0e24e)
    dcfurs.set_row(4, 0x026d2)
    dcfurs.set_row(5, 0x02012)
    dcfurs.set_row(6, 0x0200e)

def boop():
    dcfurs.set_row(0, 0x0e48e)
    dcfurs.set_row(1, 0x12b52)
    dcfurs.set_row(2, 0x12b52)
    dcfurs.set_row(3, 0x0eb4e)
    dcfurs.set_row(4, 0x02492)
    dcfurs.set_row(5, 0x02012)
    dcfurs.set_row(6, 0x0200e)

def derp():
    dcfurs.set_row(0, 0x1d18e)
    dcfurs.set_row(1, 0x26a52)
    dcfurs.set_row(2, 0x24bd2)
    dcfurs.set_row(3, 0x1c852)
    dcfurs.set_row(4, 0x04b92)
    dcfurs.set_row(5, 0x04012)
    dcfurs.set_row(6, 0x0400e)

def owo():
    dcfurs.set_row(0, 0x1c00e)
    dcfurs.set_row(1, 0x22011)
    dcfurs.set_row(2, 0x22851)
    dcfurs.set_row(3, 0x22b51)
    dcfurs.set_row(4, 0x22491)
    dcfurs.set_row(5, 0x22011)
    dcfurs.set_row(6, 0x1c00e)

## Render an emote from an ascii string
def render(str):
    ## Check for special cases
    if str == 'awoo':
        awoo()
        return
    if str == 'beep':
        beep()
        return
    if str == 'boop':
        boop()
        return
    if str == 'derp':
        derp()
        return
    if str == 'owo':
        owo()
        return

    ## Otherwise, generate from our character set.
    font = fonts.fontdict[emotefont]
    lbits = font[str[0]]
    rbits = font[str[-1]]
    dcfurs.clear()

    ## Draw the left character.
    column = int((8 - len(lbits))/2)
    for colbits in lbits:
        for y in range(0, dcfurs.nrows):
            if (colbits & (1 << y)) != 0:
                dcfurs.set_pixel(column, y, 0xff)
        column = column + 1

    ## Draw the right character.
    column = int((28 - len(rbits) + 1)/2)
    for colbits in rbits:
        for y in range(0, dcfurs.nrows):
            if (colbits & (1 << y)) != 0:
                dcfurs.set_pixel(column,y,0xff)
        column = column + 1

prebuilt = [
    owo,
    "\./",
    "X.X",
    "-.-",
    '"."',
    "C.C",
    "?.?",
    "#.#",
    "@.@",
    "!.!",
    "~.^",
    "o.o",
    "O.o",
    "O.O",
    ">.<",
    "=.=",
    "9.9",
    ## c.c
    [0x00000, 0x00000, 0x0f03c, 0x01020, 0x01020, 0, 0],
    ## \\.\\
    [0x00000, 0x00000, 0x0a00a, 0x0a00a, 0x14014, 0x14014, 0],
    ## ` . `
    [0x00000, 0x10002, 0x08004, 0, 0, 0, 0],
    ## u.u
    [0x00000, 0x00000, 0x00000, 0x11022, 0x1f03e, 0, 0],
]

## Draw a random emote from prebuilt[]
def random():
    x = choice(prebuilt)
    if type(x) is str:
        render(x)
    elif callable(x):
        x()
    else:
        dcfurs.set_frame(x)
