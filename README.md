DCFurs Badge Scripts
====================

The DC26 DefCon Furs badge is running a micropython environment that allows
you to script the badge to do awesome things.

At your disposal, you'll find:
* An STM32F401RET6 microcontroller running Micropython
* 32 Mbit SPI flash on SPI bus 3
* 7x18 pixel LED matrix display
* Two pushbutton switches on the ears
* Taiyo Yuden EYSGCNZ bluetooth radio connected to USART1
* I2C bus 1 for sensors, including:
    - MMA7660 accelerometer at address 0x4C
    - TBD for capacative touch
    - #badgelife shitty addon connector

Badge Module
------------
The `badge` module is implemented in `badge.py` and contains all the setup necessary
to bring your badge to life and operate the peripherals correctly. It is recommended
that you initialize your badge properly by adding an `import badge` statement at the
top of your `main.py` script.

### `badge.trysuspend()`
Check if the badge is in a state that can be put to standby mode, when in this state
the LED matrix and CPU will be disabled, and the accelerometer will be configured as
a wakeup source. Upon waking up from standby mode the CPU will perform a hard reset.

The badge will enter standby if all of the following conditions are met:
* No voltage is detected on the VBUS pin (ie: USB disconnected)
* No motion has been detected by the accelerometer within the last 10 minutes

DCFurs Module
-------------
The `dcfurs` module is impleneted within the Micropython firmware, and and includes
the DMA and interrupt handlers necessary to drive the LED matrix. By writing this
module in C, we can acheive a sufficiently fast scan rate to perform up to 16-steps
of per-pixel dimming control.

Pixels in the matrix are addressed by their row/column coordinates, starting from
row zero and column zero in the upper left corner of the matrix.

### `dcfurs.matrix_init()`
Initialize the LED matrix and DMA interrupt handlers, this must be called first before
any other features in the DCFurs module can be used.
TODO: Can we make this automagical on import?

### `dcfurs.matrix_loop()`
Perform one iteration of the PWM main loop for driving the LED matrix. This function is
written to be callable as an interrupt handler, and would typically be driven from a
high priority timer.

```
    from pyb import Timer
    mtimer = pyb.Timer(5, freq=25000, callback=dcfurs.matrix_loop)
```

### `dcfurs.clear()`
Clear the LED matrix, setting all pixels to an off state.

### `dcfurs.set_pixel(row, col, value=True)`
Sets the intensity of a single pixel using its row and column coordinates in the matrix.
The `value` parameter can provide a PWM intensity value. Integer values in the range of
zero to 256 control the intensity of the pixel, otherwise the truth value will either
set the pixel to full intensity, or switch it off.

### `dcfurs.set_row(row, bitmap)`
Set the pixels for an entire row using a bitmap of pixel on/off values.

Animations Module
-----------------
Badge animiations are written in python as a part of the `animations` module. Each class
provided by this module is a unique animation. The interface to an animation must provide
the `draw()` function and the `interval` variable. We can write a simple row-scanning
example as follows:

```
    import dcfurs

    class example:
        def __init__(self):
            self.counter = 0
            self.interval = 500
        
        def draw(self):
            self.counter += 1
            dcfurs.clear()
            dcfurs.set_row(self.counter % 7, 0x3ffff)
```

To add your animation to the default set provided by the badge, you must add an `import`
statement to `animations/__init__.py`

```
    from animations.example import example
```

### `draw()`
This function is called from `main.py` to update the LED matrix for one tick of the
animation.

### `interval`
The animation must provide this variable to devine the time between subseqeuent calls
to `draw()`
