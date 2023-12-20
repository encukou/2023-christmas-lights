import time
import random

NUM_LIGHTS = 50

try:
    import machine
    import neopixel
except ImportError:
    neopixel = None
    np = [[0, 0, 0] for n in range(NUM_LIGHTS)]
    def led_pin(val):
        print('led', val, end='\r')
else:
    pin = machine.Pin(14, machine.Pin.OUT)  # D5
    np = neopixel.NeoPixel(pin, NUM_LIGHTS)
    led_pin = machine.Pin(2, machine.Pin.OUT)

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
    # Cannot get here
def float_to_int(rgb):
    r, g, b = rgb
    return int(r * 255), int(g * 255), int(b * 255)

def task(led_no):
    for i in range(random.getrandbits(8+2)):
        yield
    while True:
        #print('go', led_no)
        h = random.getrandbits(8) / 255
        for l_int in range(0, 256):
            np[led_no] = float_to_int(hsv_to_rgb(h, 1, l_int/256))
            yield
        for l_int in range(0, 256):
            np[led_no] = float_to_int(hsv_to_rgb(h, 1, 1-l_int/256))
            yield
        for i in range(random.getrandbits(8+2)):
            yield

def blink():
    while True:
        led_pin(0)
        for i in range(16):
            yield
        led_pin(1)
        for i in range(64):
            yield
    
tasks = [task(i) for i in range(NUM_LIGHTS)] + [blink()]

while True:
    for task in tasks:
        next(task)
    if neopixel:
        np.write()
    else:
        print(
            '',
            ''.join(f'\033[38;2;{r};{g};{b}m●\033[0m' for r, g, b in np),
            end='\r',
        )
    time.sleep(.05)

