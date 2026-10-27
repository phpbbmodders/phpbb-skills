# phpBB Skills

[![CI](https://github.com/phpbbmodders/phpbb-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/phpbbmodders/phpbb-skills/actions/workflows/ci.yml)

Agent skills for phpBB extension, language pack, documentation, and core development work.

Each folder is a skill: a `SKILL.md` with instructions an AI coding agent loads when a request matches its description, plus any reference files and scripts it needs. They follow the [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) folder format.

## Skills

### Extensions

| Skill | Use it for |
| --- | --- |
| [phpbb-test-boards](phpbb-test-boards/SKILL.md) | Disposable test boards with seed-forum and phpbb-test-board: runtime, lifecycle, PHPUnit and database checks. |
| [phpbb-cross-version-compatibility](phpbb-cross-version-compatibility/SKILL.md) | Making an extension work on both phpBB 3.3.x and 4.0. |
| [phpbb-extension-validation](phpbb-extension-validation/SKILL.md) | Validating an extension for the phpBB Customisation Database, with a BBCode report. |
| [phpbb-php-support-changes](phpbb-php-support-changes/SKILL.md) | Changing an extension's supported PHP versions consistently. |
| [phpbb-extension-screenshots](phpbb-extension-screenshots/SKILL.md) | Board and ACP screenshots, README previews and galleries. |
| [phpbb-extension-releases](phpbb-extension-releases/SKILL.md) | Packaging, publishing and checking extension releases. |
| [phpbb-development-topics](phpbb-development-topics/SKILL.md) | phpBB.com development topic announcements and update posts. |
| [phpbb-extension-adoption](phpbb-extension-adoption/SKILL.md) | Taking over an extension or changing its vendor without breaking existing installs. |
| [phpbb-export-verification](phpbb-export-verification/SKILL.md) | Checking personal data exports and static archives before release. |

### Accessibility

| Skill | Use it for |
| --- | --- |
| [phpbb-accessible-controls](phpbb-accessible-controls/SKILL.md) | Accessible board and ACP controls: icon labels, focus, feedback, keyboard use. |
| [accessibility-toolkit-setup](accessibility-toolkit-setup/SKILL.md) | Setting up Playwright and axe checks, contrast review, and isolated Linux Orca testing. |

### Core, language packs and documentation

| Skill | Use it for |
| --- | --- |
| [phpbb-core-bugfixes](phpbb-core-bugfixes/SKILL.md) | Reproducing and fixing phpBB core bugs with regression tests. |
| [phpbb-event-rfc-to-pr](phpbb-event-rfc-to-pr/SKILL.md) | Turning a core event request into a tracker ticket and a phpbb/phpbb pull request. |
| [phpbb-language-pack-releases](phpbb-language-pack-releases/SKILL.md) | Validating and packaging a language pack for the Customisation Database. |
| [phpbb-docs-translations](phpbb-docs-translations/SKILL.md) | Translating the phpBB documentation with the phpbbdocs gettext workflow. |

## Requirements

Several skills drive tools from other phpBB Modders repositories. Clone the ones you need:

- [phpbb-release-tools](https://github.com/phpbbmodders/phpbb-release-tools): release scripts, `phpbb-test-board` and screenshots.
- [seed-forum](https://github.com/phpbbmodders/seed-forum): test boards with standard fixtures.
- [phpbbdocs-hugo](https://github.com/phpbbmodders/phpbbdocs-hugo) and [phpbbdocs-languages](https://github.com/phpbbmodders/phpbbdocs-languages): documentation translation.

## Installation

Copy the skill folders you want into your agent's skills directory. For Claude Code, that is `~/.claude/skills/` for all projects, or `.claude/skills/` inside one project:

```bash
git clone https://github.com/phpbbmodders/phpbb-skills.git
cp -r phpbb-skills/phpbb-test-boards ~/.claude/skills/
```

Copy `phpbb-accessible-controls` and `accessibility-toolkit-setup` together; the first links to the second.

## Accessibility reference documents

`phpbb-accessible-controls` works from a fixed set of saved documents listed in [its manifest](phpbb-accessible-controls/references/manifest.json) with their sources and SHA-256 hashes:

- **Included:** WCAG 2.2, WAI-ARIA 1.2, Accessible Name 1.1, ARIA Authoring Practices 1.2, and the NVDA 2026.2 User Guide and Commands Quick Reference with NVDA's licence.
- **Not included:** the Apple VoiceOver pages and the JAWS help, because their publishers' terms restrict redistribution. The manifest keeps their links. The skill works without them; see [the screen-reader references](phpbb-accessible-controls/references/screen-readers.md) for how to get your own copies.

## Checks

```bash
python3 tools/check-skills.py
python3 phpbb-accessible-controls/scripts/verify_references.py
tools/route-test.sh -c tools/route-cases.tsv
```

- `check-skills.py` checks each skill's front matter, relative links and Python scripts. CI runs it with the reference hash check on every push and pull request.
- `verify_references.py` checks the saved accessibility documents against their hashes. Add `--require-local-only` if you keep the Apple and JAWS copies, so a missing one is reported as a failure.
- `route-test.sh` sends each request in [`tools/route-cases.tsv`](tools/route-cases.tsv) to a headless Claude Code session that has only the Skill tool, and reports whether the expected skill was chosen. Run it after changing a description. It needs a signed-in `claude` CLI and uses normal model quota.

## Contributing

Contributions are welcome!

- **Bug reports**: [Open an issue](https://github.com/phpbbmodders/phpbb-skills/issues).
- **Everything else** (questions, feature requests, ideas, general discussion): [Use Discussions](https://github.com/phpbbmodders/phpbb-skills/discussions).
- Pull requests are welcome for bug fixes or discussed features.

## Acknowledgments

- Skills drafted with [OpenAI Codex](https://openai.com/codex/).
- Code review, bug fixes, and documentation assisted by [Claude](https://www.anthropic.com/claude).

## License

This project is licensed under the **GNU General Public License v2.0**.

See [LICENSE](LICENSE) for more information. The saved reference documents in `phpbb-accessible-controls/references/snapshots/` keep their own licences and notices: the W3C documents are under the W3C Document License, and the NVDA documents are under NVDA's licence (GPL v2 or later), [included](phpbb-accessible-controls/references/snapshots/nvda-2026.2-copying.txt).
