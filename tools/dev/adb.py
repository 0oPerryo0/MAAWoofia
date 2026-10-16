"""ADB location and device serial, overridable via MAA_ADB_PATH / MAA_ADB_SERIAL."""

import os

DEFAULT_ADB = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
DEFAULT_SERIAL = "127.0.0.1:5555"


def adb_path() -> str:
    return os.environ.get("MAA_ADB_PATH", DEFAULT_ADB)


def adb_serial() -> str:
    return os.environ.get("MAA_ADB_SERIAL", DEFAULT_SERIAL)
