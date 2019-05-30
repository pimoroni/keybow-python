import RPi.GPIO as GPIO
from spidev import SpiDev
import time


__version__ = '0.0.1'


KEYS = [
    (17, 3),
    (27, 7),
    (23, 11),
    (22, 2),
    (24, 6),
    (5, 10),
    (6, 1),
    (12, 5),
    (13, 9),
    (20, 0),
    (16, 4),
    (26, 8)
]

MINI_KEYS = [
    (17, 0),
    (22, 1),
    (6, 2)
]

callbacks = [None for key in KEYS]
pins = [key[0] for key in KEYS]
leds = [key[1] for key in KEYS]
buf = [[0, 0, 0, 0] for key in KEYS]

spi = SpiDev()


def set_led(index, r, g, b):
    """Set an led.

    :param index: 0-based index of key to set the LED for
    :param r, g, b: amount of Red, Green and Blue (0-255)

    """
    index = leds.index(index)
    buf[index][0] = r
    buf[index][1] = g
    buf[index][2] = b


set_pixel = set_led


def show():
    # Start of frame, 4 empty bytes
    _buf = [0b00000000 for _ in range(4)]
    for rgbbr in buf:
        r, g, b, br = rgbbr
        _buf.append(0b11100000 | br)   # Start of LED frame, 0b11100000 + brightness
        _buf.append(b)
        _buf.append(g)
        _buf.append(r)
    # End of frame, 4 empty bytes
    _buf += [0b00000000 for _ in range(4)]
    spi.xfer2(_buf)


def _handle_keypress(pin):
    time.sleep(0.01)
    state = GPIO.input(pin)
    i = pins.index(pin)
    callback = callbacks[i]
    if callback is not None and callable(callback):
        callback(i, not state)


def on(index=None, handler=None):
    """Attach a handler to a Keybow key.

    Your handler should accept an index and a state argument.

    """
    if index is not None:
        try:
            index = list(index)
        except TypeError:
            index = [index]
    else:
        index = range(len(KEYS))

    if handler is None:
        def decorate(handler):
            for i in index:
                callbacks[i] = handler
        return decorate

    for i in index:
        callbacks[i] = handler


GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in pins:
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=_handle_keypress, bouncetime=200)

spi.open(0, 0)
