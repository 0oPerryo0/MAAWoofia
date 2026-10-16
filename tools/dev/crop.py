"""Crop a template out of a 720p screenshot and print the padded roi for the pipeline.

Usage: python tools/dev/crop.py <screenshot.png> x y w h <out.png>
"""

import sys
from pathlib import Path

from PIL import Image

ROI_PADDING = 20


def crop_template(src: Path, box: tuple[int, int, int, int], out: Path) -> tuple[int, int, int, int]:
    x, y, w, h = box
    with Image.open(src) as img:
        width, height = img.size
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
            raise ValueError(f"box {box} is outside the {width}x{height} screenshot")
        out.parent.mkdir(parents=True, exist_ok=True)
        img.crop((x, y, x + w, y + h)).save(out)

    left = max(0, x - ROI_PADDING)
    top = max(0, y - ROI_PADDING)
    right = min(width, x + w + ROI_PADDING)
    bottom = min(height, y + h + ROI_PADDING)
    return (left, top, right - left, bottom - top)


def main() -> None:
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(1)
    src, *nums, out = sys.argv[1:]
    roi = crop_template(Path(src), tuple(int(n) for n in nums), Path(out))
    print(f"roi: [{roi[0]}, {roi[1]}, {roi[2]}, {roi[3]}]")


if __name__ == "__main__":
    main()
