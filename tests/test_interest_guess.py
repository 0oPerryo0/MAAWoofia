from interest_guess import choose_card, pick_card

TABLE = {"銀煌鬥神白威": ["摸摸", "多人運動", "騎乘"], "卡‧拉特": ["鬥劍", "情侶吸管", "緊箍環"]}


def test_picks_matching_card():
    assert pick_card("銀煌鬥神白威", ["對坐", "騎乘", "試香"], TABLE) == 1


def test_normalizes_whitespace_and_width():
    assert pick_card(" 銀煌鬥神白威 ", ["多人 運動", "試香"], TABLE) == 0


def test_normalizes_name_dots():
    assert pick_card("卡．拉特", ["試香", "鬥劍"], TABLE) == 1


def test_no_match_returns_none():
    assert pick_card("銀煌鬥神白威", ["對坐", "試香", "鬥劍"], TABLE) is None


def test_unknown_character_returns_none():
    assert pick_card("小狼", ["摸摸"], TABLE) is None


def test_choose_prefers_table_match_over_yellow():
    assert choose_card("銀煌鬥神白威", ["對坐", "試香", "騎乘"], [True, False, False], TABLE) == 2


def test_choose_falls_back_to_yellow_border():
    assert choose_card("小狼", ["對坐", "試香", "騎乘"], [False, True, False], TABLE) == 1


def test_choose_defaults_to_middle_card():
    assert choose_card("小狼", ["對坐", "試香", "騎乘"], [False, False, False], TABLE) == 1


def _card_image(rgb):
    import numpy as np

    image = np.zeros((1280, 720, 3), dtype=np.uint8)
    image[540:550, 150:240] = rgb[::-1]  # BGR
    return image


def test_yellow_border_detected():
    from interest_guess import is_yellow_border

    assert is_yellow_border(_card_image((245, 217, 64)), 132)


def test_purple_border_not_yellow():
    from interest_guess import is_yellow_border

    assert not is_yellow_border(_card_image((193, 5, 217)), 132)


ALIASES = {"Cowgirl": "騎乘", "기승위": "騎乘", "多人运动": "多人運動"}


def test_card_names_in_other_languages_map_to_zh_tw():
    assert pick_card("銀煌鬥神白威", ["Face-off", "cowgirl", "Perfume"], TABLE, ALIASES) == 1
    assert pick_card("銀煌鬥神白威", ["多人运动"], TABLE, ALIASES) == 0


def test_korean_card_name_without_spaces_still_maps():
    from interest_guess import to_zh_tw

    assert to_zh_tw("기 승 위", ALIASES) == "騎乘"
    assert to_zh_tw("未知卡", ALIASES) == "未知卡"


def test_shipped_card_names_cover_every_language():
    import json
    from pathlib import Path

    aliases = json.loads((Path(__file__).parents[1] / "agent" / "data" / "card_names.json").read_text("utf-8"))
    assert aliases["Cooked Noodles"] == "煮好的泡麵"
    assert aliases["調理済みラーメン"] == "煮好的泡麵"
    assert aliases["끓인 라면"] == "煮好的泡麵"
    assert aliases["煮好的泡面"] == "煮好的泡麵"
