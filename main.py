# main.py -- put your code here!
import pyb
import dcfurs
import badge
import emotes
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
                emotes.owo()
                pyb.delay(2500)
            ## Parse a specific emote to draw. 
            else:
                emstr = ubinascii.unhexlify(value).decode("ascii")
                emotes.render(emstr)
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
        ## Change animation on button press
        if badge.right.event():
            selected = (selected + 1) % len(available)
            anim = available[selected]()
        elif badge.left.event():
            if selected == 0:
                selected = len(available)
            selected = selected - 1
            anim = available[selected]()
        elif badge.ble.any():
            ble()
        elif badge.boop.event():
            #micropython.mem_info()
            emotes.boop()
            pyb.delay(1000)

        ## Run the animation timing
        if ival > 50:
            pyb.delay(50)
            ival -= 50
        else:
            pyb.delay(ival)
            ival = 0
        
        ## Attempt to suspend the badge between animations
        badge.trysuspend()
