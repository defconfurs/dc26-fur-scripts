## Scrolling text animation
import dcfurs
import fonts
import settings

class scroll:
    def __init__(self, text = None):
        if text:
            self.text = text
        else:
            self.text = settings.banner
        self.interval = 250
        self.scrollbuf = bytearray([0x00, 0x00, 0x00, 0x00])
        self.shift = 0
        
        for char in self.text:
            font = fonts.fontdict[settings.scrollfont]
            if char in font:
                self.scrollbuf += font[char]
    
    def draw(self):
        dcfurs.clear()
        for x in range(0, dcfurs.ncols):
            colbits = self.scrollbuf[(self.shift + x) % len(self.scrollbuf)]
            for y in range(0, dcfurs.nrows):
                if (colbits & (1 << y)) != 0:
                    dcfurs.set_pixel(x, y, 0xff)
        self.shift = (self.shift + 1) % len(self.scrollbuf)

