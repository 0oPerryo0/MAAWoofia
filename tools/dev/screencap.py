"""Save the emulator screen to dev/screens/<name>.png, scaled so the short side is 720.

Usage: python tools/dev/screencap.py <name>
"""

import io
import subprocess
import sys
from pathlib import Path

from PIL import Image

from adb import adb_path, adb_serial

ROOT = Path(__file__).resolve().parents[2]
SHORT_SIDE = 720


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    raw = subprocess.run(
        [adb_path(), "-s", adb_serial(), "exec-out", "screencap", "-p"],
        capture_output=True, check=True, timeout=30,
    ).stdout
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    scale = SHORT_SIDE / min(img.size)
    if scale != 1:
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    out = ROOT / "dev" / "screens" / f"{sys.argv[1]}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"saved {out.relative_to(ROOT)} ({img.width}x{img.height})")


if __name__ == "__main__":
    main()
