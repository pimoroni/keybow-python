import RPi.GPIO as GPIO
from spidev import SpiDev
import time
import atexit


__version__ = '0.0.2'


FULL = [
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

MINI = [
    (17, 2),
    (22, 1),
    (6, 0)
]

_is_setup = False


def setup(keymap=FULL):
    global _is_setup, spi, callbacks, pins, leds, buf, states
    if _is_setup:
        return
    _is_setup = True

    callbacks = [None for key in keymap]
    pins = [key[0] for key in keymap]
    leds = [key[1] for key in keymap]
    buf = [[0, 0, 0, 1.0] for key in keymap]
    states = [True for key in keymap]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for pin in pins:
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=_handle_keypress, bouncetime=1)

    spi = SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 1000000

    atexit.register(_on_exit)


def set_led(index, r, g, b):
    """Set an led.

    :param index: 0-based index of key to set the LED for
    :param r, g, b: amount of Red, Green and Blue (0-255)

    """
    setup()
    try:
        index = leds[index]
        buf[index][0] = r
        buf[index][1] = g
        buf[index][2] = b
    except IndexError:
        raise IndexError("LED {} is out of range!".format(index))


set_pixel = set_led


def set_all(r, g, b):
    """Set all Keybow LEDs."""
    setup()
    for i in range(len(leds)):
        set_led(i, r, g, b)


def clear():
    """Clear Keybow LEDs."""
    set_all(0, 0, 0)


def show():
    """Update LEDs on Keybow."""
    setup()
    # Start of frame, 4 empty bytes
    _buf = [0b00000000 for _ in range(8)]
    for rgbbr in buf:
        r, g, b, br = rgbbr
        br = int(br * 31)
        _buf.append(0b11100000 | br)   # Start of LED frame, 0b11100000 + brightness
        _buf.append(b)
        _buf.append(g)
        _buf.append(r)
    # End of frame, 4 empty bytes
    _buf += [0b00000000 for _ in range(1)]
    spi.xfer2(_buf)


def _handle_keypress(pin):
    time.sleep(0.005)
    state = GPIO.input(pin)
    i = pins.index(pin)

    # Suppress any repeated key events
    if state == states[i]:
        return

    states[i] = state

    callback = callbacks[i]
    if callback is not None and callable(callback):
        callback(i, not state)


def on(index=None, handler=None):
    """Attach a handler to a Keybow key.

    Your handler should accept an index and a state argument.

    """
    setup()
    if index is not None:
        try:
            index = list(index)
        except TypeError:
            index = [index]
    else:
        index = range(len(callbacks))

    if handler is None:
        def decorate(handler):
            for i in index:
                callbacks[i] = handler
        return decorate

    for i in index:
        callbacks[i] = handler


def _on_exit():
    clear()
    show()
