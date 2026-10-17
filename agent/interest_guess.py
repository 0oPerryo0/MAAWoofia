import json
import time
import unicodedata
from pathlib import Path

from maa.agent.agent_server import AgentServer
from maa.context import Context
from maa.custom_action import CustomAction

TABLE_PATH = Path(__file__).parent / "data" / "interests.json"
# card names in 简中/English/日本語/한국어 -> 繁中, from the game's 培慾卡片名稱表
CARD_NAMES_PATH = Path(__file__).parent / "data" / "card_names.json"

# 720x1280 portrait layout of the 培慾 card game
CARD_CENTERS = [(193, 620), (360, 620), (526, 620)]
CARD_LEFT_X = [132, 298, 465]
BORDER_Y = 545
CONFIRM = (360, 910)
DEFAULT_INDEX = 1
DOTS = str.maketrans({"‧": ".", "・": ".", "·": ".", "．": "."})


def normalize(text: str) -> str:
    return "".join(unicodedata.normalize("NFKC", text).translate(DOTS).split())


def to_zh_tw(card: str, aliases: dict[str, str]) -> str:
    """Map a card name read in another game language back to its 繁中 name (unknown names pass through)."""
    lookup = {normalize(name).casefold(): tw for name, tw in aliases.items()}
    return lookup.get(normalize(card).casefold(), card)


def pick_card(
    character: str, cards: list[str], table: dict[str, list[str]], aliases: dict[str, str] | None = None
) -> int | None:
    lookup = {normalize(name): wants for name, wants in table.items()}
    wanted = {normalize(card) for card in lookup.get(normalize(character), [])}
    for index, card in enumerate(cards):
        if normalize(to_zh_tw(card, aliases or {})) in wanted:
            return index
    return None


def choose_card(
    character: str,
    cards: list[str],
    yellow: list[bool],
    table: dict[str, list[str]],
    aliases: dict[str, str] | None = None,
) -> int:
    index = pick_card(character, cards, table, aliases)
    if index is not None:
        return index
    if any(yellow):
        return yellow.index(True)
    return DEFAULT_INDEX


def is_yellow_border(image, left_x: int) -> bool:
    """image is BGR; known-correct cards have a yellow top border, unknown ones purple."""
    strip = image[BORDER_Y - 2 : BORDER_Y + 3, left_x + 20 : left_x + 100]
    b, g, r = strip[..., 0], strip[..., 1], strip[..., 2]
    return ((r > 200) & (g > 170) & (b < 120)).mean() > 0.5


@AgentServer.custom_action("interest_round")
class InterestRound(CustomAction):
    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:
        param = json.loads(argv.custom_action_param or "{}") or {}
        character = param.get("character", "")
        print(f"interest_round: character={character!r}", flush=True)
        table = json.loads(TABLE_PATH.read_text(encoding="utf-8"))
        aliases = json.loads(CARD_NAMES_PATH.read_text(encoding="utf-8")) if CARD_NAMES_PATH.exists() else {}

        image = context.tasker.controller.post_screencap().wait().get()
        yellow = [is_yellow_border(image, x) for x in CARD_LEFT_X]

        names = []
        for x, y in CARD_CENTERS:
            context.tasker.controller.post_click(x, y).wait()
            time.sleep(0.6)
            image = context.tasker.controller.post_screencap().wait().get()
            reco = context.run_recognition("InterestGuess_CardName", image)
            names.append(reco.best_result.text if reco and reco.hit else "")

        index = choose_card(character, names, yellow, table, aliases)
        if pick_card(character, names, table, aliases) is None:
            print(f"interest_round: no table match: {character} {names} yellow={yellow} -> {index}", flush=True)

        context.tasker.controller.post_click(*CARD_CENTERS[index]).wait()
        time.sleep(0.6)
        context.tasker.controller.post_click(*CONFIRM).wait()
        return True
