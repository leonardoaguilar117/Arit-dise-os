"""Overlay the rebuilt vector wordmark on the approved PNG and report how well they match."""
import io, sys
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
from marks import ARITE, SW

lines = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in ARITE)
html = (f'<html><body style="margin:0;background:#fff"><svg width="960" height="960" viewBox="0 0 960 960" '
        f'stroke="#000" stroke-width="{SW}" fill="none">{lines}</svg></body></html>')
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg = b.new_page(viewport={"width": 960, "height": 960})
    pg.set_content(html)
    png = pg.screenshot()
    b.close()
mine = np.array(Image.open(io.BytesIO(png)).convert("L")) < 128
ref = np.array(Image.open(Path(__file__).parent.parent / "Logo" / "1. Base negro@2x.png").convert("L")) < 128
inter, union = (mine & ref).sum(), (mine | ref).sum()
print(f"IoU {inter / union:.3f}  ref px {ref.sum()}  mine px {mine.sum()}  only-ref {(ref & ~mine).sum()}  only-mine {(mine & ~ref).sum()}")
diff = np.zeros(ref.shape + (3,), np.uint8) + 255
diff[ref & mine] = (0, 0, 0); diff[ref & ~mine] = (220, 0, 0); diff[mine & ~ref] = (0, 120, 255)
Image.fromarray(diff).crop((180, 310, 780, 640)).save(Path(__file__).parent / "assets" / "logo-diff.png")
