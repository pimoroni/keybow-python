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
