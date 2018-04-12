## Matrix-esque Rain Animation
import dcfurs

class dos:
    def __init__(self):
        self.interval = 750
        self.onoff = True
        dcfurs.clear()
        ## C
        dcfurs.set_pixel(0,1,256)
        dcfurs.set_pixel(0,2,256)
        dcfurs.set_pixel(0,3,256)
        dcfurs.set_pixel(0,4,256)
        dcfurs.set_pixel(1,5,256)
        dcfurs.set_pixel(2,5,256)
        dcfurs.set_pixel(3,4,256)
        dcfurs.set_pixel(3,1,256)
        dcfurs.set_pixel(2,0,256)
        dcfurs.set_pixel(1,0,256)
        ## Colon
        dcfurs.set_pixel(5,1,256)
        dcfurs.set_pixel(5,4,256)
        ## Backslash
        dcfurs.set_pixel(7,0,256)
        dcfurs.set_pixel(7,1,256)
        dcfurs.set_pixel(8,2,256)
        dcfurs.set_pixel(8,3,256)
        dcfurs.set_pixel(9,4,256)
        ## >
        dcfurs.set_pixel(11,0,256)
        dcfurs.set_pixel(12,1,256)
        dcfurs.set_pixel(13,2,256)
        dcfurs.set_pixel(12,3,256)
        dcfurs.set_pixel(11,4,256)
        
    def draw(self):
        ## Blink the underscore
        if self.onoff:
            value = 0
            self.onoff = False
        else:
            value = 256
            self.onoff = True
        dcfurs.set_pixel(14,5,value)
        dcfurs.set_pixel(15,5,value)
        dcfurs.set_pixel(16,5,value)
        dcfurs.set_pixel(17,5,value)
