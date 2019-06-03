import mock
import sys
import pytest


def _mock():
    sys.modules['spidev'] = mock.Mock()
    sys.modules['spidev.SpiDev'] = mock.Mock()
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()


def test_setup():
    _mock()
    import keybow
    keybow._is_setup = False
    keybow.setup()


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

    keybow.on(handler=lambda i, s: False)


def test_handle_keypress():
    _mock()
    import keybow

    @keybow.on(0)
    def handle_input_test(index, state):
        raise ValueError()

    with pytest.raises(ValueError):
        keybow._handle_keypress(keybow.FULL[0][0])

    # A second press should not call the handle_input_test function
    keybow._handle_keypress(keybow.FULL[0][0])


def test_set_led():
    _mock()
    import keybow

    keybow.set_led(0, 255, 0, 0)

    assert keybow.buf[3] == [255, 0, 0, 1.0]


def test_set_all():
    _mock()
    import keybow

    keybow.set_all(0, 255, 0)

    assert keybow.buf == [[0, 255, 0, 1.0] for _ in range(12)]


def test_clear():
    _mock()
    import keybow

    keybow.set_all(0, 255, 255)
    keybow.clear()

    assert keybow.buf == [[0, 0, 0, 1.0] for _ in range(12)]


def test_show():
    _mock()

    class SpiDev():
        def __init__(self):
            self.captured = None

        def xfer2(self, data):
            self.captured = data

    import keybow
    spi = SpiDev()
    keybow.setup()
    keybow.spi = spi

    keybow.set_all(0, 255, 0)
    keybow.show()

    # Lazy capture recording
    # with open('/tmp/capture.txt', 'w') as f:
    #    f.write(str(spi.captured))
    # assert 1 == 2

    assert spi.captured == [
        0, 0, 0, 0, 0, 0, 0, 0,  # SOF
        255, 0, 255, 0,          # LED1
        255, 0, 255, 0,          # LED2
        255, 0, 255, 0,          # ...
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,
        255, 0, 255, 0,          # LED12
        0]                       # EOF


def test_onexit():
    _mock()
    import keybow
    keybow._on_exit()
