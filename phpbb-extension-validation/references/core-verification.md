# Verifying the extension against the phpBB codebase

Existence claims — "this event does not exist", "this service id is wrong", "this
method was removed" — are the findings most likely to be wrong and most damaging to
the report's credibility. Never make one from memory. Resolve it against real
3.3.x source or mark it unverified.

## 0. Prefer file reads over shell commands

**Do this verification with plain file reads. Do not reach for a shell.**

Almost everything here can be answered by opening files at known paths, and on
most hosts a shell command triggers an approval prompt for every invocation — a
review that shells out fifty times asks the reviewer fifty questions, which is
worse than useless. File reads are silent, faster, and available everywhere.

Use a shell only for the one thing file reads cannot do: establishing which
release first contained a PHP core event, via `git log -S`. If no shell is
available, that single check degrades to `unverified` (§0.3) and nothing else is
lost.

The `git` commands shown later in this file are reference forms for hosts where a
shell is free. Where it is not, use §0.1 and §0.2 instead — they answer the same
questions. "No shell" is not "no verification".

Check once, before you start, whether you can read files under the clone path at
all. If you cannot, say so and use §0.3. Do not discover a missing capability in
the middle of the sweep and then give up.

### 0.1 Revision — two file reads, no `git`

The short SHA and branch are plain files inside the clone:

- `<clone>/.git/HEAD` contains e.g. `ref: refs/heads/3.3.x` — that is the branch.
- `<clone>/.git/refs/heads/3.3.x` contains the full 40-character SHA. The first
  seven characters are the short SHA.
- If that ref file is absent the ref is packed: read `<clone>/.git/packed-refs`
  and find the line ending `refs/heads/3.3.x`.

That answers "which revision am I verifying against" with two file reads. There
is no excuse for reporting the revision as unavailable when the clone path is
known.

### 0.2 Symbol resolution — known paths, no grep

phpBB's layout is predictable, so symbols resolve by reading known files
directly. This is the primary route, not a workaround:

| Symbol | Read |
| --- | --- |
| Template event + its `Since:` | `<clone>/phpBB/docs/events.md` — one entry per event |
| Core constant / table constant | `<clone>/phpBB/includes/constants.php` |
| Service id | `<clone>/phpBB/config/**/*.yml` — the file names say which area |
| Class or method | `<clone>/phpBB/phpbb/<namespace path>.php`, derived from the class name |
| Core function | `<clone>/phpBB/includes/functions.php` and `functions_*.php` |
| Permission | `<clone>/phpBB/language/en/acp/permissions_phpbb.php` |
| PHP core event | the file named in the event's own prefix — `core.viewtopic_*` lives in `viewtopic.php`, `core.acp_users_*` in `includes/acp/acp_users.php`, and so on |

That last row is the one worth persisting with: a `core.*` event name encodes
where it is dispatched, so you can open that file and search within it even when
you cannot search across the tree.

If the host can open files by absolute path outside the workspace, this is all
available. If it cannot open the clone at all, say so plainly and use §0.3.

### 0.3 When a reference cannot be fetched

The clone outranks the documentation. If R3 (the PHP events list) cannot be
fetched:

- **Existence** is still verifiable — the event is in the source, per §0.2.
- **Introduction version** is the part you lose, because that comes from R3's
  "Added in" column or from `git log`. Without either, mark the minimum-version
  check `unverified` for PHP events and say so. Do not guess, and do not silently
  drop the check.
- Template events keep their `Since:` from `events.md`, so that half of the
  version check still works.

## 1. Obtain the reference source (do this before Step 3)

A `phpbb/phpbb` checkout you can read is expected input, not an optional extra —
it is the only way to verify the symbol inventory below. Resolve its path in this
order and stop at the first that yields a valid clone. **Only ask the user if
every other route fails** — nobody should have to retype this path on every run.

1. **Remembered path.** Read `phpbb_clone` from the config file:
   - Windows: `%LOCALAPPDATA%\phpbb-extension-validation\config.json`
   - macOS / Linux: `${XDG_CONFIG_HOME:-$HOME/.config}/phpbb-extension-validation/config.json`

   ```json
   {
     "phpbb_clone":   "D:/src/phpbb/phpbb",
     "branch":        "3.3.x",
     "recorded":      "2026-09-18",
     "docs_clone":    "D:/src/phpbb/documentation",
     "website_clone": "D:/src/phpbb/phpbb-website-private"
   }
   ```

   `docs_clone` and `website_clone` remove the network from the reference step:

   - `docs_clone` — `phpbb/documentation` **on branch `3.3.x`** — supplies R1
     from `development/development/coding_guidelines.rst` (the doubled directory
     is correct) and R3 from `development/extensions/events_list.rst`. Check
     `<docs_clone>/.git/HEAD` first: on any branch other than `3.3.x` those files
     are absent or the wrong version, so use the network form instead. Do not
     switch the branch yourself.
   - `website_clone` — `phpbb-website-private` — supplies R2 from
     `templates/extensions/validation-policy.html.twig`, the source of the
     published policy page. Read the prose, ignore the Twig and HTML markup.

2. **Your own persistent memory**, if this agent has one — a stored note such as
   "local phpBB 3.3.x clone lives at …". Treat it as a hint to validate, not as
   fact: a remembered path may have moved or been deleted.
3. **Probe the obvious locations** before asking. Anything matching
   `*/phpbb/phpbb`, `*/phpbb3`, or a sibling of the extension's own parent
   directory, e.g. `~/src/phpbb/phpbb`, `D:/src/phpbb/phpbb`, `~/code/phpbb`,
   `/var/www/phpbb`.
4. **Ask the user** and wait for an answer.

### Validate whatever you found

A path only counts as a usable clone when all four of these hold, and all four
come from file reads:

- `<path>/.git/` exists — a real checkout
- `<path>/phpBB/includes/constants.php` exists — actually phpBB, not a fork of
  something else
- `<path>/.git/HEAD` names the branch — expect `refs/heads/3.3.x`
- `<path>/.git/refs/heads/3.3.x` holds the SHA — first seven characters are the
  short SHA for the coverage notes

With a free shell the equivalents are `git -C <path> rev-parse --abbrev-ref HEAD`
and `git -C <path> log -1 --format='%h %ci'`, but prefer the reads. Never treat
the absence of `git` as the absence of a clone.

If a remembered or probed path fails validation, say so in one line, fall through
to the next source, and do not silently proceed without a clone.

### Remember it for next time

Once a path validates, write it to the config file above — create the file and its
directory if needed, and preserve any other keys already there. Record the path,
the branch you saw, and today's date. If the config already holds that same path,
leave it alone.

If the agent also has persistent memory, store the path there as well so it
survives a lost config file, but always re-validate on use.

The config file lives outside the extension tree, so writing it does not breach
the read-only constraint. It holds paths only — never extension contents or
findings.

### The clone also supplies R5

Once the clone path is known, read `<clone>/phpBB/docs/events.md` for the
template-events list and complete R5's ledger row with status `local` and the
event count. Do not fetch the area51 events page when a clone is available — the
in-repo file is authoritative for that exact revision and carries the `Since:`
versions.

### State it in the coverage notes

The coverage notes' `Core symbols verified` line names the clone path and short
sha, so a reviewer can see which checkout the conclusions came from. Note when the
path came from a remembered value rather than something the user supplied this
run. The posted report carries none of this — only a single line when
verification was incomplete.

### If the branch is wrong

If the clone validates but is not on `3.3.x`, ask before using it — do not switch
the branch yourself (you must not modify anything, and it may be the user's
working checkout with uncommitted changes). A `3.2.x` or `master` checkout will
give wrong answers about both existence and introducing release.

### If there is no clone at all

This means the clone is genuinely unreachable — not merely that `git` or
recursive search is unavailable. Work through §0 before concluding this.

Without a clone, state it plainly: **verification is unavailable.** The GitHub
tree cannot be grepped, so you cannot prove a symbol's absence. In that mode:

- You may still confirm a symbol is *present* by fetching a specific known file.
- You must **never** report that a symbol does not exist. Every such finding is
  downgraded to `[valinfo]` prefixed `unverified — confirm against 3.3.x`.
- The coverage notes must say `Core symbols verified: 0/M — unavailable`, and
  the report itself carries the one line saying verification was incomplete.

## 2. Build the symbol inventory

Grep the **extension** first and collect every core symbol it depends on into one
table, then resolve the table in a single pass. Do not verify ad hoc as you read.

| What | Find it in the extension with |
| --- | --- |
| PHP core events | `grep -rn "'core\.\|\"core\." <ext>` and every `getSubscribedEvents()` return |
| Template events | `grep -rn "EVENT " <ext>/styles` |
| Service ids consumed | `grep -rn "@" <ext>/config/*.yml`, plus `$container->get()` / `$phpbb_container->get()` calls |
| Core classes & interfaces | `grep -rn "use \\\\phpbb\|\\\\phpbb\\\\" <ext>` |
| Core functions | `grep -rnoE "\b(add_form_key|check_form_key|confirm_box|generate_link_hash|check_link_hash|append_sid|build_url|meta_refresh|trigger_error|phpbb_...)\(" <ext>` — and any other bare function call not defined in the extension |
| Core constants & tables | `grep -rnoE "\b[A-Z_]{4,}\b" <ext>` filtered to ones the extension does not define |
| Core permissions | every `acl_get`/`acl_gets` argument and every `auth` string in `*_info.php` |
| Migration dependencies | every `depends_on()` entry |

Record the total as **M**.

## 2b. The extension's own definition inventory

The symbol inventory above resolves what the extension borrows from core. This one
resolves what it defines for itself, and it exists because a whole class of defect
is invisible without it: you cannot notice a variable that was never assigned, or
a cache that was never purged, unless you first listed the assignments and the
caches. Reading file-by-file will not surface these — enumerate, then check.

Build three lists.

### Variables, properties and methods

For each class and each method, list what it **uses** and what it **defines**,
then subtract:

- every `$variable` read in a method, against the parameters, the assignments on
  the path leading there, and `global` imports
- every `$this->property` read, against the declared properties of the class and
  its parents
- every `$this->method()` call, against the methods of the class and its parents
- every array key read from `$this->` state or from an argument, against where
  that array is populated

Anything used but never defined is a defect. Report it with the method name and
the path on which the definition is missing. The archetype is a value used to
build a URL or an email variable that is simply never assigned on that path — no
error at compile time, a broken link at run time. Cross-reference L14, and N5 for
notification e-mail variables specifically.

Where a value is assigned only inside an `if`, say so: "defined only when
`$mode === 'add'`, read unconditionally at line N".

### Caches

List every cache the extension writes or invalidates: `$cache->put()`,
`$cache->get()`, `$cache->destroy()`, `$cache->sql_save()`, any custom cache
service, and any config value used as a cache stamp. Then list every action that
changes the underlying data, and check each one purges **all** the caches derived
from that data.

A purge that covers one cache and misses a sibling is the common shape, and it is
checkable only against this list. Name both caches and the action — see N14–N15.

### Language keys

List the keys the extension defines and the keys it uses, which E49–E51 already
require, and additionally diff the defined set against core's
`<phpbb_clone>/phpBB/language/en/**`. Collisions are E48a and are denials: the
last file loaded wins, so either core wording changes silently or the extension's
own text disappears, and the symptom shows up somewhere unrelated.

## 3. Resolve every entry

```bash
# PHP event: must appear in a trigger_event/dispatch call in core
grep -rn "core\.the_event_name" <clone>/phpBB --include=*.php

# and read the surrounding dispatcher call to get the exposed variables
grep -rn -B15 "core\.the_event_name" <clone>/phpBB --include=*.php

# template event: look it up in the clone's own events list (authoritative,
# 526-odd entries, each with Location: and Since:)
grep -n -A3 '^the_event_name$' <clone>/phpBB/docs/events.md
# cross-check that core actually ships the placeholder file
find <clone>/phpBB/styles -name 'the_event_name.html'

# service id
grep -rn "the.service.id" <clone>/phpBB/config

# class / method signature
grep -rn "function the_method" <clone>/phpBB/phpbb/path/to/class.php

# function
grep -rn "function the_function" <clone>/phpBB/includes <clone>/phpBB/phpbb

# constant / table constant
grep -rn "the_constant" <clone>/phpBB/includes/constants.php

# permission
grep -rn "'a_the_permission'\|u_the_permission" <clone>/phpBB
```

For an event, also confirm the handler only touches variables the dispatcher
actually passes — compare the `$vars` array in the core `trigger_event` call
against every `$event['...']` read and write in the listener. Reading an
unexposed key yields null; writing one is silently discarded.

Mark each entry resolved, missing, or unverified. Record resolved as **N**.

## 4. Check the minimum-version range

Existence in `3.3.x` HEAD is not enough. An extension whose `composer.json`
`extra.soft-require` allows an older 3.3 release but uses a symbol added later
will fatal on boards running that older release. This is a common real defect.

For each resolved event, service, or method, establish when it was introduced:

- For a **template** event, `<clone>/phpBB/docs/events.md` gives a `Since:`
  version per event (reference R5) — read it straight from the clone; it matches
  the revision you are verifying against.
- For a **PHP** event, the events list (reference R3, obtained in step 2)
  documents an **"Added in"** version — prefer it.
- Otherwise, in the clone:

```bash
git -C <clone> log --oneline -S 'core.the_event_name' --reverse -- phpBB | head -3
git -C <clone> tag --contains <first-commit-sha> | sort -V | head -1
```

Compare the earliest release containing it against the lowest phpBB version
`soft-require` permits. If the symbol is newer, that is a `[valdeny]`: either the
constraint must be raised or the code must degrade gracefully. Name both versions
in the finding.

Note that this uses git on the *reference clone*, which is a normal repository.
The extension under review is still an extracted archive and is never subject to
git commands.

## 5. Report coverage

State real numbers. "N/M: incomplete" is not a coverage report — it tells the
reviewer nothing about how much was verified or what would fix it. Give the
counts you actually reached, then name the missing capability and the remedy:

```
Core symbols verified: 34/41 against D:/src/phpbb/phpbb @ a1b2c3d (3.3.x)
  Unresolved (7): core.acp_users_mode_add, core.ucp_pm_view_messsage, ...
  Blocked by: no recursive search outside the workspace; introduction versions
  unverified because R3 could not be fetched.
  To fix: add the clone as a second workspace folder, or enable a terminal tool.
```

The coverage notes must carry one line:

```
Core symbols verified: <N>/<M> against <clone path> @ <short sha> (3.3.x)
```

or, with no clone:

```
Core symbols verified: 0/<M> — no local 3.3.x clone available; existence findings
are unverified.
```

If `N < M`, list the unresolved symbols beneath that line so a reviewer knows
exactly what to check by hand.
