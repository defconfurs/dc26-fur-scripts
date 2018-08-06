DCFurs Badge Scripts
====================

The DC26 DefCon Furs badge is running a micropython environment that allows
you to script the badge to do awesome things.

### Features Include
* STM32F411RET6 microcontroller running Micropython
* 32 Mbit SPI flash on SPI bus 3
* 18x7 pixel LED matrix display
* Two pushbutton switches located on the ears
* Taiyo Yuden EYSGCNZ bluetooth radio connected to USART1
* I2C bus 1 for sensors, including:
    - NXP MMA7660 accelerometer at address 0x4C
    - Azoteq IQS231A capacative touch controller at address 0x44
    - #badgelife shitty addon connector

### Further Reading
* Source code, schematics and documentation are available on [GitHub](https://github.com/oskirby/dc26-fur-scripts)
* A web-based tool for creating JSON animations at http://dcfurs.liquidthex.com/defcon/

Badge Module
------------
The `badge` module is implemented in `badge.py` and contains all the setup necessary
to bring your badge to life and operate the peripherals correctly. It is recommended
that you initialize your badge properly by adding an `import badge` statement at the
top of your `main.py` script.

### `badge.imu`
This contains an instance of the MMA7660 accelerometer, which has been configured to
perform wakeup and tap detection on the badge. The accelerometer is also available
for orientation detection. Please refer to the micropython documentation for the API
to the `pyb.Accel` class.

### `badge.ble`
This contains an instance of the `pyb.UART` class, and is configured to communicate
to the Taiyo Yuden EYSGCNZWY bluetooth module.

### `badge.boop`
This contains a class dedicated to driving the IQS231A capacative sense controller,
it provides an `event()` method that returns `True` when a capacative touch has been
detected.

### `badge.trysuspend()`
Check if the badge is in a state that can be put to standby mode, when in this state
the LED matrix and CPU will be disabled, and the accelerometer will be configured as
a wakeup source. Upon waking up from standby mode the CPU will perform a hard reset.

The badge will enter standby if all of the following conditions are met:
* No voltage is detected on the VBUS pin (ie: USB disconnected)
* No motion has been detected by the accelerometer in the last `settings.sleeptimeout`
    milliseconds

Settings Module
---------------
The `settings` module is implemented in `settings.py` and contains a collection of
tunable parameters on how you want your badge to operate, such as the default
animation to play on bootup and how long of a timeout to use before going to sleep.

DCFurs Module
-------------
The `dcfurs` module is impleneted within the Micropython firmware, and and includes
the DMA and interrupt handlers necessary to drive the LED matrix. By writing this
module in C, we can acheive a sufficiently fast scan rate to perform up to 64-steps
of per-pixel dimming control.

Pixels in the matrix are addressed by their row/column coordinates, starting from
row zero and column zero in the upper left corner of the matrix.

### `dcfurs.init(timer)`
Initialize the LED matrix and DMA interrupt handlers, this must be called first before
any other features in the DCFurs module can be used. The `timer` parameter provides a
handle to the STM32 Advanced-function timer `TIM1`, configured at the desired PWM
frequency. This timer will be used to provide interrupts and DMA transfers in order
to refresh the delay.

```
    import dcfurs
    from pyb import Timer

    pwmclk = pyb.Timer(1, freq=125000)
    dcfurs.init(pwmclk)
```

### `dcfurs.clear()`
Clear the LED matrix, setting all pixels to an off state.

### `dcfurs.set_row(row, pixels)`
Set the pixels for an entire row using a bitmap of pixel on/off values. The `pixels` 
parameter can contain an integer, which will act as a bitmask of the pixels for this
row, or an `bytearray` of PWM intensities.

### `dcfurs.set_pixel(row, col, value=True)`
Sets the intensity of a single pixel using its row and column coordinates in the matrix.
The `value` parameter can provide a PWM intensity value. Integer values in the range of
zero to 256 control the intensity of the pixel, otherwise the truth value will either
set the pixel to full intensity, or switch it off.

### `dcfurs.set_frame(fbuf)`
Sets the entire frame buffer in a single call. The `fbuf` parameter should be an array exactly
`dcfurs.nrows` in length, each elemnent of which describes one row of the matrix. If the row
is an integer, it is interpreted as a bitmap that would be passed to `dcfurs.set_row()`, or if
the row is a `bytearray` then it will be interpreted as an array of PWM intensity values.

This function can be implemented as a slightly more efficient version of:

```
    def set_frame(fbuf)
        i = 0
        for row in fbuf:
            set_row(i, row)
            i += 1
```

### `dcfurs.has_pixel(row, col)`
Checks if the pixel at the given row and colum exists in the LED matrix. Due to the shape
of the badge, some of the pixels at the corners of the matrix and over the bridge of the
nose are missing from the display. This function will return `True` if the pixel exists
and `False` otherwise.

### `dcfurs.nrows`
This constant integer defines the number of rows in the LED matrix. This will have a
value of 7.

### `dcfurs.ncols`
This constant integer defines the number of columns in the LED matrix. This is will
have a value of 18.

Badge Animations
================
Badge animations can be written as Python classes, or can be provided as JSON frame
data. The resulting animations will be included as part of the `animations` module,
with each class in this module providing a unique animation.

Every class provided by this module must present the following interface.

### `draw()`
This function is called to render the next frame of the animation to the LED matrix.

### `interval`
The animation must provide this variable to define the time, in milliseconds, until the
call should be made to the `draw()` function.

Python Animations
-----------------
Badge animations written in python should be placed in the `animations/` directory, and
must implement both the `draw()` method and set the `interval` variable. We can write a
simple row-scanning example as follows:

```
    import dcfurs

    class example:
        def __init__(self):
            self.counter = 0
            self.interval = 500
        
        def draw(self):
            self.counter += 1
            dcfurs.clear()
            dcfurs.set_row(self.counter % dcfurs.nrows, 0x3ffff)
```

To add your animation to the default set provided by the badge, you must add an `import`
statement to `animations/__init__.py`

```
    from animations.example import example
```

From a REPL console, you can now run your animation with a simple python loop.

```
    import animations

    test = animations.example()
    while True:
        test.draw()
        pyb.delay(test.interval)
```

JSON Animations
---------------
For simple animations that don't require user interraction, the frames can also be
provided in JSON format. These animations should be placed in the `animations/`
directory and named with a `.json` file extension. During initialization the
`animations` module will generate class definitions for each JSON file found.

The JSON file should contain an array, with each element of the array containing
a JSON object that defines an `interval` encoded as an integer, and a `frame` encoded
as a string. The string should be a hexadecimal representation of the PWM intensity
for each pixel, with rows delimited by a colon `':'`. One nibble is given for each
pixel, with a value of `0` turning the pixel off and `F` setting the pixel to full
intensity.

Thus a single frame which shows PWM intensity increasing from right to left and top to
bottom can be encoded as:

```
    [
        {
            "interval": 1000,
            "frame": "000000000000001234:000000000000123456:000000000012345678:00000000123456789a:000000123456789abc:0000123456789abcde:00123456789abcdeff"
        }
    ]
```


Recovery and Programming Modes
==============================
If something has gone wrong with your badge, don't panic! There are many
ways to recover the state of your firwmare.

During power on, the two pushbuttons switches on the ears can be used to
select the boot mode of the badge firmware. Switch `SW1` is located on the
left ear, adjacent to the shitty addon header and puts the badge into DFU
bootloader mode. Switch `SW2` is located on the right ear opposite the
shitty addon header, and puts the badge into safe mode or performs factory
recovery.

Safe Mode and Recovery
----------------------
If switch `SW2` is pressed during power on, the LED on the back of the badge
will begin to cycle through three colors: Green, Blue and Cyan to select
the boot mode. To select a boot mode, wait until the desired color is active
and then release `SW2`. The badge will flash your selected mode and then proceed
to boot.

* Green selects normal boot mode, which mounts the filesystem and executes `boot.py` and `main.py`
* Blue selects safe mode, which mounts the filesystem but does not execute `boot.py` or `main.py`
* Cyan performs a factory recovery, which formats the filesystem and restores the default contents.

Updating Firmware
-----------------
The STM32F411 microcontroller features a DFU bootloader, which is capable of updating
its firmware via USB. From a Linux or OSX machine, you will need the `firmware.dfu`
image, as well as the `dfu-util` program. To apply a firwmare update, perform the
following steps.

1. Completely power down the badge by removing the batteries and USB power.
2. Power on badge via USB while holding down switch `SW1`, located adjacent to the
    shitty addon header.
3. Execute the command `dfu-util -a 0 -d 0483:df11 -D firmware.dfu`. Note that this
    may require `sudo` depending on your operating system and USB permissions.
4. Wait for the upgrade to complete, which may take up to 30 seconds.
5. Unplug the badge from USB to restart and apply the firmware update.
