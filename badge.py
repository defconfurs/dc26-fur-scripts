## Here's all the stuff to make your badge's hardware operate normally.
import pyb
import dcfurs
from pyb import Pin
from pyb import Timer
from pyb import Accel
from pyb import ExtInt

##-----------------------------------------------
## LED Matrix Drivers
##-----------------------------------------------
import micropython
micropython.alloc_emergency_exception_buf(100)

## Bring up the LED matrix
dcfurs.matrix_init()
dcfurs.clear()
mtimer = pyb.Timer(5, freq=25000, callback=dcfurs.matrix_loop)

##-----------------------------------------------
## Pushbutton Class
##-----------------------------------------------
class switch(Pin):
    def __init__(self, pin):
        self.pin = pin
        self.prev = self.pin.value()
    
    ## Returns 1 on a rising edge, or 0 on no change.
    def event(self):
        if not self.prev:
            self.prev = self.pin.value()
            return self.prev
        else:
            self.prev = self.pin.value()
            return 0

right = switch(Pin('SW1', Pin.IN))
left = switch(Pin('SW2', Pin.IN, pull=Pin.PULL_DOWN))

##-----------------------------------------------
## Accelerometer and Sleep Control
##-----------------------------------------------
## Bring up and configure the Accelerometer
imu = pyb.Accel()
imu.write(0x7, 0x00)    # Switch to standby mode
imu.write(0x8, 0x00)    # Set sampling rate to 120Hz
imu.write(0x6, 0x04)    # Enable tap detection interrupt
imu.write(0x9, 0x6f)    # Set tap threshold to 15 counts, disable all by Z-axis for tap.
imu.write(0xA, 0x0f)    # Increase the tap debounce threshold.
imu.write(0x7, 0xc1)    # Set push-pull active-high interrupt, back to active mode.

## Track the elapsed time between shake and tap events.
evtime = 0

## Enable wakeup from an active-high edge on PA0
def imucallback(line):
    tilt = imu.read(0x3)
    evtime = pyb.millis()
    if (tilt & 0x80) != 0:
        print("Shake detected!")
    if (tilt & 0x20) != 0:
        print("Tap detected!")

exti = ExtInt('MMA_INT', Pin.IRQ_RISING, Pin.PULL_NONE, imucallback)
vbus = Pin('USB_VBUS', Pin.IN)

## Check for low power states, or do nothing.
def trysuspend():
    ## Never suspend when USB VBus is present
    if vbus.value():
        return False
    ## Don't sleep unless a timeout has elapsed.
    if (evtime + 60000) < pyb.millis():
        return False
    ## Turn off the display and go to deep sleep, with PA0 wakeup enabled.
    dcfurs.clear()
    pyb.standby(True)   # NOTE: pyb.standby API modified to enable PA0 wakeup.
    ## Will never get here...
