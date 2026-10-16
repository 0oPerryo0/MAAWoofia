import json
import re
import time
import unicodedata

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

# 720x1280 portrait layout of STORY (主線) screens
MODE_ROI_NODE = "StageNav_Mode"
OCR_NODE = "StageNav_OCR"
MODE_TOGGLE = (360, 1212)
SWIPE_UP = (360, 1000, 360, 600)  # reveals older chapters / lower-numbered stages
NUMBER_NODE = "StageNav_ChapterNumber"
MAX_CHAPTER_SWIPES = 8
MAX_STAGE_SWIPES = 15
SETTLE_SECONDS = 2.0  # lists slide in after opening; OCR too early misreads positions


def parse_stage(text: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)-(\d+)", "".join(unicodedata.normalize("NFKC", text).split()))
    if not match:
        raise ValueError(f"stage must look like 11-36, got {text!r}")
    return int(match.group(1)), int(match.group(2))


def stage_matches(label: str, stage: tuple[int, int], hard: bool = False) -> bool:
    label = label.strip()
    if ("困難" in label) != hard:
        return False
    return re.search(rf"(?<![\d-]){stage[0]}-{stage[1]}$", label) is not None


def chapter_matches(label: str, chapter: int) -> bool:
    return re.search(rf"(?<!\d)0?{chapter}(?!\d)", label.strip()) is not None


def is_chapter_title(box) -> bool:
    """Chapter cards have a large title starting at x≈217; the number sits above-left of it."""
    x, _, _, h = box
    return 200 <= x <= 240 and h >= 60


def number_roi_for_title(box) -> tuple[int, int, int, int]:
    x, y, _, _ = box
    return (x - 22, y - 34, 110, 85)


def _find_chapter(context: Context, chapter: int):
    image = context.tasker.controller.post_screencap().wait().get()
    reco = context.run_recognition(OCR_NODE, image)
    for result in (reco.all_results if reco else []):
        if not is_chapter_title(result.box):
            continue
        roi = list(number_roi_for_title(result.box))
        number = context.run_recognition(NUMBER_NODE, image, {NUMBER_NODE: {"roi": roi}})
        if number and number.hit and chapter_matches(number.best_result.text, chapter):
            return result.box
    return None


def _ocr(context: Context):
    image = context.tasker.controller.post_screencap().wait().get()
    reco = context.run_recognition(OCR_NODE, image)
    return reco.all_results if reco else []


def _center(box) -> tuple[int, int]:
    x, y, w, h = box
    return x + w // 2, y + h // 2


@AgentServer.custom_action("goto_stage")
class GotoStage(CustomAction):
    """From the STORY chapter list: pick 普通/困難, open the stage's chapter, tap the stage."""

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        param = json.loads(argv.custom_action_param or "{}") or {}
        try:
            stage = parse_stage(str(param.get("stage", "")))
        except ValueError as exc:
            print(f"goto_stage: {exc}", flush=True)
            return False
        hard = bool(param.get("hard", False))

        print(f"goto_stage: stage={stage[0]}-{stage[1]} hard={hard}", flush=True)
        if not self._set_mode(context, hard):
            print("goto_stage: could not switch 普通/困難", flush=True)
            return False

        time.sleep(SETTLE_SECONDS)
        for attempt in range(MAX_CHAPTER_SWIPES + 1):
            title = _find_chapter(context, stage[0])
            if title is None and attempt == 0:
                time.sleep(SETTLE_SECONDS)  # re-check once before scrolling away from the top
                title = _find_chapter(context, stage[0])
            if title:
                context.tasker.controller.post_click(*_center(title)).wait()
                time.sleep(2.5 + SETTLE_SECONDS)
                break
            context.tasker.controller.post_swipe(*SWIPE_UP, 500).wait()
            time.sleep(1)
        else:
            print(f"goto_stage: chapter {stage[0]} not found", flush=True)
            return False

        for _ in range(MAX_STAGE_SWIPES):
            hits = [r for r in _ocr(context) if stage_matches(r.text, stage, hard)]
            if hits:
                context.tasker.controller.post_click(*_center(hits[0].box)).wait()
                time.sleep(2)
                return True
            context.tasker.controller.post_swipe(*SWIPE_UP, 500).wait()
            time.sleep(1)
        print(f"goto_stage: stage {stage[0]}-{stage[1]} not found", flush=True)
        return False

    @staticmethod
    def _set_mode(context: Context, hard: bool) -> bool:
        """Toggle the bottom 普通/困難 switch until OCR confirms the wanted mode."""
        for _ in range(3):
            image = context.tasker.controller.post_screencap().wait().get()
            mode = context.run_recognition(MODE_ROI_NODE, image)
            if mode and mode.hit and ("困難" in mode.best_result.text) == hard:
                return True
            context.tasker.controller.post_click(*MODE_TOGGLE).wait()
            time.sleep(1.5)
        return False


# 速通 dialog: + and max buttons right of the 速通次數 slider
SWEEP_PLUS = (532, 708)
SWEEP_MAX = (582, 708)
SWEEP_DIALOG_NODE = "StageNav_SweepDialog"
MAX_PRESSES = 20  # daily caps are 16 (energy) / 3 (hard, workshop); never tap blindly beyond this


def count_plan(count: int) -> tuple[str, int]:
    """count <= 0 means as many as possible."""
    return ("max", 1) if count <= 0 else ("plus", min(count - 1, MAX_PRESSES))


@AgentServer.custom_action("sweep_set_count")
class SweepSetCount(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        param = json.loads(argv.custom_action_param or "{}") or {}
        try:
            count = int(param.get("count", 1))
        except (TypeError, ValueError):
            count = 1
        print(f"sweep_set_count: count={count}", flush=True)
        button, presses = count_plan(count)
        target = SWEEP_MAX if button == "max" else SWEEP_PLUS
        for _ in range(presses):
            # only ever tap while the 速通 dialog is on screen (a popup may have replaced it)
            image = context.tasker.controller.post_screencap().wait().get()
            dialog = context.run_recognition(SWEEP_DIALOG_NODE, image)
            if not (dialog and dialog.hit):
                print("sweep_set_count: 速通 dialog gone, stopping", flush=True)
                return False
            context.tasker.controller.post_click(*target).wait()
            time.sleep(0.3)
        return True
