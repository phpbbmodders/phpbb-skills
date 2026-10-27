# Authoritative references

## Fetching is mandatory and gated

Fetch every **Required** row below **before** running any check. This is a hard
gate, not a suggestion:

- Check the 24-hour cache first (below); a cached copy under 24 hours old
  satisfies the requirement without a network call.
- **Then try the local clone.** R1, R2, R3 and R5 all have a local source — see
  the table. A failed fetch is not a reason to give up on a reference that is
  sitting on disk.
- Fetch them one at a time, and after each one record its ledger row (below)
  immediately. Do not batch the fetches and do not defer the ledger.
- **Do not begin Step 4 (the checklist) until the ledger has a row for every
  Required reference.** If you find yourself reading extension code with an
  incomplete ledger, stop and finish the fetches.
- **Do not write the report** until the ledger is complete. It is published in
  the coverage notes after the report, not inside the report itself.
- Never skip a fetch because you believe you already know the document's
  contents. Your recollection of phpBB documentation is not a substitute, is
  frequently wrong about 3.3 specifics, and cannot be quoted.
- If a fetch fails or no fetch tool exists, fall back to the local clone before
  recording anything as `failed`. Only when both the cache and the local source
  are unavailable is the row `failed`/`unavailable`, and then add the single
  "verification was incomplete" line to the report and drop every
  guideline-citation finding to `[valinfo]` with no `[url=]` quote.

## The references

Each reference has three possible sources, tried in this order: **the 24-hour
cache**, then **a local repository clone**, then **the network**. Prefer local
reads — they need no approval prompt, cannot fail offline, and for R1/R3 they are
the source the published page is generated from.

| # | Purpose | Required | Local source (preferred) | Network fallback |
| --- | --- | --- | --- | --- |
| R1 | Coding guidelines | yes | `<docs_clone>/development/development/coding_guidelines.rst` | https://raw.githubusercontent.com/phpbb/documentation/3.3.x/development/development/coding_guidelines.rst — rendered at https://area51.phpbb.com/docs/33x/coding-guidelines.html |
| R2 | Extensions validation policy | yes | `<website_clone>/templates/extensions/validation-policy.html.twig` | https://www.phpbb.com/extensions/rules-and-policies/validation-policy/ |
| R3 | Core events list (with its "Added in" column) | yes | `<docs_clone>/development/extensions/events_list.rst` | https://raw.githubusercontent.com/phpbb/documentation/3.3.x/development/extensions/events_list.rst |
| R4 | Canonical `license.txt` | yes | none — no local clone of the skeleton | https://raw.githubusercontent.com/phpbb-extensions/phpbb-ext-skeleton/master/skeleton/license.txt.twig |
| R5 | Template events list | if templates shipped | `<phpbb_clone>/phpBB/docs/events.md` | https://area51.phpbb.com/docs/33x/events.html |
| R6 | Extension skeleton layout | if packaging looks odd | none | https://github.com/phpbb-extensions/phpbb-ext-skeleton |

The clone paths come from `config.json` (see `core-verification.md`):

```json
{
  "phpbb_clone":   "D:/src/phpbb/phpbb",
  "docs_clone":    "D:/src/phpbb/documentation",
  "website_clone": "D:/src/phpbb/phpbb-website-private"
}
```

### Notes on each local source

- **R1 and R3 live in `phpbb/documentation`, and only on branch `3.3.x`.** Note
  the doubled directory in R1's path — `development/development/` — it is correct.
  Before reading either, confirm the clone's branch by reading
  `<docs_clone>/.git/HEAD`; it must say `ref: refs/heads/3.3.x`. On any other
  branch those files are absent or belong to the wrong version, so fall back to
  the raw URL and mark the ledger row accordingly rather than reading whatever
  the working tree happens to hold. Do not switch the branch yourself.
- **R2 is the source of the published policy page**, a Twig template in the
  website repository. Read the prose and ignore the surrounding Twig and HTML
  markup. Being a private repository, it has no public raw URL — the network
  fallback is the rendered page.
- **R5** comes from the phpBB source clone and needs no branch gymnastics beyond
  the `3.3.x` check already performed in step 3.
- **R4 and R6** have no local source unless someone clones
  `phpbb-extensions/phpbb-ext-skeleton`. If a `skeleton_clone` key appears in
  `config.json`, R4 is `<skeleton_clone>/skeleton/license.txt.twig`.

A local read is a `local` ledger row, with the file's path and its line or entry
count as the proof column. It satisfies the fetch gate exactly as `fetched` does.

## 24-hour cache

These documents change rarely, so cache them and reuse a copy that is under 24
hours old. This removes the main excuse for skipping a fetch and makes repeat
validations fast.

Cache directory (create it if absent — it is outside the extension tree, so
writing here does not breach the read-only constraint):

- Windows: `%LOCALAPPDATA%\phpbb-extension-validation\references\`
- macOS / Linux: `${XDG_CACHE_HOME:-$HOME/.cache}/phpbb-extension-validation/references/`

One file per reference, named by id and extension: `R1.html`, `R2.html`,
`R3.rst`, `R4.txt`, `R6.html`. R5 is read from the clone and is not cached —
cache `R5.html` only when falling back to the remote page.

Procedure per reference:

1. If the file exists and its modification time is **less than 24 hours old**,
   read it from disk. Ledger status is `cached (<age>)`, e.g. `cached (3h)`.
2. Otherwise fetch the URL, write the body to the cache path, and use it. Ledger
   status is `fetched`.
3. If the fetch fails but a **stale** cache file exists, use the stale copy and
   mark the row `stale cache (<age>)` in the ledger; treat quotations from it as
   valid but note the age. A stale copy beats no reference.
4. If the fetch fails and there is no cache file, the row is
   `failed: <reason>`.

Checking age:

```bash
# Windows (PowerShell)
(Get-Item $env:LOCALAPPDATA\phpbb-extension-validation\references\R1.html).LastWriteTime

# POSIX
find "$HOME/.cache/phpbb-extension-validation/references" -name 'R1.html' -mmin -1440
```

Do not hand-edit cached files, and do not cache anything else there. If a cached
copy looks truncated or is not the expected document, delete it and re-fetch
rather than working from it. To force a refresh, delete the directory.

Alongside the cache, `config.json` in the parent directory remembers the local
`phpbb/phpbb` clone path between runs — see `core-verification.md`. Deleting the
reference cache does not discard it.

## The reference ledger

Build this as you fetch, and reproduce it verbatim in the coverage notes that
follow the report:

```
R1 coding guidelines      local         docs_clone development/development/coding_guidelines.rst
R2 validation policy      local         website_clone templates/extensions/validation-policy.html.twig
R3 events list            local         <N> events, docs_clone development/extensions/events_list.rst
R4 license.txt            cached (3h)   <line count> lines
R5 template events        local         <N> events, phpbb_clone phpBB/docs/events.md
```

Status is one of `fetched`, `cached (<age>)`, `local` (read from the clone),
`stale cache (<age>)`, `failed: <reason>`, `n/a: <reason>`, or
`unavailable: no fetch tool`. `cached` and `local` satisfy the gate; `failed`
does not.

The third column is proof you actually read the document, so it must come from
the text you read — a short verbatim phrase from the section you relied on, or a
concrete count. Do not write a paraphrase or a generic label there. If you cannot
produce it, the row is not `fetched`.

## What each reference is for

- **R1 coding guidelines** — the only source you may quote for a style or
  convention finding. Sections you will actually use: file layout, naming,
  indentation/brace style, SQL formatting, and the language/localisation rules
  behind every hard-coded-text denial.
- **R2 validation policy** — what the team may deny for. Check your deny list
  against it; if the policy does not support a denial, downgrade it.
- **R3 events list** — event names and, importantly, the **"Added in"** column
  used for the minimum-version check in `core-verification.md`. If `config.json`
  names a `docs_clone` on `3.3.x`, read
  `<docs_clone>/development/extensions/events_list.rst` from disk instead of
  fetching, and mark the row `local`. Otherwise prefer the
  `raw.githubusercontent.com` form, which succeeds more often than the rendered
  blob page.
- **R4 license.txt** — the reference for confirming the extension's copy is a
  legitimate GPL-2.0-only license. It is a reference point, not a byte-exact
  target: ignore whitespace, line endings, and harmless standard GPL-2.0 text
  outside the template. See checklist item 5.
- **R5 template events** — validates `EVENT` names in shipped templates, and its
  `Since:` field gives the introducing version for the minimum-version check,
  exactly as R3's "Added in" column does for PHP events. Read from
  `<clone>/phpBB/docs/events.md`.
- **R6 skeleton** — the reference layout when packaging looks unusual.

## Quoting rule

A `[url=]` quotation in a finding is only permitted when that document's ledger
row says `fetched`, `cached`, or `stale cache` **and** the quoted words appear in
the text you read.
Before writing the report, re-check every quotation against the fetched text and
delete any you cannot match. Never reconstruct a quote from memory, and never
quote a document whose row is `failed`, `n/a`, or `unavailable`.

## Local phpBB clone

A grep-able local `phpbb/phpbb` clone on `3.3.x` is **expected input**, not an
optional extra — it is the only way to confirm that a core event, service, class,
method, constant, or permission exists, what an event exposes, and which release
introduced it. The GitHub tree cannot be grepped, so absence cannot be proven
online.

See `core-verification.md` for the full procedure: obtaining and validating the
clone, building the symbol inventory, resolving it, checking the minimum-version
floor, and reporting coverage.

## Files in `language/`

Everything under `language/` is user-facing text. Treat every value there as a
string that may be rendered into HTML, a JS string, or an HTML attribute, and
check escaping at the point of use.
