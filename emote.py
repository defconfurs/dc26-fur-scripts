## Some canned emotes that you might find interesting.
import dcfurs
from random import choice

## Tall font for emotes
font7bit = {
    '0':bytearray([0x1c,0x22,0x22,0x1c]),
    '1':bytearray([0x42,0x7f,0x40]),
    '2':bytearray([0x62,0x51,0x49,0x46]),
    '3':bytearray([0x22,0x41,0x49,0x36]),
    '5':bytearray([0x23,0x45,0x49,0x31]),
    '6':bytearray([0x36,0x49,0x49,0x32]),
    '7':bytearray([0x01,0x71,0x0d,0x03]),
    '8':bytearray([0x36,0x49,0x49,0x36]),
    '9':bytearray([0x26,0x49,0x49,0x3e]),
    'A':bytearray([0x3c,0x0a,0x0a,0x3c]),
    'B':bytearray([0x3e,0x2a,0x2a,0x1c]),
    'C':bytearray([0x1c,0x22,0x22]),
    'D':bytearray([0x3e,0x22,0x22,0x1c]),
    'E':bytearray([0x3e,0x2a,0x22]),
    'F':bytearray([0x3e,0x0a,0x02]),
    'G':bytearray([0x1c,0x22,0x2a,0x32]),
    'H':bytearray([0x3e,0x08,0x08,0x3e]),
    'I':bytearray([0x22,0x3e,0x22]),
    'J':bytearray([0x12,0x22,0x1e,0x02]),
    'K':bytearray([0x3e,0x08,0x14,0x22]),
    'L':bytearray([0x3e,0x20,0x20,0x20]),
    'M':bytearray([0x3e,0x04,0x08,0x04,0x3e]),
    'N':bytearray([0x3e,0x04,0x08,0x3e]),
    'O':bytearray([0x1c,0x22,0x22,0x1c]),
    'P':bytearray([0x3e,0x0a,0x0a,0x04]),
    'Q':bytearray([0x1e,0x21,0x31,0x5e]),
    'R':bytearray([0x3f,0x09,0x09,0x36]),
    'S':bytearray([0x24,0x2a,0x2a,0x12]),
    'T':bytearray([0x02,0x02,0x3e,0x02,0x02]),
    'U':bytearray([0x1e,0x20,0x20,0x1e]),
    'V':bytearray([0x06,0x18,0x20,0x18,0x06]),
    'W':bytearray([0x1c,0x20,0x10,0x20,0x1c]),
    'X':bytearray([0x22,0x14,0x08,0x14,0x22]),
    'Y':bytearray([0x03,0x04,0x38,0x04,0x03]),
    'Z':bytearray([0x31,0x29,0x25,0x23]),
    'o':bytearray([0x18,0x24,0x18]),
    '=':bytearray([0x14,0x14,0x14,0x14]),
    '+':bytearray([0x08,0x08,0x3e,0x08,0x08]),
    '-':bytearray([0x08,0x08,0x08]),
    '_':bytearray([0x20,0x20,0x20,0x20,0x20]),
    '"':bytearray([0x0c,0x00,0x0c]),
    '~':bytearray([0x08,0x04,0x08,0x04]),
    '^':bytearray([0x08,0x04,0x02,0x04,0x08]),
    '<':bytearray([0x08,0x14,0x22]),
    '>':bytearray([0x22,0x14,0x08]),
    '#':bytearray([0x14,0x3e,0x14,0x3e,0x14]),
    '$':bytearray([0x24,0x2a,0x6b,0x2a,0x12]),
    '@':bytearray([0x1c,0x42,0x59,0x15,0x3d,0x22,0x1c]),
    '?':bytearray([0x06,0x01,0x59,0x09,0x06]),
    '!':bytearray([0x5e])
}

def owo():
    dcfurs.clear()
    ## Draw the Oh's
    for x in range(1,6):
        dcfurs.set_pixel(0,x,256)
        dcfurs.set_pixel(4,x,256)
        dcfurs.set_pixel(13,x,256)
        dcfurs.set_pixel(17,x,256)
    for x in range(1,4):
        dcfurs.set_pixel(x,0,256)
        dcfurs.set_pixel(x,6,256)
    for x in range(14,17):
        dcfurs.set_pixel(x,0,256)
        dcfurs.set_pixel(x,6,256)
    ## What's this?
    dcfurs.set_pixel(6,2,256)
    dcfurs.set_pixel(6,3,256)
    dcfurs.set_pixel(7,4,256)
    dcfurs.set_pixel(8,3,256)
    dcfurs.set_pixel(9,3,256)
    dcfurs.set_pixel(10,4,256)
    dcfurs.set_pixel(11,2,256)
    dcfurs.set_pixel(11,3,256)

def boop():
    dcfurs.clear()
    # Gimmie a B!
    for x in range(0,7):
        dcfurs.set_pixel(1, x, 256)
    dcfurs.set_pixel(2,0,256)
    dcfurs.set_pixel(3,0,256)
    dcfurs.set_pixel(4,1,256)
    dcfurs.set_pixel(4,2,256)
    dcfurs.set_pixel(2,3,256)
    dcfurs.set_pixel(3,3,256)
    dcfurs.set_pixel(4,4,256)
    dcfurs.set_pixel(4,5,256)
    dcfurs.set_pixel(2,6,256)
    dcfurs.set_pixel(3,6,256)
    # And an Oh!
    dcfurs.set_pixel(7,0,256)
    dcfurs.set_pixel(7,4,256)
    for x in range(1,4):
        dcfurs.set_pixel(6,x,256)
        dcfurs.set_pixel(8,x,256)
    # And an another Oh!
    dcfurs.set_pixel(10,0,256)
    dcfurs.set_pixel(10,4,256)
    for x in range(1,4):
        dcfurs.set_pixel(9,x,256)
        dcfurs.set_pixel(11,x,256)
    # Gimmie a P!
    for x in range(0,7):
        dcfurs.set_pixel(13, x, 256)
    dcfurs.set_pixel(14,0,256)
    dcfurs.set_pixel(15,0,256)
    dcfurs.set_pixel(16,1,256)
    dcfurs.set_pixel(16,2,256)
    dcfurs.set_pixel(14,3,256)
    dcfurs.set_pixel(15,3,256)

## Render an emote from an ascii string
def render(str):
    lbits = font7bit[str[0]]
    rbits = font7bit[str[-1]]
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
    ## Anger
    [0x00000, 0x10002, 0x08004, 0x04008, 0x02010, 0, 0],
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
