import mock
import sys


def test_setup():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    import keybow
    del keybow


def test_handlers():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
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
