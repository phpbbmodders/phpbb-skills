#!/usr/bin/env python3
"""Check every skill folder in this repository without using the network.

For each */SKILL.md it checks the front matter (name matches the folder,
description present and at most 1024 characters), that relative Markdown
links in the skill's .md files resolve (links to files its reference manifest
marks local-only are skipped, since those are not in Git), and that its Python
scripts compile. Exit status is 0 when every check passes and
1 otherwise; each problem is printed on its own line.
"""
import argparse
import json
from pathlib import Path
import re
import sys

MAX_DESCRIPTION = 1024
NAME_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
LINK_PATTERN = re.compile(r'\]\(([^)\s]+)\)')


def parse_args() -> argparse.Namespace:
    """Return the parsed command-line options."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        '-r', '--root', type=Path,
        default=Path(__file__).resolve().parent.parent,
        help='repository root holding the skill folders (default: this '
             'script\'s parent repository)')
    return parser.parse_args()


def front_matter(text: str) -> dict[str, str]:
    """Return the top-level key/value pairs of a SKILL.md front matter block."""
    lines = text.split('\n')
    if not lines or lines[0].strip() != '---':
        raise ValueError('missing front matter')
    fields = {}
    for line in lines[1:]:
        if line.strip() == '---':
            return fields
        match = re.match(r'^([a-z_-]+):\s*(.*)$', line)
        if match:
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
                value = value[1:-1]
            fields[match.group(1)] = value
    raise ValueError('front matter is not closed with ---')


def local_only_files(folder: Path) -> set[Path]:
    """Return files a skill's reference manifest marks local-only (not in Git)."""
    manifest = folder / 'references' / 'manifest.json'
    if not manifest.exists():
        return set()
    documents = json.loads(manifest.read_text(encoding='utf-8'))['documents']
    return {(manifest.parent / document['file']).resolve()
            for document in documents
            if document.get('distribution') == 'local-only'}


def check_skill(folder: Path) -> list[str]:
    """Return the problems found in one skill folder."""
    problems = []
    skill_file = folder / 'SKILL.md'
    try:
        fields = front_matter(skill_file.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        return [f'{skill_file}: {error}']

    name = fields.get('name', '')
    description = fields.get('description', '')
    if name != folder.name:
        problems.append(f'{skill_file}: name "{name}" does not match folder "{folder.name}"')
    if not NAME_PATTERN.match(name):
        problems.append(f'{skill_file}: name must be lowercase words joined by hyphens')
    if not description:
        problems.append(f'{skill_file}: description is missing')
    elif len(description) > MAX_DESCRIPTION:
        problems.append(f'{skill_file}: description is {len(description)} characters '
                        f'(limit {MAX_DESCRIPTION})')

    local_only = local_only_files(folder)
    for markdown in folder.rglob('*.md'):
        if 'snapshots' in markdown.parts:
            continue
        for target in LINK_PATTERN.findall(markdown.read_text(encoding='utf-8')):
            if re.match(r'^[a-z]+:', target) or target.startswith('#'):
                continue
            path = (markdown.parent / target.split('#')[0]).resolve()
            if path in local_only:
                continue
            if not path.exists():
                problems.append(f'{markdown}: link target not found: {target}')

    for script in folder.rglob('*.py'):
        try:
            compile(script.read_text(encoding='utf-8'), str(script), 'exec')
        except SyntaxError as error:
            problems.append(f'{script}: does not compile: {error}')
    return problems


def main() -> int:
    """Check all skill folders and return the exit status."""
    root = parse_args().root
    folders = sorted(path.parent for path in root.glob('*/SKILL.md'))
    if not folders:
        print(f'No skill folders found under {root}', file=sys.stderr)
        return 1
    problems = [problem for folder in folders for problem in check_skill(folder)]
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f'{len(problems)} problems in {len(folders)} skills.', file=sys.stderr)
        return 1
    print(f'Checked {len(folders)} skills: no problems found.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
