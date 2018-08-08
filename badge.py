## Here's all the stuff to make your badge's hardware operate normally.
import pyb
import dcfurs
import settings
from pyb import Pin
from pyb import Timer
from pyb import Accel
from pyb import ExtInt
from pyb import I2C
from pyb import UART

##-----------------------------------------------
## LED Matrix Drivers
##-----------------------------------------------
import micropython
micropython.alloc_emergency_exception_buf(100)

## Bring up the LED matrix
pwmclk = Timer(1, freq=125000)
dcfurs.init(pwmclk)
dcfurs.clear()

##-----------------------------------------------
## Bluetooth Module
##-----------------------------------------------
ble_enable = Pin('BLE_EN', Pin.OUT_OD)
ble_enable.value(0)
pyb.delay(5)
ble_enable.value(1)
ble = UART(1, 115200)

## Write variables with a little delay to make up
## for the lack of flow control.
def ble_set(name, value=None):
    line = "set: " + name
    if value:
        line += "=" + value
    line += "\r\n"
    for ch in line:
        ble.write(ch)
        pyb.delay(1)

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
## Capacative Touch Controller
##-----------------------------------------------
class capsense:
    IQS231_ADDR = const(0x44)

    ## IQS231A Register Address
    REG_PRODUCT_NUMBER = const(0x00)
    REG_SOFTWARE_VERSION = const(0x01)
    REG_DEBUG_EVENTS = const(0x02)
    REG_COMMANDS = const(0x04)
    REG_OTP_BANK_1 = const(0x05)
    REG_OTP_BANK_2 = const(0x06)
    REG_OTP_BANK_3 = const(0x07)
    REG_QUICK_RELEASE = const(0x08)
    REG_MOVEMENT = const(0x09)
    REG_TOUCH_THRESHOLD = const(0x0a)
    REG_PROXIMITY_THRESHOLD = const(0x0B)
    REG_TEMPERATURE_THRESHOLD = const(0x0C)
    REG_CH0_MULTIPLIERS = const(0x0D)
    REG_CH0_COMPENSATION = const(0x0E)
    REG_CH1_MULTIPLIERS = const(0x0F)
    REG_CH1_COMPENSATION = const(0x10)
    REG_SYSTEM_FLAGS = const(0x11)
    REG_UI_FLAGS = const(0x12)
    REG_ATI_FLAGS = const(0x13)
    REG_EVENT_FLAGS = const(0x14)
    REG_CH0_ACF = const(0x15)
    REG_CH0_LTA = const(0x17)
    REG_CH0_QRD = const(0x19)
    REG_CH1_ACF = const(0x1B)
    REG_CH1_UMOV = const(0x1D)
    REG_CH1_LMOV = const(0x1F)

    ## Command Register
    CMD_STANDALONE = 0x01
    CMD_AUTO_ATI = 0x02
    CMD_ENABLE_SENSING = 0x20
    CMD_DISABLE_SENSING = 0x40
    CMD_ATI_CH0 = 0x80

    ## Main Events Register
    MAIN_EVENT_SENSING_DISABLED = 0x20
    MAIN_EVENT_WARM_BOOT = 0x10
    MAIN_EVENT_COLD_BOOT = 0x08
    MAIN_EVENT_RELEASE = 0x04
    MAIN_EVENT_TOUCH = 0x02
    MAIN_EVENT_PROX = 0x01

    ## System Flags
    SYS_FLAGS_I2C_MODE = 0x80
    SYS_FLAGS_ADVNACE_TRACKING = 0x40
    SYS_FLAGS_CH1_ACTIVE = 0x20
    SYS_FLAGS_NO_SYNC = 0x08
    SYS_FALGS_CH0_LTA_HALTED = 0x04
    SYS_FLAGS_ATI_MODE = 0x02
    SYS_FLAGS_ZOOM_MODE = 0x01

    ## UI Flags
    UI_FLAGS_AUTO_ATI_OFF = 0x10
    UI_FLAGS_SENSING_DISABLE = 0x08
    UI_FLAGS_QUICK_RELEASE = 0x04
    UI_FLAGS_OUTPUT_ACTIVE = 0x01

    ## Event Flags
    EV_FLAGS_CH1_ATI_ERROR = 0x80
    EV_FLAGS_CH1_MOVEMENT = 0x10
    EV_FLAGS_CH0_ATI_ERROR = 0x08
    EV_FLAGS_CH0_UNDEBOUNCED = 0x04
    EV_FLAGS_CH0_TOUCH = 0x02
    EV_FLAGS_CH0_PROX = 0x01

    def __init__(self):
        self.prev = False
        self.i2c = I2C(1, I2C.MASTER, baudrate=400000)
        if not self.i2c.is_ready(self.IQS231_ADDR):
            self.i2c = None
    
    def write(self, addr, val):
        if self.i2c:
            self.i2c.mem_write(bytearray([val]), self.IQS231_ADDR, addr)

    def read(self, addr):
        if self.i2c:
            buf = self.i2c.mem_read(2, self.IQS231_ADDR, addr)
            return buf[1]
        else:
            return 0
    
    def debug(self):
        if self.i2c:
            buf = self.i2c.mem_read(6, self.IQS231_ADDR, self.REG_EVENT_FLAGS)
            print("0x%02x 0x%02x 0x%02x 0x%02x 0x%02x 0x%02x" % 
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]))
    
    def event(self):
        if not self.i2c:
            return False
        try:
            buf = self.i2c.mem_read(5, self.IQS231_ADDR, self.REG_CH0_ACF)
        except OSError as exc:
            ## In the event of I2C noise, the capsense controller may reset, in
            ## which case we require silence on the bus for at least t_test_mode
            ## to successfully reboot.
            if not self.i2c.is_ready(self.IQS231_ADDR):
                exti.disable()
                pyb.delay(500)
                exti.enable()
                exti.swint()
            if settings.debug:
                print("Capsense failed: " + uerrno.errorcode[exc.args[0]])
            return False
        acf = (buf[1] << 8) + buf[2]
        lta = (buf[3] << 8) + buf[4]
        if self.prev:
            self.prev = (acf < (lta/2))
            return False
        else:
            self.prev = (acf < (lta/2))
            return self.prev

boop = capsense()

##-----------------------------------------------
## Accelerometer and Sleep Control
##-----------------------------------------------
## Bring up and configure the Accelerometer
imu = pyb.Accel()
imu.write(0x7, 0x00)    # Switch to standby mode
imu.write(0x8, 0x00)    # Set sampling rate to 120Hz
imu.write(0x6, 0xe4)    # Enable shake and tap detection interrupts
imu.write(0x9, 0x6f)    # Set tap threshold to 15 counts, disable all by Z-axis for tap.
imu.write(0xA, 0x0f)    # Increase the tap debounce threshold.
imu.write(0x7, 0xc1)    # Set push-pull active-high interrupt, back to active mode.

## For tracking orientation.
xyz = [imu.x(), imu.y(), imu.y()]
sensitivity = 5

## Keep track of activity timing.
evtime = 0

## Enable wakeup from an active-high edge on PA0
def imucallback(line):
    global evtime
    evtime = pyb.millis()
    return imu.read(0x3)
    
def imudebug(line):
    tilt = imucallback(line)
    if (tilt & 0x80) != 0:
        print("Shake detected!")
    if (tilt & 0x20) != 0:
        print("Tap detected!")

exti = ExtInt('MMA_INT', Pin.IRQ_RISING, Pin.PULL_NONE, imucallback if not settings.debug else imudebug)
vbus = Pin('USB_VBUS', Pin.IN)

## Check for low power states, or do nothing.
def trysuspend():
    global evtime

    ## Do nothing if sleep is disabled
    timeout = settings.sleeptimeout
    if not timeout:
        return False

    ## Detect motion via the accelerometer
    dx = imu.x() - xyz[0]
    dy = imu.y() - xyz[1]
    dz = imu.z() - xyz[2]
    delta = (dx * dx) + (dy * dy) + (dz * dz)
    xyz[0] += dx
    xyz[1] += dy
    xyz[2] += dz
    if delta > (sensitivity * sensitivity):
        evtime = pyb.millis()
        return False

    ## Never suspend when USB VBus is present
    if vbus.value():
        evtime = pyb.millis()
        return False
    ## Don't sleep unless a timeout has elapsed.
    if (evtime + timeout) > pyb.millis():
        return False
    ## Turn off the display and go to deep sleep, with PA0 wakeup enabled.
    ble_enable.value(0)
    dcfurs.clear()
    pyb.standby(True)   # NOTE: pyb.standby API modified to enable PA0 wakeup.
    ## Will never get here...
