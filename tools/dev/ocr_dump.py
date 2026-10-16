"""Print every OCR text box on a screenshot (or the live screen with --live).

Usage: python tools/dev/ocr_dump.py <screenshot.png | --live> [min_score]
"""

import sys
from pathlib import Path

import numpy as np
from maa.controller import AdbController
from maa.pipeline import JOCR, JRecognitionType
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit
from PIL import Image

from adb import adb_path, adb_serial
from reco_check import ImageController

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    min_score = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    Toolkit.init_option(ROOT / "dev")
    if sys.argv[1] == "--live":
        live = AdbController(adb_path(), adb_serial())
        live.post_connection().wait()
        image = live.post_screencap().wait().get()
    else:
        image = np.array(Image.open(sys.argv[1]).convert("RGB"))[:, :, ::-1].copy()
    ctrl = ImageController(image)
    ctrl.post_connection().wait()
    resource = Resource()
    resource.post_bundle(ROOT / "assets" / "resource").wait()
    tasker = Tasker()
    tasker.bind(resource, ctrl)
    detail = tasker.post_recognition(JRecognitionType.OCR, JOCR(roi=(0, 0, 0, 0)), image).wait().get()
    results = getattr(detail.nodes[0].recognition, "all_results", []) if detail and detail.nodes else []
    for r in sorted(results, key=lambda r: (r.box[1], r.box[0])):
        if r.score >= min_score:
            print(f"{list(r.box)}\t{r.score:.2f}\t{r.text}")


if __name__ == "__main__":
    main()
