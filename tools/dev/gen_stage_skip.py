"""Generate assets/resource/pipeline/stage_skip.json (four sections share one sweep chain).

Usage: python tools/dev/gen_stage_skip.py
Sections run in order Main → Hard → Tour → Leftover; each can be disabled from the UI
(`enabled: false`), and each falls through to the next section on success or failure.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "resource" / "pipeline" / "stage_skip.json"

SECTIONS = ["Main", "Hard", "Tour", "Leftover"]


def after(section: str) -> list[str]:
    rest = SECTIONS[SECTIONS.index(section) + 1 :]
    return [f"Skip_{s}" for s in rest] + ["Skip_Finish"]


def open_sortie(p: str, nxt: list[str]) -> dict:
    return {
        f"{p}_OpenSortie": {
            "recognition": {"type": "And", "param": {"all_of": ["HomeAnchor"]}},
            "action": "Click",
            "target": [290, 1110, 140, 80],
            "post_delay": 2500,
            "next": nxt + ["[JumpBack]ClosePopup", "[JumpBack]NetworkRetry"],
        }
    }


def sweep_chain(p: str, section: str, count: int) -> dict:
    done = after(section)
    return {
        f"{p}_Sweep": {
            "recognition": "OCR",
            "expected": "^速通$",
            "roi": [215, 1185, 110, 55],
            "action": "Click",
            "post_delay": 1500,
            "next": [f"{p}_Dialog", f"{p}_NotEnough"],
            "on_error": done,
        },
        f"{p}_Dialog": {
            "recognition": "OCR",
            "expected": "速通次數",
            "roi": [240, 650, 260, 40],
            "action": "Custom",
            "custom_action": "sweep_set_count",
            "custom_action_param": {"count": count},
            "post_delay": 800,
            "next": [f"{p}_Confirm"],
        },
        f"{p}_Confirm": {
            "recognition": "OCR",
            "expected": "^確定$",
            "roi": [380, 765, 160, 55],
            "action": "Click",
            "post_delay": 3000,
            "next": [f"{p}_Result", f"{p}_NotEnough", "[JumpBack]NetworkRetry"],
        },
        f"{p}_Result": {
            "recognition": {
                "type": "And",
                "param": {
                    "all_of": [
                        {"recognition": "OCR", "expected": "速通結果", "roi": [250, 185, 220, 60]},
                        {"recognition": "OCR", "expected": "^完成$", "roi": [280, 945, 160, 55]},
                    ],
                    "box_index": 1,
                },
            },
            "action": "Click",
            "post_delay": 2000,
            "next": done,
        },
        # Spend guard: any "not enough" prompt (energy / tickets / attempts) is cancelled.
        f"{p}_NotEnough": {
            "recognition": {
                "type": "And",
                "param": {
                    "all_of": [
                        {"recognition": "OCR", "expected": "不足", "roi": [60, 380, 600, 350]},
                        {"recognition": "OCR", "expected": "^取消$", "roi": [60, 600, 600, 300]},
                    ],
                    "box_index": 1,
                },
            },
            "action": "Click",
            "post_delay": 1500,
            "next": done,
        },
    }


def story_section(section: str, p: str, hard: bool, count: int) -> dict:
    nodes = {
        f"Skip_{section}": {"next": [f"{p}_OpenSortie", "[JumpBack]GoHomeStep"]},
        **open_sortie(p, [f"{p}_Story"]),
        f"{p}_Story": {
            "recognition": "OCR",
            "expected": "STORY",
            "roi": [40, 180, 480, 220],
            "action": "Click",
            "post_delay": 2500,
            "next": [f"{p}_Goto", f"{p}_Story"],
        },
        f"{p}_Goto": {
            "recognition": "OCR",
            "expected": "主線",
            "roi": [75, 80, 80, 35],
            "action": "Custom",
            "custom_action": "goto_stage",
            "custom_action_param": {"stage": "", "hard": hard},
            "post_delay": 1500,
            "next": [f"{p}_Sweep"],
            "on_error": after(section),
        },
    }
    nodes.update(sweep_chain(p, section, count))
    return nodes


def tour_section() -> dict:
    p = "Tour"
    nodes = {
        "Skip_Tour": {"next": [f"{p}_OpenSortie", "[JumpBack]GoHomeStep"]},
        **open_sortie(p, [f"{p}_Challenge"]),
        f"{p}_Challenge": {
            "recognition": "OCR",
            "expected": "ALLENGE|^挑戰$",
            "roi": [350, 600, 330, 450],
            "action": "Click",
            "post_delay": 2500,
            "next": [f"{p}_Workshop", f"{p}_Challenge"],
        },
        f"{p}_Workshop": {
            "recognition": "OCR",
            "expected": "觀光工坊",
            "roi": [180, 460, 230, 80],
            "action": "Click",
            "post_delay": 2500,
            "next": [f"{p}_RecommendOn", f"{p}_TurnRecommendOn", f"{p}_Workshop"],
        },
        # 推薦 ON: each folder shows only its highest level
        f"{p}_RecommendOn": {
            "recognition": "OCR",
            "expected": "^ON$",
            "roi": [375, 1185, 90, 50],
            "next": [f"{p}_Level", f"{p}_ExpandFolder"],
            "on_error": after("Tour"),
        },
        f"{p}_TurnRecommendOn": {
            "recognition": "OCR",
            "expected": "^OFF$",
            "roi": [265, 1185, 90, 50],
            "action": "Click",
            "post_delay": 1500,
            "next": [f"{p}_RecommendOn"],
        },
        f"{p}_Level": {
            "recognition": "OCR",
            "expected": "工坊.?LV.?[0-9]+",
            "roi": [290, 200, 360, 560],
            "action": "Click",
            "post_delay": 2500,
            "next": [f"{p}_Sweep"],
        },
        # Open folders read e.g. 玩具工坊; locked ones are cut off by a lock icon (果凍工…開放)
        f"{p}_ExpandFolder": {
            "recognition": "OCR",
            "expected": "^.{2}工坊$",
            "roi": [170, 180, 300, 560],
            "action": "Click",
            "post_delay": 1500,
            "next": [f"{p}_Level"],
            "on_error": after("Tour"),
        },
    }
    nodes.update(sweep_chain(p, "Tour", 0))
    return nodes


def build() -> dict:
    nodes = {
        "StageSkip": {"next": [f"Skip_{s}" for s in SECTIONS] + ["Skip_Finish"]},
        "Skip_Finish": {"next": ["HomeAnchor", "[JumpBack]GoHomeStep"]},
    }
    nodes.update(story_section("Main", "SkipMain", hard=False, count=1))
    nodes.update(story_section("Hard", "SkipHard", hard=True, count=1))
    nodes.update(tour_section())
    nodes.update(story_section("Leftover", "SkipLeft", hard=False, count=0))
    nodes["Skip_Leftover"]["enabled"] = False
    return nodes


def main() -> None:
    header = "// Generated by tools/dev/gen_stage_skip.py — edit the generator, not this file.\n"
    OUT.write_text(header + json.dumps(build(), ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
