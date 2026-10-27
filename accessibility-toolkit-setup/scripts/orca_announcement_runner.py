#!/usr/bin/env python3
"""Run an existing Orca launcher for logged announcements in a private session."""
import argparse
import os
from pathlib import Path
import runpy
import sys


def main() -> int:
    """Validate isolation and paths, then delegate event handling to real Orca."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrypoint', type=Path, required=True)
    parser.add_argument('--module-dir', type=Path, required=True)
    parser.add_argument('--prefs-dir', type=Path, required=True)
    parser.add_argument('--debug-log', type=Path, required=True)
    args = parser.parse_args()
    if (os.environ.get('A11Y_ISOLATED_SESSION') != '1'
            or not os.environ.get('DISPLAY')
            or not os.environ.get('DBUS_SESSION_BUS_ADDRESS')):
        parser.error('Use a private Xvfb/D-Bus session and A11Y_ISOLATED_SESSION=1')
    if not args.entrypoint.is_file() or not (args.module_dir / 'orca').is_dir():
        parser.error('Provide the verified Orca entrypoint and Python module directory')
    args.prefs_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    args.debug_log.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    sys.path.insert(0, str(args.module_dir.resolve()))
    import orca.speech  # pylint: disable=import-outside-toplevel
    # Log actual generated announcements without sending audio to the host.
    orca.speech.init = lambda: None
    sys.argv = [str(args.entrypoint), '--disable', 'braille', '--user-prefs',
                str(args.prefs_dir), '--debug-file', str(args.debug_log)]
    launcher = runpy.run_path(str(args.entrypoint), run_name='isolated_orca')
    entry = launcher['main']
    # A host reader can coexist with this private session. Never replace it.
    entry.__globals__['otherOrcas'] = lambda: []
    return entry()


if __name__ == '__main__':
    raise SystemExit(main())
