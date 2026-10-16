from adb import adb_serial


def test_serial_env_override(monkeypatch):
    monkeypatch.setenv("MAA_ADB_SERIAL", "emulator-5554")
    assert adb_serial() == "emulator-5554"


def test_serial_default(monkeypatch):
    monkeypatch.delenv("MAA_ADB_SERIAL", raising=False)
    assert adb_serial() == "127.0.0.1:5555"
