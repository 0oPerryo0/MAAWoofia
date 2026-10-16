import time

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

# 720x1280 portrait FRIENDS (追蹤清單) list
OCR_NODE = "FriendPoke_OCR"
POKE_LABEL = "頂一下"
ICON_ABOVE_LABEL = 18  # the tappable icon sits just above the 頂一下 label
NAME_X = (215, 235)  # friend names start at x≈222; titles below them start further right
SWIPE_UP = (360, 1000, 360, 450)
MAX_PAGES = 12


def poke_targets(results) -> list[tuple[int, int]]:
    return [(r.box[0] + r.box[2] // 2, r.box[1] - ICON_ABOVE_LABEL) for r in results if r.text == POKE_LABEL]


def page_names(results) -> set[str]:
    return {r.text for r in results if NAME_X[0] <= r.box[0] <= NAME_X[1]}


@AgentServer.custom_action("poke_all_friends")
class PokeAllFriends(CustomAction):
    """Tap every 頂一下 (once per friend per day; repeats are harmless), scrolling to the end."""

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        seen: set[str] = set()
        for _ in range(MAX_PAGES):
            image = context.tasker.controller.post_screencap().wait().get()
            reco = context.run_recognition(OCR_NODE, image)
            results = reco.all_results if reco else []
            names = page_names(results)
            if names and names <= seen:
                return True  # scrolled to the end: nothing new on this page
            for x, y in poke_targets(results):
                context.tasker.controller.post_click(x, y).wait()
                time.sleep(0.5)
            seen |= names
            context.tasker.controller.post_swipe(*SWIPE_UP, 600).wait()
            time.sleep(1.5)
        return True
