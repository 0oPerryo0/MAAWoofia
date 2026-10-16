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
    assert poke_targets(PAGE) == [(564, 287), (565, 452)]


def test_page_names_are_friend_names_only():
    assert page_names(PAGE) == {"CRM", "處死式熱水爐"}


def test_no_labels_means_no_targets():
    assert poke_targets([R("FRIENDS", (74, 45, 202, 36))]) == []
