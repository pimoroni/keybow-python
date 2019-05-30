import keybow
import signal


@keybow.on()
def handle_key(index, state):
    print("Key {} has been {}".format(index, 'pressed' if state else 'released'))


signal.pause()
