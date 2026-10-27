---
name: phpbb-event-rfc-to-pr
description: Implement a phpBB core event request as a real PR once its tracker ticket is filed. Use when the user posts a tracker.phpbb.com/browse/PHPBB-XXXXX link for an event RFC (a docs/events/*.txt file in one of their phpBB extension repos) and wants the actual core change opened as a pull request against phpbb/phpbb. Also covers writing the RFC itself in tracker-submission format, and keeping the reference doc in misc/docs/phpbb-tracker-event-request-process.md current.
metadata:
  author: william
  version: "1.0.0"
---

# phpBB event RFC → PR

Turns a filed phpBB tracker ticket requesting a new/extended event into a real, working pull request against `phpbb/phpbb`, following the exact conventions phpBB core actually uses (verified against live merged PRs, not just the written docs).

Reference doc with the full written-up process: `misc/docs/phpbb-tracker-event-request-process.md`. Read it if you need the ticket-description format (Type/Location/Purpose/Use case/Variables) for drafting a new RFC — this skill is about the step *after* that, once a ticket is posted.

## When this applies

The user has (or is about to) post a `docs/events/*.txt` RFC to tracker.phpbb.com and gives you the resulting ticket ID or URL (`PHPBB-XXXXX`). They want you to do "the git work": implement it for real and open the PR, then hand back the PR URL for them to paste into the ticket's **GitHub Pull Request URL** field.

Do not start implementing before you have the actual ticket ID — the branch name, commit message, and PR title all depend on it.

## One-time setup

Check whether a fork of `phpbb/phpbb` already exists under the user's GitHub account (`gh repo view <user>/phpbb --json name,parent`). If not:

```bash
gh repo fork phpbb/phpbb --clone=false
```

Then clone it locally (into the user's repos directory, e.g. `~/Desktop/repos/phpbb`) if not already cloned:

```bash
git clone https://github.com/<user>/phpbb.git phpbb
cd phpbb
git remote add upstream https://github.com/phpbb/phpbb.git
```

If already cloned, just make sure `upstream` is fetched fresh before branching (see below) — don't assume the local checkout is current.

## Per-ticket workflow

1. **Read the live ticket** (`tracker.phpbb.com/browse/PHPBB-XXXXX`) rather than trusting the local RFC file might be stale — confirm Type, Location, Purpose, Use case, and Variables/template markup match what's posted.

2. **Pick the base branch:**
   - `master` — a genuinely new event where the relevant code has moved/restructured on master (e.g. classes that changed namespace since 3.3.x), or where the RFC targets 4.0-only behavior.
   - `3.3.x` — extending an existing event's variables, or a new template/PHP event on code that's unchanged between branches. This is the common case; verified against real merged precedent (`phpbb/phpbb#7046`, `#7052` both targeted `3.3.x` for new template events).
   Check which branch actually contains the `LOCATION` file/function before deciding — don't guess from the ticket text alone.

   ```bash
   git fetch upstream <branch> --depth=1
   git checkout -b <branch> upstream/<branch>   # once, if not already tracked locally
   git checkout <branch> && git checkout -b ticket/<id>
   ```

3. **Implement exactly what the ticket describes**, matching the LOCATION precisely (`grep`/`Read` the real file first — don't assume the RFC's line numbers or surrounding code are still accurate). Match the file's existing docblock/whitespace conventions exactly (tabs, alignment) rather than reformatting.

   - **New PHP event:** insert the `@event`/`@var`/`@since` docblock + `trigger_event()` call at the described point, using the same style as neighboring `trigger_event()` calls in that file (check one first for exact convention — spacing, `array(...)` vs `[...]`, etc.).
   - **Extending an existing event with a new variable:** add the var to both the docblock (`@var` line) and the `$vars` array, and add `@changed <version> Added <var_name> var` to the docblock — this is core's established convention for documenting an added variable (verified across `viewtopic.php`, `search.php`, `posting.php`, etc.), not a placeholder.
   - **New template event:** insert `{% EVENT event_name %}` (current Twig syntax — never the deprecated `<!-- EVENT name -->` HTML-comment form) at the exact described position, then hand-add an alphabetically-ordered entry to `phpBB/docs/events.md` in the same format as its neighbors (`* Locations:` / `* Since:` / `* Purpose:`). PHP events do **not** get a `docs/events.md` entry — their listing is auto-generated from the docblock.
   - **Determining `@since`/`@changed` version:** read the branch's actual version constant (`phpBB/includes/constants.php`, `PHPBB_VERSION`) to find the current tagged release, then use the next one — `X.Y.(Z+1)-RC1` on 3.3.x, `4.0.0-a(N+1)` on master (check the highest `@since 4.0.0-a*` already in the codebase to find N). Never leave `@since` as a "to be filled in" placeholder — older tutorials show that, but real merged PRs always ship a concrete guessed version.

4. **Validate:**
   ```bash
   php -l <file>
   phpcs --standard=build/code_sniffer/ruleset-php-strict-core.xml <file>
   ```
   If phpcs reports anything, diff it against the *unmodified* file on the target branch (`git show upstream/<branch>:<path> > /tmp/x.php && phpcs ... /tmp/x.php`) before treating it as a real problem — several core files carry long-standing pre-existing warnings (non-namespaced legacy classes, etc.) unrelated to any given change. Only new findings introduced by your diff matter.

5. **Commit** with the exact three-part format phpBB's tooling parses to auto-link the commit to the ticket:
   ```
   [ticket/<id>] <short title, matches ticket summary, <79 chars>

   <longer description of what changed and why, wrapped <79 chars>.

   PHPBB-<id>
   ```
   (Not `PHPBB3-<id>` — that prefix is from an outdated 2015-era tutorial; the current tracker uses plain `PHPBB-<id>`, confirmed against a live 2026 PR.)

   **The 79-char title limit is actually enforced by CI, not just convention** — `.github/workflows/tests.yml`'s `basic-checks` job runs a "Check commit message" step (`git-tools/commit-msg-hook-range.sh`) on every PR, which caught a real violation here (PHPBB-17725/26/27, all "PHP event + template event" tickets where packing both event names into one title line pushed it to 85-87 chars). A maintainer just relayed what that automated check reported — it wasn't a personal review judgment. Before committing, check every line including the title:
   ```bash
   git log -1 --format=%B | awk '{ if (length($0) > 79) print length($0)": "$0 }'
   ```
   If a combined PHP+template-event ticket makes the title too long, drop the ` + <template_event_name>` suffix from the title alone (e.g. `Add core.foo_modify_template_vars event`) — the template event is still named in full in the body, so nothing is lost. If this is caught only after the commit is already pushed (as happened here, via the automated check rather than manual review), `git commit --amend` and `git push --force-with-lease` on the same branch — do **not** open a new PR; a maintainer confirmed the branch/PR itself was fine, only the commit message needed fixing.

6. **Push and open the PR:**
   ```bash
   git push -u origin ticket/<id>
   gh pr create --repo phpbb/phpbb --base <branch> --head <user>:ticket/<id> \
     --title "Ticket/<id> <short title>" \
     --body "..."
   ```
   PR title is capitalized `Ticket/<id>`, no brackets — different from the commit message's `[ticket/<id>]`. Body follows the real checklist format:
   ```
   Checklist:

   - [x] Correct branch: master for new features; 3.3.x for fixes
   - [x] Tests pass
   - [x] Code follows coding guidelines: [master](https://area51.phpbb.com/docs/master/coding-guidelines.html) and [3.3.x](https://area51.phpbb.com/docs/dev/3.3.x/development/coding_guidelines.html)
   - [x] Commit follows commit message [format](https://area51.phpbb.com/docs/dev/3.3.x/development/git.html)

   Tracker ticket:

   https://tracker.phpbb.com/browse/PHPBB-<id>

   <short plain-English summary of what the event does and why, referencing sibling tickets/PRs if this is one of a related batch>
   ```

7. **Check CI briefly** (`gh pr checks <n> --repo phpbb/phpbb`) but don't block on it or treat a broken run as your fault by default — phpBB core's own CI is frequently red from pre-existing/unrelated failures (Psalm errors in untouched files, DB test-fixture flakiness). If checks fail, spot-check one or two logs to confirm they're unrelated to your diff (unrelated file, or failure that reproduces identically against the unmodified upstream file/branch — `git diff upstream/<branch> <your-branch> -- <path>` should be empty for any file you didn't touch) before reporting back — don't just assume, verify.

8. **On a `3.3.x`-targeted PR, always check the forward-merge-preview bot comment** — this step is mandatory, not optional cleanup:
   ```bash
   gh pr view <n> --repo phpbb/phpbb --json comments --jq '.comments[] | select(.author.login=="github-actions") | .body'
   ```
   `check_merge_to_master.yml` dry-runs merging `3.3.x` into `master` (phpBB's name for its 4.0 dev branch) with this PR included, and reports "Merge result: Success ✅" or "Conflict ❌ — A separate PR will be needed to merge `3.3.x` into `master`."

   **On Conflict, immediately open the second PR yourself — do not just note it and move on.** Confirmed directly by a phpBB maintainer: "You need to make a 2nd PR for the master too." Treat the bot's message as a literal to-do assigned to you, not a note that the core team will handle it later:
   1. Diff the file between branches at your edit location to see what actually diverged (`diff <(git show upstream/3.3.x:<path>) <(git show upstream/master:<path>)`) — don't assume the conflict means your `3.3.x` patch is wrong. Confirmed example: PHPBB-17725/26/27's `mcp_warn.php`/`mcp_notes.php` edits all conflicted because master had already replaced `phpbb_get_user_avatar()` — the exact line each event sat next to — with a new `avatar.helper` service, unrelated to any of those patches.
   2. `git checkout master && git checkout -b ticket/<id>-master` (the `-master` suffix is phpBB's real convention for this, seen in merged history).
   3. Reimplement the same event against master's current code at the same conceptual insertion point, adapting to whatever diverged (new service, moved code block, renamed variable, etc.) — re-derive the variables from what's actually available on master, don't just copy the 3.3.x diff.
   4. Repeat steps 4–7 (validate, commit referencing the same `PHPBB-<id>` and the first PR number, push, open PR targeting `master`) for this second PR.
   A ticket that touches diverged code isn't done after one PR — it's done when both the `3.3.x` PR shows a clean forward-merge (or never needed one) and, if it didn't, the `master` PR exists too.

9. **Report back**: give the user every PR URL from this ticket (one or two) and tell them explicitly to paste them into the ticket's **GitHub Pull Request URL** field(s) — don't do that step yourself, it's a tracker action on their account. Don't post PR comments, tracker comments, or anything else without separately showing the exact text and getting a yes first.

## Batching multiple RFCs

When the user has several `docs/events/*.txt` RFCs and posts multiple ticket links in sequence (one per message), treat each as its own independent run of steps 1–9 — same fork, same local clone, a fresh `ticket/<id>` branch off the right base each time. Don't bundle unrelated events into one PR even if they're thematically related (e.g. three MCP page events from the same extension) — each ticket gets its own branch, commit, and PR (and a second `-master` PR too, if step 8 finds a conflict), cross-linked in the PR body by ticket number when genuinely related.
