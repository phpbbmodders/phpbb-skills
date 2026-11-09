# phpBB Modders extension conventions

The Modernize step compares the extension against this list and changes only what differs. Keep a change that the repository intentionally does differently, and say so in the plan.

## Code and package

- **File headers:** `<Name> extension for the phpBB Forum Software package`, then every original `@author` and `@copyright` line unchanged, then `@copyright (c) <year>, phpBB Modders, https://www.phpbbmodders.com/`, then `@license GNU General Public License, version 2 (GPL-2.0)`. Keep free-text lines such as translator credits.
- **composer.json:** homepage `https://www.phpbbmodders.com/`, license `GPL-2.0-only`, phpBB Modders first as `Extension Developer` (email `board@phpbbmodders.com`), earlier authors as `Past Developer`. Description matches the GitHub repository description and the README's first line. `require.php` and `extra.soft-require.phpbb/phpbb` match the organization's current minimums. Keep or add `extra.version-check` pointing at the extension's phpBB.com listing.
- **ext.php:** `is_enableable()` refuses below the phpBB and PHP minimums with a `<EXT>_NOT_ENABLEABLE` language string. A renamed extension also refuses while the old one is enabled, with a `<EXT>_DISABLE_OLD` string, and moves the old install's records on enable.
- **No donation material:** no `.github/FUNDING.yml` and no donation links, images or language strings from previous authors.
- **Cron tasks:** every task has a unique `set_name` call, `cron.task.<vendor>.<ext>.<task>`.
- **Uploaded files** live in the extension's own folder under the board's `store/`, never under `ext/`.

## Repository

- **CI:** `tests.yml` with the code sniffer and the organization's strict EPV workflow on phpBB `3.3.x` and `master`; `lint.yml` with `php -l` and `composer validate` on the minimum PHP and the newest.
- **Line endings:** `.gitattributes` with `* text=auto eol=lf` and `binary` rules for images; `docs/` and `.editorconfig` export-ignored. Store every text file with LF; normalize in its own commit when the change is large.
- **README:** Tests and Lint badges, one-line description, Features, Screenshots (three or four previews about 440 px wide, linked to `docs/images/screenshots/README.md`), Requirements, Installation with an "Upgrading from …" section after a rename, a TODO section only if `docs/TODO.md` exists, Contributing (issues for bugs, the organization's Discussions and community forum for everything else), Acknowledgments, License last.
- **GitHub settings:** description equal to the composer description; topics `php`, `phpbb`, `phpbb-extension` plus two to four about its purpose; the organization's standard label set when the repository's labels have never been used, otherwise added alongside; Projects off. Leave merge settings alone until the organization decides its merge policy.
