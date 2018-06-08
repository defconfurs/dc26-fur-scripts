# main.py -- put your code here!
import pyb
import dcfurs
import badge
import micropython

print("Booting...")

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

## Run the show.
import animations
selected = 0
available = animations.all()
anim = available[selected]()

timeout = 120000

while True:
    anim.draw()
    ival = anim.interval
    while ival > 0:
        ## Change animation on button press
        if badge.right.event():
            selected = (selected + 1) % len(available)
            anim = available[selected]()
            timeout = 120000
        elif badge.left.event():
            if selected == 0:
                selected = len(available)
            selected = selected - 1
            anim = available[selected]()
            timeout = 120000
        elif badge.boop.event():
            #micropython.mem_info()
            boop()
            pyb.delay(1000)

        ## Run the animation timing
        if ival > 50:
            pyb.delay(50)
            ival -= 50
            timeout -= 50
        else:
            pyb.delay(ival)
            timeout -= ival
            ival = 0
        
        ## Attempt to suspend the badge between animations
        badge.trysuspend()

    ## Rotate through animations every 60 seconds.
    if timeout < 0:
        owo()
        pyb.delay(5000)
        selected = (selected + 1) % len(available)
        anim = available[selected]()
        timeout = 120000
