from PIL import Image
import numpy as np, sys
im = np.array(Image.open(sys.argv[1]).convert("L")).astype(int)
ink = im < 128
ys, xs = np.where(ink)
print("bbox", xs.min(), xs.max(), ys.min(), ys.max(), im.shape)
def runs(a):
    r = []; i = 0
    while i < a.size:
        if a[i]:
            s = i
            while i < a.size and a[i]: i += 1
            r.append((s, i - 1))
        i += 1
    return r
for y in (335, 348, 360, 425, 440, 470, 493, 600):
    print("row", y, runs(ink[y]))
for x in (300, 433, 478, 500, 568, 620, 660, 705, 740):
    print("col", x, runs(ink[:, x]))
