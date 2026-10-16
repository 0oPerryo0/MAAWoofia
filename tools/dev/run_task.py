"""Run one pipeline entry against the emulator, with the Python agent attached.

Usage: python tools/dev/run_task.py <Entry> [--no-agent] [--override <json>]
Logs and on-error screenshots go to dev/debug/.
"""

import json
import subprocess
import sys
from pathlib import Path

from maa.agent_client import AgentClient
from maa.controller import AdbController
from maa.resource import Resource
from maa.tasker import Tasker
from maa.toolkit import Toolkit

from adb import adb_path, adb_serial

ROOT = Path(__file__).resolve().parents[2]


def run_task(entry: str, use_agent: bool = True, override: dict | None = None) -> bool:
    Toolkit.init_option(ROOT / "dev")

    resource = Resource()
    resource.post_bundle(ROOT / "assets" / "resource").wait()

    controller = AdbController(adb_path(), adb_serial())
    if not controller.post_connection().wait().succeeded:
        print(f"cannot connect to ADB device {adb_serial()} (adb: {adb_path()})")
        return False

    agent_proc = None
    client = None
    if use_agent:
        client = AgentClient()
        client.bind(resource)
        agent_proc = subprocess.Popen(
            [sys.executable, str(ROOT / "agent" / "main.py"), client.identifier],
            cwd=ROOT / "dev",
        )
        if not client.connect():
            print("cannot connect to agent")
            agent_proc.kill()
            return False

    try:
        tasker = Tasker()
        tasker.bind(resource, controller)
        tasker.set_log_dir(ROOT / "dev" / "debug")
        tasker.set_save_on_error(True)
        if not tasker.inited:
            print("tasker failed to initialize")
            return False
        return tasker.post_task(entry, override or {}).wait().succeeded
    finally:
        if client is not None:
            client.disconnect()
        if agent_proc is not None:
            agent_proc.wait(timeout=10)


def main() -> None:
    argv = sys.argv[1:]
    override = {}
    if "--override" in argv:
        i = argv.index("--override")
        override = json.loads(argv[i + 1])
        del argv[i : i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        sys.exit(1)
    ok = run_task(args[0], use_agent="--no-agent" not in argv, override=override)
    print("SUCCEEDED" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
