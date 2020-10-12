# Keybow

## 3 and 12 key, backlit mechanical keyboard add-ons for the Raspberry Pi

[![Build Status](https://travis-ci.com/pimoroni/keybow-python.svg?branch=master)](https://travis-ci.com/pimoroni/keybow-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/keybow-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/keybow-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/keybow.svg)](https://pypi.python.org/pypi/keybow)
[![Python Versions](https://img.shields.io/pypi/pyversions/keybow.svg)](https://pypi.python.org/pypi/keybow)

# Installing

## Stable library from PyPi

Enable SPI:

```
sudo raspi-config nonint do_spi 0
```

Install the library:

```python
python3 -m pip install keybow
```

You may need to use `sudo` (or optionally `python` in lieu of `python3`)

## Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/keybow-python`
* `cd keybow-python`
* `sudo ./install.sh`

# API

## `@keybow.on()` Detect Keypress

Decorator to attach a handler to a Keybow key. Your handler should accept an index and a state argument.

**Handler callback params:**
* `index`: Integer - 0-based index of key to set the LED for, see [#index](#index)
* `state`: Boolean - `True` on key down, `False` on release

```python
@keybow.on()
def handle_key(index, state):
    print("{}: Key {} has been {}".format(
        time.time(),
        index,
        'pressed' if state else 'released'))
```

## `keybow.set_all(r, g, b)` Set all LEDs

**Parameters:**
* `r`, `g`, `b`: Integer - amount of Red, Green and Blue (0-255)

```python
keybow.set_all(0, 64, 128)
keybow.show()
```

> NOTE: Use [`keybow.show()`](#show) to update the LEDs actual state

## `keybow.set_led(index, r, g, b)` Set a single led.

**Parameters:**
* `index`: Integer - 0-based index of key to set the LED for, see [#index](#index)
* `r`, `g`, `b`: Integer - amount of Red, Green and Blue (0-255)

```python
for x in range(4):
    keybow.set_led(x, 255, 0, 0)
for x in range(4):
    keybow.set_led(x + 4, 0, 255, 0)
for x in range(4):
    keybow.set_led(x + 8,  0, 0, 255)
keybow.show()
```

> NOTE: Use [`keybow.show()`](#show) to update the LEDs actual state

## `keybow.clear()` Clear all LEDs

Turn off all LEDs

```python
keybow.clear()
keybow.show()
```

> NOTE: Use [`keybow.show()`](#show) to update the LEDs actual state

## `keybow.show()` Update LEDs <a id="show"></a>

Whenever setting LEDs use this to update the LED values. This needs to be used whenever you set any LED values

## Key `index` <a id="index"></a>

With GPIO on the left, the index is mapped out as following:

|      |      |      |
| ---: | ---: | ---: |
|  `9` | `10` | `11` |
|  `6` |  `7` |  `8` |
|  `3` |  `4` |  `5` |
|  `0` |  `1` |  `2` |
