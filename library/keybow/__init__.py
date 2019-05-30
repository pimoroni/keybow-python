import RPi.GPIO as GPIO

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
