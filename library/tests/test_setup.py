import mock
import sys


def _mock():
    sys.modules['spidev'] = mock.Mock()
    sys.modules['spidev.SpiDev'] = mock.Mock()
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()


def test_setup():
    _mock()
    import keybow
    del keybow


def test_handlers():
    _mock()
    import keybow

    @keybow.on(0)
    def handle_input_a(index, state):
        pass
    assert keybow.callbacks[0] is not None

    @keybow.on((1, ))
    def handle_input_b(index, state):
        pass
    assert keybow.callbacks[1] is not None

    @keybow.on([2])
    def handle_input_c(index, state):
        pass
    assert keybow.callbacks[2] is not None

    @keybow.on({3})
    def handle_input_d(index, state):
        pass
    assert keybow.callbacks[3] is not None


def test_leds():
    _mock()
    import keybow

    keybow.set_led(0, 255, 0, 0)
