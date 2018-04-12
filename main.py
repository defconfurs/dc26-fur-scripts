# main.py -- put your code here!
import pyb
import dcfurs
from pyb import Pin
from pyb import Timer
from pyb import Accel

print("Hello World!")
dcfurs.matrix_init()
dcfurs.clear()

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

class PushSW(Pin):
    def __init__(self, activelow=False):
        self.activelow = activelow
        self.prev = self.value()
    
    def press(self):
        if self.activelow and not self.prev:
            self.prev = self.value()
            return self.prev
        elif self.prev and not self.activelow:
            self.prev = self.value()
            return self.prev
        else:
            self.prev = self.value()
            return 0

## Setup the Accelerometer for tap detection
imu = pyb.Accel()
imu.write(0x7, 0x00)    # Switch to standby mode
imu.write(0x8, 0x00)    # Set sampling rate to 120Hz
imu.write(0x6, 0x04)    # Enable tap detection interrupt
imu.write(0x9, 0x0f)    # Set tap threshold to 15 counts.
imu.write(0x7, 0xc1)    # Set push-pull active-high interrupt, back to active mode.

## Setup the input pins
wkup = pyb.Pin('MMA_INT', Pin.IN)
right = PushSW(Pin('SW1', Pin.IN))
left = PushSW(Pin('SW2', Pin.IN, pull=Pin.PULL_DOWN))

## Run the main test pattern
print("Starting test pattern...")
def mtick(timer):
    dcfurs.matrix_loop()
mtimer = pyb.Timer(5, freq=16000, callback=mtick)

## Wait for a tap event.
owo()
while not wkup.value():
    pyb.delay(100)
boop()
pyb.delay(3000)

## Run the show.
import animations
selected = 0
available = animations.all()
anim = available[selected]()

while True:
    anim.draw()
    ival = anim.interval
    while ival > 0:
        ## Change animation on button press
        if right.press():
            selected = (selected + 1) % len(available)
            anim = available[selected]()
        elif left.press():
            if selected == 0:
                selected = len(available)
            selected = selected - 1
            anim = available[selected]()

        ## Run the animation timing
        if ival > 10:
            pyb.delay(10)
            ival -= 10
        else:
            pyb.delay(ival)
            ival = 0
