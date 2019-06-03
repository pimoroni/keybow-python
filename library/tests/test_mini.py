import mock
import sys
import pytest


def _mock():
    sys.modules['spidev'] = mock.Mock()
    sys.modules['spidev.SpiDev'] = mock.Mock()
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()


def test_mini():
    _mock()
    import keybow

    keybow.setup(keybow.MINI)

    assert len(keybow.callbacks) == 3
    assert len(keybow.pins) == 3
    assert len(keybow.leds) == 3
    assert len(keybow.buf) == 3
    assert len(keybow.states) == 3


def test_set_led_out_of_range():
    _mock()
    import keybow

    keybow.setup(keybow.MINI)

    with pytest.raises(IndexError):
        keybow.set_led(4, 255, 0, 0)
