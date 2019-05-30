import RPi.GPIO as GPIO
from spidev import SpiDev


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
    buf[index] = [r, g, b]


def show():
    # Start of frame, 4 empty bytes
    _buf = [0b00000000 for _ in range(4)]
    for rgbbr in buf:
        r, g, b, br = rgbbr
        _buf.append(0b11100000 | br)   # Start of LED frame, 0b11100000 + brightness
        _buf.append(b)
        _buf.append(g)
        _buf.append(r)
    # End of frame, 7 empty bytes
    _buf += [0b00000000 for _ in range(7)]
    spi.xfer(_buf)


def handle_keypress(pin):
    state = GPIO.input(pin)
    i = pins.index(pin)
    callback = callbacks[i]
    if callback is not None and callable(callback):
        callback(i, state)


def on(index=None, handler=None):
    """Attach a handler to a Keybow key.

    Your handler should accept an index and a state argument.

    """
    if index is not None:
        try:
            index = list(index)
        except TypeError:
            index = [index]

    if handler is None:
        def decorate(handler):
            for i in index:
                callbacks[i] = handler
        return decorate

    for i in index:
        callbacks[i] = handler


GPIO.setmode(GPIO.BCM)
GPIO.setup(pins, GPIO.INPUT, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pins, GPIO.PISING, callback=handle_keypress, bouncetime=50)

spi.open(0, 0)
