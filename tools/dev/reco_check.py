"""Replay a saved screenshot through one pipeline node: does it hit, and where would it click?

Usage: python tools/dev/reco_check.py <NodeName> <screenshot.png> [--reco-only]
The node runs with its `next` cleared, against a fake controller that always returns the image.
--reco-only replaces the action with DoNothing (for Custom actions that need the agent).
"""

import sys
from pathlib import Path

import numpy as np
from maa.controller import CustomController
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


class ImageController(CustomController):
    def __init__(self, image: np.ndarray):
        super().__init__()
        self.image = image
        self.clicks: list[tuple[int, int]] = []

    def connect(self) -> bool:
        return True

    def request_uuid(self) -> str:
        return "reco-check"

    def screencap(self) -> np.ndarray:
        return self.image

    def click(self, x: int, y: int) -> bool:
        self.clicks.append((x, y))
        return True

    def touch_down(self, contact: int, x: int, y: int, pressure: int) -> bool:
        self.clicks.append((x, y))
        return True

    def touch_up(self, contact: int) -> bool:
        return True


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        sys.exit(1)
    node, shot = args
    Toolkit.init_option(ROOT / "dev")
    image = np.array(Image.open(shot).convert("RGB"))[:, :, ::-1].copy()  # BGR
    ctrl = ImageController(image)
    ctrl.post_connection().wait()
    resource = Resource()
    resource.post_bundle(ROOT / "assets" / "resource").wait()
    tasker = Tasker()
    tasker.bind(resource, ctrl)
    override = {node: {"next": [], "timeout": 1000, "post_delay": 0}}
    if "--reco-only" in sys.argv:
        override[node]["action"] = "DoNothing"
    ok = tasker.post_task(node, override).wait().succeeded
    print(f"{node}: {'HIT' if ok else 'MISS'} clicks={ctrl.clicks}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
