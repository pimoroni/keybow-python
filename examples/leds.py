import keybow
import time
import colorsys

try:
    while True:
        t = time.time()
        h = t / 360.0
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
	for x in range(12):
            keybow.set_pixel(x, r, g, b)
        keybow.show()
        time.sleep(1.0 / 60)

except KeyboardInterrupt:
    pass
