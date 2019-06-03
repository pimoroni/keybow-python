#!/usr/bin/env python
import keybow
import time
import colorsys

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
]

try:
    for x in range(len(colors) * 2):
        r, g, b = colors[0]
        for x in range(12):
            keybow.set_pixel(x, r, g, b)
        colors.append(colors.pop(0))
        keybow.show()
        time.sleep(0.5)

    while True:
        t = time.time()
        for x in range(12):
            h = t / 10.0
            h += x / 12.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            keybow.set_pixel(x, r, g, b)
        keybow.show()
        time.sleep(1.0 / 60)

except KeyboardInterrupt:
    pass
