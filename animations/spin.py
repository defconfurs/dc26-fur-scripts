## Windmill
import dcfurs
import badge

class spin:
    def __init__(self):
        self.interval = 50
        self.counter = 1
        self.tintBrightness = 1
        self.rimBrightness = 50
        self.brightness = 255
        self.showTint = True
        self.showRim = True
        self.clockwise = True
    
    def brick_vertical(self, targetY, targetX, brightness):
        dcfurs.set_pixel(targetY-3, targetX, brightness)
        dcfurs.set_pixel(targetY-2, targetX, brightness)
        dcfurs.set_pixel(targetY-1, targetX, brightness)
        dcfurs.set_pixel(targetY, targetX, brightness)
        dcfurs.set_pixel(targetY+1, targetX, brightness)
        dcfurs.set_pixel(targetY+2, targetX, brightness)
        dcfurs.set_pixel(targetY+3, targetX, brightness)

    def brick_up(self, targetY, targetX, brightness):
        dcfurs.set_pixel(targetY-3, targetX-3, brightness)
        dcfurs.set_pixel(targetY-2, targetX-2, brightness)
        dcfurs.set_pixel(targetY-1, targetX-1, brightness)
        dcfurs.set_pixel(targetY, targetX, brightness)
        dcfurs.set_pixel(targetY+1, targetX+1, brightness)
        dcfurs.set_pixel(targetY+2, targetX+2, brightness)
        dcfurs.set_pixel(targetY+3, targetX+3, brightness)

    def brick_horizontal(self, targetY, targetX, brightness):
        dcfurs.set_pixel(targetY, targetX-3, brightness)
        dcfurs.set_pixel(targetY, targetX-2, brightness)
        dcfurs.set_pixel(targetY, targetX-1, brightness)
        dcfurs.set_pixel(targetY, targetX, brightness)
        dcfurs.set_pixel(targetY, targetX+1, brightness)
        dcfurs.set_pixel(targetY, targetX+2, brightness)
        dcfurs.set_pixel(targetY, targetX+3, brightness)
    
    def brick_down(self, targetY, targetX, brightness):
        dcfurs.set_pixel(targetY-3, targetX+3, brightness)
        dcfurs.set_pixel(targetY-2, targetX+2, brightness)
        dcfurs.set_pixel(targetY-1, targetX+1, brightness)
        dcfurs.set_pixel(targetY, targetX, brightness)
        dcfurs.set_pixel(targetY+1, targetX-1, brightness)
        dcfurs.set_pixel(targetY+2, targetX-2, brightness)
        dcfurs.set_pixel(targetY+3, targetX-3, brightness)

    def spin_brick_clockwise(self, targetY, targetX, brightness):
        if self.counter % 4 == 0:
            self.brick_vertical(targetY, targetX, brightness)
        elif self.counter % 4 == 1:
            self.brick_up(targetY, targetX, brightness)
        elif self.counter % 4 == 2:
            self.brick_horizontal(targetY, targetX, brightness)
        elif self.counter % 4 == 3:
            self.brick_down(targetY, targetX, brightness)

    def spin_brick_counter_clockwise(self, targetY, targetX, brightness):
        if self.counter % 4 == 0:
            self.brick_vertical(targetY, targetX, brightness)
        elif self.counter % 4 == 1:
            self.brick_down(targetY, targetX, brightness)
        elif self.counter % 4 == 2:
            self.brick_horizontal(targetY, targetX, brightness)
        elif self.counter % 4 == 3:
            self.brick_up(targetY, targetX, brightness)

    def addRim(self):
        brightness = self.rimBrightness
        if self.showRim:
            # Bridge of nose
            dcfurs.set_pixel(6, 5, brightness)
            dcfurs.set_pixel(7, 4, brightness)
            dcfurs.set_pixel(8, 4, brightness)
            dcfurs.set_pixel(9, 4, brightness)
            dcfurs.set_pixel(10, 4, brightness)
            dcfurs.set_pixel(11, 5, brightness)
            # border
            for row in range(0, 7):
                dcfurs.set_pixel(0, row, brightness)
                dcfurs.set_pixel(17, row, brightness)
            for col in range(0, 17):
                dcfurs.set_pixel(col, 0, brightness)
                dcfurs.set_pixel(col, 6, brightness)
    def addTint(self):
        brightness = self.tintBrightness
        if self.showTint:
            for row in range(0,7):
                for col in range(0,18):
                    dcfurs.set_pixel(col, row, brightness)

    def draw(self):
        dcfurs.clear()
        self.addTint()
        self.addRim()
        if self.clockwise: 
            self.spin_brick_counter_clockwise(3, 3, self.brightness)
            self.spin_brick_clockwise(14, 3, self.brightness)
        else:
            self.spin_brick_clockwise(3, 3, self.brightness)
            self.spin_brick_counter_clockwise(14, 3, self.brightness)
        if (badge.imu.read(0x3) & 0x80) != 0: # Shake event
            if self.clockwise:
                self.clockwise = False
                print('counter clockwise')
            else:
                self.clockwise = True
                print('clockwise')
        self.counter += 1