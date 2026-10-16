import pytest

from stage_nav import chapter_matches, parse_stage, stage_matches


def test_parse_main_stage():
    assert parse_stage("11-36") == (11, 36)


def test_parse_strips_spaces_and_fullwidth():
    assert parse_stage(" １１－４ ") == (11, 4)


def test_parse_rejects_garbage():
    with pytest.raises(ValueError):
        parse_stage("abc")


def test_stage_matches_exact_label():
    assert stage_matches("11-36", (11, 36))


def test_stage_matches_hard_prefix():
    assert stage_matches("困難11-4", (11, 4))


def test_stage_does_not_match_longer_number():
    assert not stage_matches("11-36", (11, 3))
    assert not stage_matches("111-3", (11, 3))


def test_chapter_matches_with_leading_zero_and_noise():
    assert chapter_matches("09", 9)
    assert chapter_matches("Y09", 9)
    assert chapter_matches("11", 11)


def test_chapter_does_not_match_other_numbers():
    assert not chapter_matches("110", 11)
    assert not chapter_matches("10", 1)


def test_count_plan_single_skip_needs_no_clicks():
    from stage_nav import count_plan

    assert count_plan(1) == ("plus", 0)


def test_count_plan_three_skips_presses_plus_twice():
    from stage_nav import count_plan

    assert count_plan(3) == ("plus", 2)


def test_count_plan_zero_means_max():
    from stage_nav import count_plan

    assert count_plan(0) == ("max", 1)


def test_chapter_number_roi_from_title_box():
    from stage_nav import number_roi_for_title

    # title 東黎城的日與夜Ⅱ at [217,614,332,103] → number "11" inside [195,580,110,85]
    assert number_roi_for_title((217, 614, 332, 103)) == (195, 580, 110, 85)


def test_is_chapter_title_box():
    from stage_nav import is_chapter_title

    assert is_chapter_title((217, 614, 332, 103))
    assert not is_chapter_title((502, 680, 23, 17))  # star count
