# False-positive guard

Test every candidate finding against this list first. These are the mistakes that
make AI-generated validation reports unusable.

## Data-flow tests before calling something a vulnerability

1. **Is the value attacker-controlled?** Trace it to its origin. A constant, a
   value the developer typed, a board config set by an administrator, a value read
   back from a table only admins can write, or a language key is not user input.
   Say which one it is instead of reporting it.
2. **Does it reach a sink?** A variable that is only logged, only compared, or only
   assigned and never emitted or queried is not an XSS or injection.
3. **Is it already typed?** `$request->variable('id', 0)` is an integer. Using it
   directly in SQL is correct and needs no `sql_escape`. Same for explicit
   `(int)`/`(bool)` casts.
4. **Is escaping happening downstream?** Twig autoescapes by default in phpBB 3.3.
   A raw value assigned with `assign_var()` and rendered as `{{ VAR }}` is escaped.
   Only `|raw`, `autoescape false`, attribute/JS contexts, and legacy
   `assign_var(..., $html)` paths need attention.
5. **Is the SQL built by DBAL?** `sql_build_array()`, `sql_in_set()`,
   `sql_build_query()`, and `$db->sql_escape()` are safe. Don't ask for PDO
   prepared statements; phpBB does not use them here.
6. **Is CSRF actually reachable?** A read-only page, a form whose handler calls
   `check_form_key()` elsewhere in the same method, and `confirm_box()` flows all
   count as protected. Check the whole method, not the first ten lines.
7. **Is authorization enforced by the module?** An ACP module's `auth` string in
   `*_info.php` protects every mode of that module. Don't report a missing
   `acl_get()` without checking the module definition and any parent controller.

## phpBB-specific things that are correct and often misreported

- `$table_prefix` / `%core.table_prefix%` concatenated into a table name.
- `array_merge($lang, array(...))` in language files.
- Tabs for indentation and Allman brace style — that *is* the phpBB standard.
- `global $phpbb_root_path, $phpEx;` in a non-namespaced file.
- `.$phpEx` file extension concatenation.
- `append_sid()` output used directly in a template.
- Migrations without `effectively_installed()` — it is optional.
- Migrations without a `revert_data()` — phpBB auto-reverses most
  `update_data()` tool calls.
- A listener class with no interface beyond `EventSubscriberInterface`.
- `@var` docblocks on injected services instead of native property types (3.3
  supports PHP 7.1+).
- No `declare(strict_types=1)` — phpBB does not use it.
- Long language key names, or keys that read as sentences.
- Minor or non-substantive differences in `license.txt` — whitespace, line
  endings, the FSF's postal address or its URL form, or other harmless standard
  GPL-2.0 text that is not in the skeleton template. Report a license issue only
  when the file is materially different from, or clearly not, GPL-2.0-only.
- `styles/prosilver/theme/*.css` overriding core classes for the extension's own
  markup.

## Reporting discipline

- **Never assert that a `core.*` event, service id, or core method does not exist
  without having grepped the 3.3.x source** — see `core-verification.md`. Fetching
  a GitHub tree page does not count; you cannot prove absence that way. If you
  could not check, write "unverified — confirm against 3.3.x" and mark it
  `[valinfo]`.
- A core symbol that exists but is *newer* than the `soft-require` floor is a real
  finding, not a false positive — but state the release that introduced it and how
  you established that, or mark it unverified.
- **Never fabricate a quotation** from the coding guidelines or validation policy.
  Quote only text you actually fetched; otherwise describe the rule in your own
  words with a link and no `[quote]`.
- Do not report the same underlying issue once per occurrence. Report it once with
  the clearest example and list the other locations.
- **Do not report style preferences the guidelines do not state.** This is the
  most common source of unsupported findings. Before writing a style or
  convention finding, ask which line of R1 states the rule. If the answer is
  "it's just better practice", "most PHP projects do it this way", or "another
  framework requires it", drop the finding. The phpBB standard is what R1 says,
  not what good PHP generally looks like.
- Do not report the absence of things phpBB does not require: unit tests,
  changelogs, semantic versioning, docblock coverage, `declare(strict_types=1)`,
  PSR-12 compliance, a clean static-analysis run, CI configuration.
- Do not review third-party libraries, minified bundles, or vendored code
  line-by-line. Note their presence and that they were not audited.
- Do not comment on files with no issues, and do not pad the report with a
  "looks good" section per file.
- Do not report missing docblocks, missing tests, or absent CI as findings.
- **Do not reach for version control.** The extension is an extracted archive, so
  there is no history, no diff, and no "changed files" to scope the review to.
  Review the whole fileset as shipped. Never justify a finding with what a commit,
  branch, or tag appears to say, and never report a *missing* `.gitignore`,
  changelog, or release tag — their absence is not a defect. A `.git/` directory
  that *is* present is only a packaging finding, not something to inspect.
- If the extension is small and genuinely clean, a short report with no findings is
  the correct output.

## Logic findings need a failing case

Section L is the easiest place to generate confident nonsense, because a
misreading of control flow looks exactly like a bug. One test governs every
logic finding:

**Name the input, the state, or the sequence that makes it fail, and say what
goes wrong.** "Off-by-one on the last page when the total is an exact multiple of
the page size, so the final row is never shown" is a finding. "The pagination
logic looks suspect" is not.

- If you cannot construct that case, you have a suspicion. Drop it.
- Read the whole function, and the callers, before concluding a variable is
  unset or a branch unreachable — guard clauses and early returns higher up are
  the usual explanation.
- Do not report a defect that depends on a caller that does not exist in the
  package, unless the method is public API an author could plausibly call.
- Do not report a security-logic defect (L-b) without tracing the actual branch
  taken: `!$auth->acl_get()` guarding an error path is correct, and the same
  expression guarding the action is a denial. Which one is it?
- Unless it is a security-control failure or a guaranteed fatal, a logic finding
  is `[valinfo]` and says it needs confirmation by hand. You are reading, not
  running.

## The opposite failure: under-reporting

This file exists to stop invented findings, not to excuse a shallow pass. Do not
use it to talk yourself out of real ones.

- A pass whose findings are only packaging, metadata, compatibility or style has
  probably not looked at authorization, CSRF or admin-text localization. That is
  under-reporting, and it is the more common failure on extensions with an ACP
  module.
- "I could not confirm it is exploitable" is not a reason to drop a missing
  `check_form_key()` or a privileged action with no `acl_get()`. Absence of a
  required control is the finding; you do not need a working exploit.
- A blank cell in the section S surface table is not a pass. It means unchecked.
- `na` on a checklist item means the item genuinely does not apply, not that you
  did not get to it.
- An existing denial is not a reason to stop looking. The verdict is settled long
  before the review is finished, and everything you skip after that point becomes
  a second rejection round for the author.
