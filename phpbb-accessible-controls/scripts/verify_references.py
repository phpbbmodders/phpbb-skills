#!/usr/bin/env python3
"""Verify saved reference bytes against the local manifest; never use network.

Every manifest entry has a byte length and SHA-256. Entries marked
``"distribution": "local-only"`` (Apple and JAWS documents, whose publisher
terms restrict redistribution) are not kept in Git, so a missing copy is
reported but does not fail the check unless --require-local-only is given.
A copy that is present is always checked. Exit status is 0 when every
required document matches and 1 otherwise.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    """Return the parsed command-line options."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        '-r', '--require-local-only', action='store_true',
        help='fail when a local-only (Apple or JAWS) document is missing, '
             'instead of only reporting it')
    return parser.parse_args()


def main() -> int:
    """Return zero when every required document has its expected bytes."""
    args = parse_args()
    references = Path(__file__).resolve().parent.parent / 'references'
    missing_local = []
    try:
        manifest = json.loads((references / 'manifest.json').read_text())
        documents = manifest['documents']
        if manifest['schema_version'] != 1 or not documents:
            raise ValueError('Unsupported or empty reference manifest')
        for document in documents:
            path = (references / document['file']).resolve()
            if not path.is_relative_to(references.resolve()):
                raise ValueError('Reference path escapes the reference directory')
            local_only = document.get('distribution') == 'local-only'
            if local_only and not path.exists() and not args.require_local_only:
                missing_local.append(document['file'])
                continue
            data = path.read_bytes()
            if len(data) != document['bytes']:
                raise ValueError(f'Byte length mismatch: {document["file"]}')
            if hashlib.sha256(data).hexdigest() != document['sha256']:
                raise ValueError(f'SHA-256 mismatch: {document["file"]}')
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Reference integrity failed: {error}', file=sys.stderr)
        return 1
    verified = len(documents) - len(missing_local)
    print(f'Verified {verified} pinned reference documents.')
    if missing_local:
        print(f'{len(missing_local)} local-only Apple/JAWS documents are not '
              'present; use their publisher links (see '
              'references/screen-readers.md).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
