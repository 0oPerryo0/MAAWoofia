from collections import namedtuple

from friend_poke import page_names, poke_targets

R = namedtuple("R", "text box")

PAGE = [
    R("FRIENDS", (74, 45, 202, 36)),
    R("CRM", (223, 246, 53, 24)),
    R("追蹤中", (438, 305, 59, 24)),
    R("頂一下", (534, 305, 61, 25)),
    R("處死式熱水爐", (223, 408, 138, 30)),
    R("頂一下", (534, 470, 62, 26)),
]


def test_poke_targets_tap_icon_above_each_label():
    assert poke_targets(PAGE) == [(564, 277), (565, 442)]


def test_page_names_are_friend_names_only():
    assert page_names(PAGE) == {"CRM", "處死式熱水爐"}


def test_no_labels_means_no_targets():
    assert poke_targets([R("FRIENDS", (74, 45, 202, 36))]) == []


def _image_with_icon(rgb, x=564, y=277):
    import numpy as np

    image = np.zeros((1280, 720, 3), dtype=np.uint8)
    image[y - 12 : y + 12, x - 12 : x + 12] = rgb[::-1]  # BGR
    return image


def test_yellow_icon_is_pokeable():
    from friend_poke import is_pokeable

    assert is_pokeable(_image_with_icon((250, 215, 40)), 564, 277)


def test_grey_icon_is_not_pokeable():
    from friend_poke import is_pokeable

    assert not is_pokeable(_image_with_icon((130, 130, 130)), 564, 277)


def test_targets_skip_grey_buttons():
    image = _image_with_icon((250, 215, 40), 564, 277)  # first row yellow, second row black/grey
    assert poke_targets(PAGE, image) == [(564, 277)]
