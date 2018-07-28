# main.py -- put your code here!
import pyb
import dcfurs
import badge
import emote
import micropython
import ubinascii

print("Booting...")

## Handle events from the BLE module.
def blerx(args):
    for x in args:
        name, value = x.split('=')
        if name == 'emote':
            ## Select a random emote.
            if (not value) or (value == 'random'):
                emote.random()
                pyb.delay(2500)
            ## Parse a specific emote to draw. 
            else:
                emstr = ubinascii.unhexlify(value).decode("ascii")
                emote.render(emstr)
                pyb.delay(2500)

def ble():
    line = badge.ble.readline().decode("ascii")
    #print(line)
    try:
        event, x = line.split(':', 1)
        args = x.rstrip().split()
        if (event == 'rx'):
            blerx(args)
    except:
        return

## Run the show.
import animations
selected = 0
available = animations.all()
anim = available[selected]()

while True:
    anim.draw()
    ival = anim.interval
    while ival > 0:
        ## Change animation on button press, or emote if both pressed.
        if badge.right.event():
            if badge.left.value():
                emote.random()
            else: 
                selected = (selected + 1) % len(available)
                anim = available[selected]()
        elif badge.left.event():
            if badge.right.value():
                emote.random()
            elif selected == 0:
                selected = len(available)-1
                anim = available[selected]()
            else:
                selected = selected - 1
                anim = available[selected]()
        # Service events.
        elif badge.ble.any():
            ble()
        elif badge.boop.event():
            #micropython.mem_info()
            emote.boop()
            ival = 1000

        ## Pause for as long as long as both buttons are pressed.
        if badge.right.value() and badge.left.value():
            ival += 50
        
        ## Run the animation timing
        if ival > 50:
            pyb.delay(50)
            ival -= 50
        else:
            pyb.delay(ival)
            ival = 0
        
        ## Attempt to suspend the badge between animations
        badge.trysuspend()
