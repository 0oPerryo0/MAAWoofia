"""Exploration helper: tap / back / swipe through MaaFramework input, then screenshot.

Usage:
  python tools/dev/act.py tap <x> <y> <shot_name>
  python tools/dev/act.py back <shot_name>
  python tools/dev/act.py swipe <x1> <y1> <x2> <y2> <shot_name>
Coordinates are in the 720p screenshot space. Screenshot goes to dev/screens/<shot_name>.png.
"""

import sys
import time
from pathlib import Path

from maa.controller import AdbController
from maa.toolkit import Toolkit
from PIL import Image

from adb import adb_path, adb_serial

ROOT = Path(__file__).resolve().parents[2]
KEYCODE_BACK = 4


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] not in {"tap", "back", "swipe"}:
        print(__doc__)
        sys.exit(1)
    Toolkit.init_option(ROOT / "dev")
    ctrl = AdbController(adb_path(), adb_serial())
    if not ctrl.post_connection().wait().succeeded:
        print(f"cannot connect to ADB device {adb_serial()}")
        sys.exit(1)
    if args[0] == "tap":
        ctrl.post_click(int(args[1]), int(args[2])).wait()
    elif args[0] == "back":
        ctrl.post_click_key(KEYCODE_BACK).wait()
    else:
        x1, y1, x2, y2 = (int(a) for a in args[1:5])
        ctrl.post_swipe(x1, y1, x2, y2, 500).wait()
    time.sleep(2.5)
    img = ctrl.post_screencap().wait().get()  # BGR numpy array
    out = ROOT / "dev" / "screens" / f"{args[-1]}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img[:, :, ::-1]).save(out)
    Image.fromarray(img[:, :, ::-1]).resize((360, 640)).save(ROOT / "dev" / "screens" / "_last.png")
    print(f"saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
