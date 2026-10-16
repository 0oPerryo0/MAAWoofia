import pytest
from PIL import Image

from crop import crop_template


@pytest.fixture
def src(tmp_path):
    path = tmp_path / "screen.png"
    Image.new("RGB", (1280, 720), "white").save(path)
    return path


def test_crop_returns_padded_roi(src, tmp_path):
    out = tmp_path / "t.png"
    assert crop_template(src, (100, 100, 50, 40), out) == (80, 80, 90, 80)
    assert Image.open(out).size == (50, 40)


def test_crop_roi_clamped_to_screen(src, tmp_path):
    assert crop_template(src, (0, 0, 30, 30), tmp_path / "t.png") == (0, 0, 50, 50)


def test_crop_rejects_box_outside_screen(src, tmp_path):
    with pytest.raises(ValueError):
        crop_template(src, (1270, 700, 50, 50), tmp_path / "t.png")
