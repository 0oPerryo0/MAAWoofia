"""Export data tables (TextAsset, MonoBehaviour) from Unity bundles into dev/asset-dump/tables/.

Read-only and data-only: textures, sprites, audio and meshes are never read.
Usage: python tools/dev/dump_tables.py <bundle> [<bundle> ...]
"""

import json
import sys
from pathlib import Path

import UnityPy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "dev" / "asset-dump" / "tables"
DATA_TYPES = {"TextAsset", "MonoBehaviour"}
# Bundle headers have the engine version stripped; this is the player version from the APK.
UnityPy.config.FALLBACK_UNITY_VERSION = "2022.3.62f2"


def dump_bundle(bundle: Path) -> int:
    env = UnityPy.load(str(bundle))
    target = OUT / bundle.name.split("_assets_")[0]
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for obj in env.objects:
        if obj.type.name not in DATA_TYPES:
            continue
        if obj.type.name == "TextAsset":
            data = obj.read()
            name = data.m_Name or str(obj.path_id)
            (target / f"{name}.bytes").write_bytes(data.m_Script.encode("utf-8", "surrogateescape"))
        else:
            try:
                tree = obj.read_typetree()
            except Exception as exc:  # typetree missing for IL2CPP scripts
                tree = {"_unreadable": str(exc)}
            name = tree.get("m_Name") or str(obj.path_id)
            (target / f"{name}.json").write_text(
                json.dumps(tree, ensure_ascii=False, indent=1, default=str), encoding="utf-8"
            )
        count += 1
    return count


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for arg in sys.argv[1:]:
        print(f"{dump_bundle(Path(arg))} data objects <- {Path(arg).name}")


if __name__ == "__main__":
    main()
