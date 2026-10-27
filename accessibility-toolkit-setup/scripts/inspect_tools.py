#!/usr/bin/env python3
"""Report local accessibility tools without starting services or changing settings."""
import importlib.util
import json
import os
import platform
import shutil
import sys


def main() -> None:
    """Print interpreter, platform, executable and module availability as JSON."""
    commands = ('orca', 'Xvfb', 'xvfb-run', 'dbus-run-session', 'speech-dispatcher',
                'espeak', 'espeak-ng', 'chromium', 'google-chrome', 'firefox', 'node')
    modules = ('playwright', 'PIL', 'gi', 'pyatspi', 'speechd')
    print(json.dumps({
        'python': sys.executable,
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'display_configured_not_verified': bool(os.environ.get('DISPLAY')),
        'executables': {name: shutil.which(name) for name in commands},
        'modules_in_this_interpreter': {
            name: bool(importlib.util.find_spec(name)) for name in modules
        },
    }, indent=2))


if __name__ == '__main__':
    main()
