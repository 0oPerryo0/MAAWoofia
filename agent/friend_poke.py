import time

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

# 720x1280 portrait FRIENDS (追蹤清單) list
OCR_NODE = "FriendPoke_OCR"
POKE_LABEL = "頂一下"
ICON_ABOVE_LABEL = 28  # centre of the square icon above the 頂一下 label
NAME_X = (215, 235)  # friend names start at x≈222; titles below them start further right
# short, slow drag (~2 rows): a fast swipe flings the list past rows that never get poked
SWIPE_UP = (360, 900, 360, 560)
SWIPE_MS = 1500
MAX_PAGES = 20


def is_pokeable(image, x: int, y: int) -> bool:
    """Not yet poked today = yellow icon; poked = grey. image is BGR."""
    patch = image[y - 18 : y + 18, x - 18 : x + 18]  # whole icon; the black hand covers ~1/3 of it
    b, g, r = patch[..., 0], patch[..., 1], patch[..., 2]
    return ((r > 200) & (g > 160) & (b < 110)).mean() > 0.35


def poke_targets(results, image=None) -> list[tuple[int, int]]:
    targets = [(r.box[0] + r.box[2] // 2, r.box[1] - ICON_ABOVE_LABEL) for r in results if r.text == POKE_LABEL]
    if image is None:
        return targets
    return [(x, y) for x, y in targets if is_pokeable(image, x, y)]


def page_names(results) -> set[str]:
    return {r.text for r in results if NAME_X[0] <= r.box[0] <= NAME_X[1]}


@AgentServer.custom_action("poke_all_friends")
class PokeAllFriends(CustomAction):
    """Tap every 頂一下 (once per friend per day; repeats are harmless), scrolling to the end."""

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        seen: set[str] = set()
        poked = 0
        for _ in range(MAX_PAGES):
            image = context.tasker.controller.post_screencap().wait().get()
            reco = context.run_recognition(OCR_NODE, image)
            results = reco.all_results if reco else []
            names = page_names(results)
            if names and names <= seen:
                print(f"poke_all_friends: {len(seen)} friends seen, {poked} poked", flush=True)
                return True  # scrolled to the end: nothing new on this page
            for x, y in poke_targets(results, image):
                context.tasker.controller.post_click(x, y).wait()
                poked += 1
                time.sleep(0.5)
            seen |= names
            context.tasker.controller.post_swipe(*SWIPE_UP, SWIPE_MS).wait()
            time.sleep(1.5)
        print(f"poke_all_friends: page limit reached, {len(seen)} friends seen, {poked} poked", flush=True)
        return True
