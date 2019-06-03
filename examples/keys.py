import keybow
import signal
import time


@keybow.on()
def handle_key(index, state):
    print("{}: Key {} has been {}".format(time.time(), index, 'pressed' if state else 'released'))


signal.pause()
