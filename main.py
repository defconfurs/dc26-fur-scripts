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

def mtick(timer):
    dcfurs.matrix_loop()

## Setup the Accelerometer for tap detection
imu = pyb.Accel()
imu.write(0x7, 0x00)    # Switch to standby mode
imu.write(0x8, 0x00)    # Set sampling rate to 120Hz
imu.write(0x6, 0x04)    # Enable tap detection interrupt
imu.write(0x9, 0x0f)    # Set tap threshold to 15 counts.
imu.write(0x7, 0xc1)    # Set push-pull active-high interrupt, back to active mode.
wkup = pyb.Pin('MMA_INT', Pin.IN)

## Run the main test pattern
print("Starting test pattern...")
mtimer = pyb.Timer(4, freq=16000, callback=mtick)

## Wait for a tap event.
owo()
while not wkup.value():
    pyb.delay(100)
boop()
pyb.delay(3000)

## Run the show.
import animations
x = animations.rand()
anim = x()
while True:
    anim.draw()
    pyb.delay(anim.interval)
