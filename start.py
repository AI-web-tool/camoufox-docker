"""
Launch Camoufox as a Playwright server on a fixed port.
Prints the WebSocket endpoint and keeps the process alive.
"""

import base64
import os
import signal
import subprocess
import sys
from pathlib import Path

import orjson

from camoufox.server import get_nodejs, to_camel_case_dict
from camoufox.pkgman import LOCAL_DATA
from camoufox.utils import launch_options

PORT = int(os.environ.get("CAMOUFOX_PORT", "9222"))
WS_PATH = os.environ.get("CAMOUFOX_WS_PATH", "")
LAUNCH_SCRIPT = LOCAL_DATA / "launchServer.js"


def strip_nulls(d):
    """Recursively remove keys with None/null values from a dict."""
    if not isinstance(d, dict):
        return d
    return {k: strip_nulls(v) for k, v in d.items() if v is not None}


def main():
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

    print(f"Starting Camoufox server on port {PORT} (headless=True)...")

    config = launch_options(headless=True, port=PORT)
    config = strip_nulls(config)
    config = to_camel_case_dict(config)

    if WS_PATH:
        path = WS_PATH if WS_PATH.startswith("/") else f"/{WS_PATH}"
        config["wsPath"] = path

    nodejs = get_nodejs()
    data = orjson.dumps(config)

    process = subprocess.Popen(
        [nodejs, str(LAUNCH_SCRIPT)],
        cwd=Path(nodejs).parent / "package",
        stdin=subprocess.PIPE,
        text=True,
    )
    print(data)
    if process.stdin:
        process.stdin.write(base64.b64encode(data).decode())
        process.stdin.close()

    process.wait()
    raise RuntimeError("Server process terminated unexpectedly")


if __name__ == "__main__":
    main()
