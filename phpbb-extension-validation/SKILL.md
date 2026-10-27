---
name: phpbb-extension-validation
description: Validate a phpBB 3.3 extension's source for security issues, coding-guideline violations, language-system misuse, and packaging problems, then emit a BBCode validation report with [valdeny]/[valinfo] findings and an Approve/Deny recommendation. Use when asked to validate, review, or audit a phpBB extension, an ext/ folder, or an extension archive submitted to the phpBB Extensions Database.
---

# phpBB Extension Validation

Read-only audit of a downloaded phpBB extension. You produce a report; you never
change the extension.

## What this task is

**This is a security review.** It also covers compatibility, structure, packaging
and style — secondary work, and not what the review is for.

The characteristic failure is doing the easier adjacent job instead: a
compatibility-and-structure scan that reads `composer.json`, checks the
migrations and service definitions, notes some spacing, confirms the events
exist, and stops. It feels complete because it produced findings. It is not a
validation, and it misses what matters — an ACP action with no permission check,
a form with no CSRF token, a delete link reachable by GET, admin text hard-coded
past the language system.

If you could describe your pass as "checking the extension is well-formed and
3.3-compatible", you have done the wrong task. Go back to checklist section S and
sections D and E.

Priorities, in order: **security** (authorization, CSRF, input, escaping, file and
code execution), **localization** (no user-facing text — admin-facing included —
outside the language system), then error-free execution, phpBB compliance,
maintainability, and style. A report with style findings but no security or
localization verdicts is unfinished, not clean.

## Hard constraints

- **Do not modify, create, rename, or delete any file** inside the extension tree.
  Scratch notes and the reference cache, both outside the extension tree, are
  fine.
- **The extension is an extracted archive, not a git checkout.** Do not run `git`
  against it, and do not look for history, commits, branches, diffs, tags, or an
  upstream remote. There is no "current change" to review — review the files as
  shipped. (A local `phpbb/phpbb` clone used for reference is a separate
  repository; git is fine there.)
- Report **only** in your reply (or a file the user explicitly asks for).
- Read the **entire** fileset before concluding. See *Completion rule*.
- Never ask the user to paste files; read them yourself.
- Every finding must cite a real `path/to/file.php:line` you actually read. If you
  cannot point at a line, it is not a finding.
- **The policy is the standard, not your judgement.** Every `[valdeny]` must rest
  on a provision of the validation policy (R2) that you actually read; every
  style finding on a rule the coding guidelines (R1) actually state. The
  checklist is a working aid, not authority — where it and the policy disagree,
  the policy wins. Do not invent requirements the team has not adopted, and do
  not escalate an advisory observation into a denial. See the authority section
  at the top of `references/checklist.md`.

## Role

Act as a senior phpBB extension reviewer doing a security review: web application
security first, then PHP 7.x/8.x, Symfony DI and YAML, Twig and the phpBB template
system, ES6 JavaScript, HTML/CSS, SQL and DBAL.

## Process

### 1. Inventory first

Before reading any single file, build a complete file list (every extension file,
any extension, including dotfiles). State the file count. Build the list by walking
the directory tree, not from version-control metadata. If a `.git/` directory is
present, do not traverse its contents — record it as a packaging finding (see
checklist item 6) and move on.

This list becomes the **per-file ledger**: every file in it must end the review
with a recorded result. Nothing is excluded — `README` and other documentation
are checked against the code by section P8, and binary assets by P5–P7.

Identify:

- `composer.json`, `ext.php`, `config/*.yml`, `migrations/`, `acp/`, `controller/`,
  `event/`, `styles/`, `language/`, `license.txt`, `README`.
- Third-party/vendor/minified assets. Note them as **not reviewed line-by-line**
  rather than silently skipping or flooding the report with findings about them —
  they still get a ledger row saying exactly that.

### 2. Fetch the authoritative references — mandatory gate

Obtain every **Required** reference in `references/resources.md` (R1–R4, plus R5
if the extension ships templates) **before** you read any extension code. Check
the 24-hour cache first and reuse any copy under a day old; otherwise fetch and
write it to the cache. Record the reference ledger row for each one as you go:
id, status, and the proof column — a verbatim phrase from the text or a concrete
count.

This is a gate. **Do not start step 4 with an incomplete ledger, and do not write
the report until the ledger is complete** (it is published in the coverage notes
after the report, not inside it). Never skip a fetch on
the grounds that you already know what the document says — **do not invent
guideline quotes or paraphrase a document you did not read**. A `[url=]`
quotation is permitted only when that row says `fetched` and the words appear in
the text you fetched.

If a fetch fails, mark the row `failed: <reason>` and downgrade any finding that
depended on quoting it.

### 3. Resolve the extension against phpBB source

Follow `references/core-verification.md`. You need a local `phpbb/phpbb` checkout
on `3.3.x` — expected input, not an optional extra, because the GitHub tree
cannot be grepped and absence cannot be proven without it.

Resolve its path from the remembered config file first, then your own persistent
memory, then by probing the obvious locations, and **only then ask the user**.
Validate whatever you find (real checkout, actually phpBB, on `3.3.x`) and record
a validated path back to the config so the next run does not ask again.

Build the full inventory of core symbols the extension depends on (events,
template events, service ids, classes, functions, constants, permissions,
migration dependencies), resolve every entry, and check each one against the
minimum phpBB version that `composer.json`'s `extra.soft-require` permits — a
symbol newer than that floor is a `[valdeny]`.

Then build the extension's **own** definition inventory (§2b of that file):
variables, properties and methods used versus defined; every cache written versus
every place its data changes; the defined language keys diffed against core's. A
variable that is never assigned on the path that reads it, and a cache that one
action purges and another forgets, are invisible without these lists — file-by-file
reading does not surface them.

With no clone: never claim a symbol does not exist. Downgrade every such finding
to `[valinfo]` prefixed `unverified — confirm against 3.3.x`, and add the single
line to the report saying verification was incomplete.

### 4. Sweep the action surfaces

Checklist section S, before anything else. Enumerate every entry point and
state-changing action the extension adds — ACP/UCP/MCP module modes, controller
routes, AJAX endpoints, cron tasks, forms — and build the surface table with all
six columns: privileged, auth check, CSRF, input typing, output escaping, text
localized. Resolve every cell; a blank is unchecked, not fine.

This exists because a pass that starts with packaging reliably never arrives at
ACP authorization, CSRF, and admin-text localization. Do it first.

**The surface table is not the boundary of the security review.** It exists so
privileged actions are not missed. Section D is then applied to *every file in
the inventory* via the routing table in section T — front-end controllers,
listeners, cron tasks, notification types, migrations, language files, templates,
JavaScript, CSS, shipped assets. An extension with no ACP module at all still
gets a full security pass.

### 5. Run the checklist

Work through `references/checklist.md` **in full, in its stated run order** — S,
then T, then D, L and E, then N, P, A, B, C, F, G. Packaging and compatibility are the
easiest sections and the least important; leaving them last stops them from
crowding out the security and localization work.

**Section L is logic and bugs** — intent versus implementation, security controls
that are present but wrong (inverted guard, wrong permission, missing ownership
check, ignored `check_form_key()` result), and general correctness. Its governing
rule: state the concrete failing case — which input, which state, what goes wrong
— or do not report it. Unless the defect is a security-control failure or a
guaranteed fatal, it is `[valinfo]` labelled as needing confirmation by hand.

**Section N is extension-point contracts** — notification types, cron tasks,
permission classes, anything registered with a core subsystem. Section C confirms
a symbol exists; N confirms the extension implements it correctly. A notification
type that extends the right base but mixes two id spaces in `get_item_id()`, or
whose email template references a variable the class never sets, passes every
check in C and is still broken.

**Section T is the routing table.** It maps every file type in the inventory to
the sections that apply, so no file is passed over for being unexpected, and it
is what turns "all files were checked" into something you can show. Build the
per-file ledger from it as you go: one row per inventoried file, the sections
applied, the result. It now routes `adm/style/` explicitly — ACP assets do not
live under `styles/`, which is exactly why they get skipped.

**Section P10** covers anything loaded from a third-party origin at runtime: a
JavaScript `import` from a CDN, `fetch()` across origins, `<script src>`,
`@import`, off-origin `url()`. Dependencies must be bundled, and this is a policy
matter, not a style preference.

Record a verdict for every item id as you go (`ok` / `info` / `deny` / `na` /
`unverified`). That tally is published in the coverage notes after the report, so
it is an artifact rather than a private note — but it stays out of the report
itself.

### 6. Filter false positives

Before writing any finding, test it against `references/false-positives.md`. Most
bad validation reports are made of items on that list. A value that is
admin-configured, hard-coded by the developer, already escaped downstream, or
never reaches output is not a vulnerability — say so or say nothing.

### 7. Self-audit before writing — exit gate

Every other gate in this skill protects *starting* the work. This one protects
finishing it. Before you write a single line of report:

1. **Walk the checklist again** and confirm you have a verdict for every item id.
   For any item you cannot immediately say what evidence you looked at, you have
   not done it — do it now. An item you cannot recall examining is not `ok`.
2. **Reconcile the per-file ledger against the inventory.** The counts must
   match — every file from step 1 has a row and a result. A file with no row was
   not examined; go and examine it. Do not reconcile by shrinking the inventory.
3. **Check the surface table is complete.** If the fileset contains `acp/` and
   the table is empty or missing rows, the sweep did not happen.
4. **Look at the shape of your findings.** If they are all packaging, metadata or
   style, treat that as a symptom rather than a result: re-check S, D and E
   specifically. A real 3.3 review of an extension with an ACP module almost
   always has something to say about authorization, CSRF, or localization.
5. **Attribute every denial.** For each `[valdeny]`, name the R2 provision it
   rests on — from the text you fetched, not from memory. Any denial you cannot
   attribute is downgraded to `[valinfo]` or dropped, now, before the report is
   written. Same test for style findings against R1: no stated rule, no finding.
6. **Confirm the reference ledger and symbol inventory are complete** (steps 2
   and 3).
7. **Check you did not stop early.** If the review produced a denial partway
   through, confirm every later step and section was still completed in full. A
   settled verdict is not a reason to have stopped.

### 8. Write the report

Follow `references/report-format.md` exactly. The posted report is **findings,
then a recommendation** — nothing else. No scope header, no reference ledger, no
surface table, no coverage matrix, no statistics. Grouped by file in fileset
order, `[valdeny]` for anything that blocks approval and `[valinfo]` for
everything else, and only files that have issues.

The ledger, surface table and coverage matrix are still required — they go
**after** the report, outside its fenced block, under "Coverage notes (internal —
not for posting)". Moving them out of the report does not make them optional; the
step-7 exit gate still requires them complete first.

**Read `references/example-report.txt` immediately before you draft anything.**
It is a complete finished report in the exact required syntax, in a plain-text
file containing no Markdown. Imitate it directly. This is not optional and not a
formality — the report coming out as Markdown is the most frequent failure of
this skill, and a fresh look at a correct specimen is what prevents it. Recency
beats rules: make the last formatting you saw be the formatting you want.

Then: deliver the entire report inside **one fenced code block**, with nothing but
a single short sentence outside it. No conversational preamble, no prose summary
afterwards — chat voice drags the syntax back to Markdown. Before sending, search
the draft for a backtick, an asterisk, an emphasis underscore, a hash heading, a
table pipe, or a bracket-paren link. One hit means the report is wrong; rewrite
that part.

Close with the colour-coded recommendation, exactly one of:

    [b]Recommendation:[/b] [color=#008000][b]Approve[/b][/color]
    [b]Recommendation:[/b] [color=#FF0000][b]Deny[/b][/color]

## Severity: deny vs. info

Recommend **Deny** if any of these is present. Evaluate every entry even once one
has matched — this list decides the verdict, it does not bound the review:

- An exploitable security issue: XSS, SQL injection, CSRF on a state-changing
  action, path traversal, arbitrary file read/write/include, unserialize of
  untrusted data, command execution, missing permission/auth check on an
  admin-only or moderator-only action.
- Obfuscated, encoded, or remotely-fetched executable code.
- Hard-coded user-facing text in PHP, HTML/Twig, or JS instead of language keys.
- Code that errors out or fatals on a supported PHP version, or template syntax
  that will not compile.
- A missing `license.txt`, or one that is materially different from, or clearly
  not, GPL-2.0-only. Minor or non-substantive differences from the skeleton
  template are not findings.
- Mixed Twig and legacy phpBB template syntax in the same construct.
- Use of a `core.*` event, service, class, or method that does not exist in 3.3.x
  (verified against source — see step 3).
- Use of a core symbol introduced after the lowest phpBB version that
  `extra.soft-require` permits.

Everything else — spacing, naming, unused code, redundant queries that are not in a
hot path, missing docblocks, cosmetic template issues — is `[valinfo]`.

Do not use a percentage threshold to decide the verdict; judge by the list above.

**And check the list against the policy, not the other way round.** This list is
a summary of R2, written by hand. If R2 as fetched does not support one of these
as grounds for denial, the policy governs and the entry is downgraded — note the
discrepancy in the coverage notes so the team can correct it. Likewise, nothing
absent from this list becomes a denial because it seemed serious.

## A finding never ends the review

**The review is exhaustive, not short-circuit.** A `[valdeny]` — or ten — does
not decide anything about how much work is left. Every step, every section, and
every checklist item is completed regardless of what earlier ones found.

- Never stop because the outcome is already settled. The verdict is a *summary of
  complete coverage*, not the objective. Reaching "Deny" early does not mean you
  are finished; it means the rest of the review still has to be written up.
- The deny criteria are a checklist, not a short-circuit boolean. Evaluate all of
  them even after the first one matches.
- Section S: resolve **every** surface, not just up to the first one missing a
  control. Three unprotected ACP actions are three findings, and the author needs
  all three.
- A denial in an early section does not excuse a later one. A bad `license.txt`
  says nothing about CSRF; a missing permission check says nothing about
  localization.
- The author fixes what the report lists. Anything you stopped short of
  discovering comes back as a second rejection round — that is a worse outcome
  for the author and for the team than a longer report.
- No checklist item may be recorded as `na`, blank, or "not assessed because the
  extension is already denied". If an item was genuinely not evaluated, say
  `unverified` and name why.
- These phrasings are forbidden in a report: "already denied, no further review
  performed", "review stopped at the first blocker", "remaining checks omitted as
  the outcome is decided", and anything equivalent.

The same applies in reverse: an early section that is completely clean does not
license skipping later ones.

## Completion rule

Do not write "validation passed", "no issues found", or a verdict until every file
in the step-1 inventory has a row and a result in the per-file ledger, every
symbol in the step-3 inventory has been resolved or explicitly marked unverified,
every surface in the step-4 table has all six cells filled, and every checklist
item id has a recorded verdict in the coverage matrix. "Sections completed" is not a claim you may make without the
matrix that backs it.
A single suspicious call is not a conclusion — finish the sweep. If a finding stays
uncertain after you have read the whole extension, report it as `[valinfo]` and
label it explicitly as needing manual confirmation.

Static review outside a running phpBB gives no runtime evidence. Say that once in
the report; do not use it to hedge every finding.

## Human in the loop

Close the report with the reminder that a team member must read and verify the
findings before anything is sent to the extension author. Never present the
recommendation as a final decision.
