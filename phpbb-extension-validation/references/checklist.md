# Validation checklist

Work through every item. Each item: decide pass / `[valinfo]` / `[valdeny]` / N/A,
and record that verdict in the coverage matrix — an item with no recorded verdict
has not been done. Cite `file:line` for anything that is not a pass.

**Every item is evaluated regardless of what earlier items found.** A denial in
one section does not shorten any other section; the list is exhaustive, not
short-circuit. `na` means the item genuinely does not apply — never "the
extension is already denied".

## Authority — this checklist is not the standard

**The standard is the phpBB validation policy (R2) and the coding guidelines
(R1). This checklist is a working aid that organises them; it is not itself
authoritative.** It was written by hand, it may be wrong, and it may contain
items the team never adopted.

Consequences, and they are binding:

1. **Every `[valdeny]` must be attributable to R2**, the validation policy — a
   provision you actually read in the fetched document. If you cannot point to
   the provision, it is not a denial. Downgrade it to `[valinfo]` or drop it.
2. **Every style or convention finding must be attributable to R1.** If the
   coding guidelines do not state the rule, do not report it. Your sense of good
   PHP is not the phpBB standard, and neither is another project's.
3. **Security findings** are covered by the policy's provisions on security and
   malicious code. A specific technique (stored XSS via SVG, CSRF on a GET
   action) does not need to be enumerated in the policy to be a denial — it is an
   instance of a provision that is. Say which provision.
4. **Where this checklist and the policy disagree, the policy wins** and the
   checklist item is a bug. Record it in the coverage notes so the team can fix
   the checklist; do not act on the checklist against the policy.
5. **Do not invent requirements.** Unit tests, changelogs, semantic versioning,
   docblock coverage, a particular project layout, `declare(strict_types=1)`,
   PSR-12, static-analysis clean runs — none of these are phpBB extension
   requirements. Absence of any of them is not a finding at any severity.
6. **Do not escalate on instinct.** An item marked advisory below cannot become a
   denial because it "feels risky". If you believe the policy should cover
   something it does not, say so in the coverage notes as a suggestion to the
   team, and keep it out of the report.

Each section below carries an authority line saying what backs it. Sections
marked **advisory** can only ever produce `[valinfo]`, never a denial, no matter
what the finding is.

Attribution belongs in the coverage notes, not in the posted report: for every
`[valdeny]`, one line naming the provision it rests on. A denial with no
attributable provision is the single most damaging thing this review can produce,
because the author is entitled to ask which rule they broke.

## Run order

**Do section S first, then T, then D, L and E, then the rest (N, P, A, B, C, F, G).**
Packaging and compatibility checks are the easiest to complete and the least
important; doing them first reliably produces a report that stops before it
reaches the security and localization work. Start where the risk is.

Section T is the routing table: it assigns every file in the inventory to the
sections that apply to it, and it is what makes "all files were checked" a fact
rather than an assumption. Build the per-file ledger from it as you go.

A finished pass whose findings are all packaging or style is a signal that S, D
and E were skimmed — re-check them before writing the verdict.

## S. Action surface inventory (do this first)

*Authority: R2 — security and malicious-code provisions; R1 for the localization
of admin text. Denials here rest on those.*

Before judging individual files, enumerate every **entry point and
state-changing action** the extension adds, and build a table. This mirrors the
core-symbol inventory: enumerate first, then resolve each row, so nothing is
silently missed.

S1. Find every surface:
    - ACP/UCP/MCP module modes — each `mode` in `acp/*_info.php` and its
      corresponding `main()`/`mode` handler
    - controller routes in `config/routing.yml` and their controller methods
    - AJAX/JSON endpoints and anything reading `$request->is_ajax()`
    - cron tasks and any listener that writes data
    - forms in templates (`<form`) and links that trigger an action

S2. For each surface, record a row with all six columns:

| Surface | Privileged? | Auth check | CSRF | Input typing | Output escaping | Text localized |
| --- | --- | --- | --- | --- | --- | --- |

S3. Resolve every row. A blank cell is not "fine", it is unchecked:
    - **Auth** — `$auth->acl_get()` / `acl_gets()` before the work happens, or the
      ACP module's `auth` string covering it. Rendering-time-only checks do not
      count (checklist 35).
    - **CSRF** — `add_form_key()` + `check_form_key()` for POST;
      `generate_link_hash()`/`check_link_hash()` or `confirm_box()` for
      state-changing GET (checklist 34).
    - **Input typing** — every value read with `$request->variable()` and the right
      type/default (checklist 28–29).
    - **Output escaping** — anything user- or DB-derived reaching the response is
      escaped for its context (checklist 32–33).
    - **Text localized** — every string the admin or user sees comes from a
      language key: module titles, mode titles, config labels and explanations,
      submit buttons, success and error messages, `trigger_error()` arguments, log
      entries, and confirm-box text (checklist 47–48, E1).

S4. Any surface with an unresolved privileged action, missing CSRF protection, or
    hard-coded user-facing text is a `[valdeny]` — one finding per surface, naming
    the missing control. Keep going after the first bad surface: resolve every
    row. Three unprotected actions are three findings, and the author needs all
    three in one report.

S5. Reproduce the completed surface table in the coverage notes that follow the
    report. An empty table when the extension ships an ACP module means the sweep
    was not done.

## L. Logic, correctness and bugs

*Authority: R2 where a defect breaks a board, corrupts data, or defeats a
security control — those are denials. Everything else here is **advisory**
`[valinfo]`, because static review cannot confirm behaviour. Say which.*

**The reporting rule for this whole section, applied before you write anything:
state the concrete failing case.** Which input, which state, which sequence —
and what goes wrong as a result. "This looks fragile" is not a finding. If you
cannot construct a specific case where the code misbehaves, you have a suspicion,
not a defect, and it does not go in the report. This is what keeps a logic pass
from drowning the report in noise.

Unless the defect is a security control failure or a guaranteed fatal, mark it
`[valinfo]` and label it explicitly as needing confirmation by hand.

### L-a. Intent versus implementation

L1. Build a short intent list from what the extension claims about itself: the
    `composer.json` description, the README, the ACP labels and language keys, and
    the setting names. Then check the code actually does those things. A setting
    that is stored but never read, a documented feature with no implementation, or
    a toggle whose "off" path does nothing are real findings — and they are
    findings a reviewer can confirm quickly, which makes them worth reporting.
L2. Every config setting the extension adds is both written and read. A setting
    the code never consults is `[valinfo]`.
L3. Language keys describing behaviour match what happens — an "items will be
    deleted permanently" warning above a soft delete, or vice versa.

### L-b. Security logic — the control is present but wrong

These pass every check in section D and S, because the call exists. They are the
highest-value items in this section, and they are denials.

L4. **Inverted or misplaced guard.** `!$auth->acl_get(...)` protecting the wrong
    branch, an `acl_get()` whose result is computed and discarded, a check whose
    failure path falls through instead of returning, or a guard placed after the
    write it was meant to protect.
L5. **Wrong permission consulted.** The check names a real permission, but not the
    one governing this action — a read permission gating a write, `a_` where the
    action is board-wide, or a permission the migration never created.
L6. **Missing ownership or scope check.** A record id arrives from the request and
    is acted on after only a generic permission check, with nothing confirming the
    record belongs to this user, this forum, or this board. Editing or deleting
    another user's row this way is an access-control defect even though a
    permission check is present.
L7. **CSRF token checked but result ignored** — `check_form_key()` called without
    branching on it, or inside a condition that cannot fail.
L8. **Escaping applied to the wrong value**, or applied and then undone: the safe
    variable escaped while the unsafe one is emitted, or `html_entity_decode` after
    escaping.
L9. **Authorization decided on client-supplied state** — a hidden form field, a
    cookie, or a request parameter used to decide whether the user may proceed.

### L-c. General correctness

L10. Conditional logic: `&&`/`||` confusion, negation errors, `==` where identity
     matters (id comparisons, `strpos()` results, `in_array()` without strict),
     assignment inside a condition, chained conditions that can never all hold.
L11. Loop bounds and arithmetic: off-by-one, pagination `start`/`limit` maths that
     can go negative or skip a row, `count()` re-evaluated against a mutated
     array, an `unset()` inside the loop iterating it.
L12. SQL semantics: `AND`/`OR` mixed without parentheses, a `JOIN` that multiplies
     rows, `WHERE` on a nullable column via `=` rather than `IS NULL`, `LIMIT`
     without `ORDER BY` where a specific row is expected, an `UPDATE` or `DELETE`
     whose `WHERE` can match more rows than intended — that last one is a denial.
L13. Return values and error paths: a `false`/`null` return used as data, a failed
     query treated as an empty result, `sql_fetchrow()` in a condition that also
     assigns, exceptions thrown on a path with no handler where phpBB will not
     catch them.
L14. Uninitialised or conditionally-initialised variables read on a path where
     the assignment did not run.
L15. Unreachable or duplicated logic: a branch that cannot be entered, two
     branches with identical bodies, a `switch` case that falls through
     unintentionally, code after an unconditional `return`/`trigger_error()`.
L16. Type confusion: a value that is sometimes an array and sometimes a string,
     numeric strings compared to integers, a method returning different types on
     different paths where the caller assumes one.
L17. State consistency: data written across several statements with no
     consideration of partial failure, a cache not purged after the data it
     caches changes (`$cache->destroy()`), a counter updated in one place but not
     its inverse, config left describing a state the tables no longer match.
L18. Concurrency, only where it is plainly reachable: a read-modify-write on a
     shared counter or a "check then insert" with no unique constraint. Keep this
     to cases you can name; do not speculate about races generally.

## N. phpBB extension-point contracts

*Authority: the phpBB 3.3 source — these classes have contracts, and breaking one
produces a broken board rather than a style complaint. Contract violations that
break behaviour are denials under R2; the rest is advisory.*

Section C confirms that a symbol *exists*. This section confirms the extension
*implements it correctly*. Anything the extension registers with a core subsystem
has a contract, and a class that extends the right base while filling it in wrongly
passes every check in C.

For each extension point present, read the core base class in the clone
(`<phpbb_clone>/phpBB/phpbb/...`) and check the implementation against it.

### N-a. Notification types (`notification/type/*.php`)

The most contract-heavy extension point, and the easiest to get subtly wrong.

N1. `get_type()` returns a unique, vendor-prefixed string matching the service id.
N2. **`get_item_id()` and `get_item_parent_id()` are consistent about what a
    notification item *is*.** Pick one identity and hold it: if a notification is
    "one per post", `get_item_id()` must return the post id on every path, and a
    reaction id must never appear in the same field. Mixing two id spaces in one
    notification type is a real defect — it breaks deduplication, it makes
    `mark_read` address the wrong row, and purge and sync then cannot find the
    records they are meant to delete. Trace both methods and the data passed to
    `add_notifications()` and confirm they agree.
N3. If the intent is "notify once per post" rather than once per event, there must
    be something that actually enforces it — an existing-notification lookup, or
    `item_id` chosen so the unique index collapses duplicates. A comment saying
    "only notify once" with nothing implementing it is a finding.
N4. `find_users_for_notification()` respects permissions and excludes the acting
    user; it does not return the whole board.
N5. `get_email_template()` and `get_email_template_variables()` — **every
    variable the email template references is actually set**, and every variable
    set is defined at that point in the method. An undefined variable used to
    build a URL yields a broken link in a real email, which is the worst place to
    find out. This is where L14 (variables read on a path where their assignment
    did not run) matters most; check it explicitly here.
N6. The email template files referenced exist, under `language/<lang>/email/`, and
    the greeting and body use the variables the class supplies, not invented ones.
N7. `get_title()`, `get_reference()` and `get_url()` build from data the
    notification row actually carries, and are escaped for output.
N8. **Cleanup exists and matches.** When the underlying item is deleted, the
    notifications go too: a `delete_notifications()` call on the right type with
    the right ids. Where the extension purges or synchronises its own data, the
    notification rows are included. Orphaned notification rows pointing at deleted
    items are a defect, not an untidiness.
N9. The type is registered in the notification manager (service tag
    `notification.type`) and the migration adds it with `notification.add`,
    removing it on revert.

### N-b. Cron tasks (`cron/task/*.php`)

N10. Extends `\phpbb\cron\task\base`, implements `run()`, `is_runnable()` and
     `should_run()`; `should_run()` consults a config timestamp the task then
     updates, or it will run on every request.
N11. Registered with the `cron.task` service tag; long work is chunked rather than
     unbounded.

### N-c. Permission classes and other subsystems

N12. Permission roles/options added by a migration are also declared in the
     permission language file, and the `auth` strings used elsewhere match exactly.
N13. Anything registered against a core subsystem — search backend, avatar
     driver, captcha plugin, auth provider, notification method, console command —
     implements the full interface of its base class. Read the base class; a
     missing or wrongly-signed method is a denial because core will fatal on it.

### N-d. Caches

N14. **Enumerate every cache the extension writes** — `$cache->put()`,
     `$cache->sql_save()`, `cache->destroy()` targets, and any custom cache
     service. Then check every place the underlying data changes and confirm the
     matching cache is purged there.
N15. A data-changing action that purges one of its caches but not another is a
     finding: stale values survive until an unrelated refresh. This is the common
     shape — for example an admin deletes an item, the item-list cache is
     destroyed, and a dependent counter cache is not. Name both caches and the
     action.

## T. File-type routing — every file gets an owner

*Authority: none — this is bookkeeping, not a standard. It produces no findings
of its own.*

Every file in the step-1 inventory must be examined, and this table says which
sections apply to it. Work from the inventory, not from memory: take each file,
find its row, apply those sections, record the result in the per-file ledger.

**Every PHP file gets the full security section D and the logic section L**, not
just the ones behind an ACP module. The rows below add what else applies.

Note that ACP assets live in **`adm/style/`**, not `styles/`. They are easy to
miss for exactly that reason, and they are the files that render the admin UI, so
they get the same treatment as front-end templates and scripts.

| File type / location | Sections that apply |
| --- | --- |
| `*.php` under `acp/`, `controller/`, `event/` | **D, L**, S, C, E, G |
| `*.php` under `notification/`, `cron/`, or registered with a core subsystem | **D, L, N**, C, E, G |
| `*.php` under `migrations/` | **D, L**, B, G |
| `*.php` under `language/` | **D** (HTML in keys), E, G65 |
| `acp/*_info.php` | **D, L**, S, C23, E47a |
| `ext.php` | **D, L**, B9–10, G |
| any other `*.php` anywhere in the package | **D, L**, G — and work out what calls it |
| `config/*.yml` | C18–22, G, and D for anything resembling a credential |
| `composer.json` | A1–4, P |
| `*.html`, `*.twig` under `styles/` | **D32–33, L**, S, E, F |
| `*.html` under `adm/style/` | **D32–33, L**, S, E, F — ACP templates, same checks |
| `*.js`, `*.css` under `adm/style/` | as the `*.js`/`*.css` rows below, plus P10 |
| anything else under `adm/` | **D, L**, and work out what loads it |
| `*.js` | **D32–33, L**, E, F60–61, G, **P10** |
| `*.css` | F62, G64, **P10** |
| `*.png`, `*.jpg`, `*.gif`, fonts, other binaries | P5–P7 |
| `*.svg` | **P6 — open every one**, plus P5 |
| `license.txt` | A5 |
| `README*`, `CHANGELOG*`, other `*.md` | P8, L1 (claims versus code) |
| `*.json` other than `composer.json` | P9, D44 (credentials, local paths) |
| Anything else, including unrecognised extensions | A6–A8, P, D — and look at it |

The last row is the point of the table. A file type you did not expect is a
reason to open the file, not a reason to pass over it. If something genuinely
needs no check, record it in the ledger as `n/a` with a reason — never leave it
unaccounted for.

## P. Policy and shipped assets

*Authority: R2 directly. Every item here must be checkable against a provision
you read in the fetched policy; if the policy does not support one, drop it and
note the discrepancy.*

These come from the validation policy (reference R2) and cover the files the
code-focused sections do not.

P1. No advertising, promotional content, affiliate links, donation appeals, or
    backlinks to the author's own site in code, templates, language strings, or
    the ACP UI, beyond a normal author credit in `composer.json`.
P2. Nothing in the extension collects, transmits, or reports usage, board, or
    user data. Combined with checklist 40, any outbound call must be disclosed,
    optional and necessary.
P3. The author is the copyright holder or has permission for all shipped code.
    Wholesale copies of core phpBB files, or of another extension, are a
    `[valdeny]` unless attributed and license-compatible.
P4. Any bundled third-party library is named in `composer.json`, license-
    compatible with GPL-2.0, and shipped in a form that can be reviewed — a
    minified bundle with no readable source is a `[valdeny]`.
P5. Shipped images, icons, fonts and other binaries are the author's, public
    domain, or licensed compatibly. Flag recognisable third-party logos and
    trademarks, and anything that looks lifted from a commercial icon set.
P6. **SVG files are code.** Open every one and confirm there is no `<script>`,
    no `on*` event attribute, no `<foreignObject>`, and no external
    `xlink:href`/`href` reference. An SVG served to a board user with script in
    it is stored XSS → `[valdeny]`.
P7. No unexpected binaries at all: archives, executables, `.phar`, compiled
    objects, database dumps. Name the file and its type.
P8. `README`, `CHANGELOG` and other documentation are consistent with the code —
    the version matches `composer.json`, the stated phpBB requirement matches
    `extra.soft-require`, described features exist, and the install instructions
    match the actual directory name. Contradictions are `[valinfo]`; a false
    claim about supported phpBB versions is `[valdeny]`. Documentation is
    reviewed for these claims, not for prose style.
P9. Other JSON, XML or config files shipped in the package are accounted for:
    what reads them, and do they contain credentials, absolute local paths, or
    developer machine details.
P10. **Nothing is loaded from a third-party origin at runtime.** An extension must
    ship its dependencies, not fetch them from someone else's server: a board
    silently depends on that host's availability, its content can change under
    the board without review, and every page view leaks the visitor's IP and
    referrer to it. Check for all of these, not only the PHP ones:
    - JavaScript: `import ... from 'https://...'`, a dynamic `import()` of a URL,
      `fetch()`/`XMLHttpRequest` to another origin, `new Worker(url)`, or a
      script element injected with an off-origin `src`
    - templates: `<script src="https://...">`, `<link href="https://...">`,
      `<iframe src>`, `<img src>` pointing off-site
    - CSS: `@import url(https://...)`, `url()` for fonts or images on another
      origin, including Google Fonts
    - PHP: the outbound calls already covered by checklist 40

    A CDN import such as `https://cdn.jsdelivr.net/npm/...` is the common case
    and is a `[valdeny]`: the library must be bundled in the package. Note that
    this is a policy matter (R2), not a style preference — attribute it that way.
    A documented, optional, user-configured external service is different; judge
    it under P2 and checklist 40.

## A. Packaging and metadata

*Authority: R2 for the license and package requirements; R1 for file layout and
naming. Items not traceable to either are advisory.*

1. `composer.json` exists, `type` is `phpbb-extension`, `name` is
   `vendor/package` all lowercase, and it matches the directory layout
   `ext/<vendor>/<package>/`.
2. `extra.display-name`, `description`, `homepage`, `version`, `license`,
   `authors` present and sane. `license` is `GPL-2.0-only` (or `GPL-2.0`).
3. `extra.soft-require` names `phpbb/phpbb` with a version constraint that matches
   what the code actually uses.
4. `require`/`require-dev` pulls in no unexpected third-party packages; any bundled
   `vendor/` is declared and explained.
5. `license.txt` is a legitimate **GPL-2.0-only** license. Use the Extension
   Skeleton template (reference R4) as the reference, ignoring whitespace,
   line-ending differences, and harmless standard GPL-2.0 text outside the
   template. Do not report or deny minor or non-substantive differences — report
   a license issue only when the file is materially different from, or clearly
   not, GPL-2.0-only. A missing `license.txt`, or a file under a different
   license, → `[valdeny]`; name what is materially wrong rather than saying the
   file "does not match".
6. No stray files: version-control directories and metadata (`.git/`,
   `.gitignore`, `.gitattributes`, `.github/`, `.svn/`), IDE folders,
   `.DS_Store`, `Thumbs.db`, `node_modules/`, build caches, backup copies
   (`*.bak`, `*.orig`, `file copy.php`), archives. These are packaging findings
   (`[valinfo]`) — do not read them as a repository to inspect.
7. No `.htaccess`/`index.htm` shims needed inside `ext/`; flag anything that tries
   to alter server config.
8. No PHP file is executable-on-upload dangerous (e.g. a bare `install.php` doing
   work outside the migration system).

## B. Extension lifecycle

*Authority: R1 and the phpBB migration API. Correctness problems that would break
install, enable or revert are denials; the rest is advisory.*

9. `ext.php`, if present, extends `\phpbb\extension\base` and only overrides
   `is_enableable()`, `enable_step()`, `disable_step()`, `purge_step()`.
10. `is_enableable()` returns a bool (or a message array in 3.3) and does not
    perform side effects.
11. Migrations live in `migrations/`, extend `\phpbb\db\migration\migration`, and
    each declares `static::depends_on()` pointing at a real class that exists
    (phpBB core migration or one in this extension).
12. `effectively_installed()` logic, where present, is correct and does not always
    return true/false.
13. `update_data()` / `revert_data()` are symmetric: anything added by
    `config.add`, `module.add`, `permission.add`, `table_column_add` is removed on
    revert (either explicitly or via automatic reversal).
14. Extension **version** is not stored with `config.add`/`config.update`. If it
    is, check whether a later migration removes it with `config.remove`; if not,
    `[valinfo]`: should be removed in a future release.
15. Table names use the `$table_prefix` / `%core.table_prefix%` placeholder, never
    a hard-coded `phpbb_` prefix.
16. Schema changes use `update_schema()`/`revert_schema()`, not raw SQL DDL.
17. No destructive operation on core tables (dropping columns, deleting rows) that
    is not clearly scoped to this extension's own data.

## C. Services, events, and phpBB API

*Authority: the phpBB 3.3 source itself — a symbol either exists or it does not.
Usage that fatals is a denial; preference between working approaches is
advisory.*

18. `config/services.yml` service ids are namespaced `vendor.package.*`; arguments
    match the constructor signature of the class (arity and order).
19. Every listener returns its subscribed events from
    `getSubscribedEvents()` and every handler method exists.
20. **Every `core.*` event name is verified to exist in phpBB 3.3.x** by grepping
    the source — see `core-verification.md`. A nonexistent event → `[valdeny]`;
    an unverifiable one → `[valinfo] unverified`.
21. Event handlers read and write only variables the event actually exposes
    (`$event['var']` keys present in the `dispatcher->trigger_event` call).
21a. Every core symbol used — event, template event, service id, class, method,
    function, constant, permission — was resolved against 3.3.x source, and none
    is newer than the lowest phpBB version `extra.soft-require` permits. A symbol
    above that floor → `[valdeny]`, naming both versions.
22. Routing (`config/routing.yml`) paths and controller service references resolve.
23. ACP/UCP/MCP modules: `acp/*_info.php` returns a valid `module()` array; the
    referenced module class and mode method exist; `auth` string names a real
    permission (`acl_a_*`, `ext_vendor/package`, etc.).
24. Permissions added by a migration are also defined in the permission language
    file and checked before the protected action runs.
25. Cron tasks extend `\phpbb\cron\task\base` and implement `is_runnable()` and
    `should_run()`.
26. Uses injected services, not `global $db, $user, ...`, inside classes. Globals
    in a legacy-style file → `[valinfo]`.
27. Deprecated 3.3 APIs are avoided: `$user->lang()` for new code (prefer
    `$language->lang()`), `request_var()`, `$auth->acl_get` misuse,
    `set_config()`, `add_log()` in favour of the `log` service.

## D. Security (any hit here is normally `[valdeny]`)

*Authority: R2 — security and malicious-code provisions. Specific techniques are
instances of those provisions; name the provision in the attribution line.*

**This section applies to every file in the package, not to the ACP.** Section S
enumerates entry points so that privileged actions are not missed; it is not the
boundary of the security review. Section D is applied file-by-file, to everything
in the step-1 inventory, via the routing table in section T: front-end
controllers, event listeners, cron tasks, notification types, migrations,
language files, templates, JavaScript, CSS and shipped assets all get it. An
extension with no ACP module at all still gets a full security pass.

Where a security control is present but wrong rather than missing, that is
section L-b — check both.

28. All input comes from `$request->variable()` / `$request->is_set_post()`, never
    `$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`, `$_SERVER` directly. Note the
    third `$multibyte` argument where multibyte text is expected.
29. Type expectations are enforced: `(int)`, `''`, arrays with a typed template.
    An int-typed request var used in SQL is safe; a string one is not.
30. **SQL injection**: every string interpolated into SQL passes through
    `$db->sql_escape()`, `$db->sql_in_set()`, `$db->sql_build_array()`, or is
    cast to int. Flag any `"... WHERE x = '$var'"` that is not.
31. SQL string literals use single quotes; `sql_escape`d values are wrapped in
    single quotes. Double-quoted SQL text comparisons → `[valinfo]` (or
    `[valdeny]` if that hides an injection).
32. **XSS**: anything user- or database-derived reaching a template is escaped —
    Twig autoescaping intact, no `|raw`, no `{% autoescape false %}` over
    untrusted data, no `html_entity_decode` on the way out. Legacy blocks assigned
    with `$template->assign_var()` containing HTML must be justified.
33. Language keys used **inside a JS string or an HTML attribute** are escaped with
    `|e('js')`, `|e('html_attr')`, `|escape`, or `|striptags` as appropriate.
34. **CSRF**: every state-changing POST form calls `add_form_key()` and
    `check_form_key()`; every state-changing GET link carries a link hash
    (`generate_link_hash()` / `check_link_hash()`) or a confirm box
    (`confirm_box()`).
35. **Authorization**: each admin/mod action checks `$auth->acl_get()` (or the ACP
    module `auth` covers it) before doing the work — not only before rendering the
    link.
36. No path traversal: user input never reaches `include`, `require`, `file_get_contents`,
    `fopen`, `unlink`, `move_uploaded_file`, `realpath` without a whitelist or
    `basename()` plus an allowed-directory check.
37. No `eval()`, `assert()` on strings, `create_function()`, `exec`, `shell_exec`,
    `system`, `passthru`, `proc_open`, `popen`, backticks.
38. No `unserialize()` of request or database-stored untrusted data (prefer
    `json_decode`).
39. No obfuscation: `base64_decode`/`gzinflate`/`str_rot13`/hex-escaped blobs that
    produce code, long single-line encoded strings, or code fetched over the
    network and executed.
40. Outbound HTTP calls (`curl_*`, `file_get_contents('http...')`) are disclosed,
    optional, over HTTPS, with TLS verification left on, and do not leak board or
    user data. Undisclosed phone-home → `[valdeny]`.
41. File uploads go through phpBB's `filespec`/`upload` classes or validate
    extension, MIME, and size, and store outside a web-executable path.
42. Uploaded/generated files are not written into the extension's own directory.
43. No `ini_set`/`error_reporting`/`set_time_limit` changes, no `@` error
    suppression hiding failures, no `die()`/`exit()` outside `trigger_error` flows.
44. No credentials, API keys, tokens, or personal data present anywhere in the
    shipped files.
45. Email/notification code does not allow header injection from user input.
46. Cookies set directly (rather than via `$request`) use secure flags.

## E. Language system

*Authority: R1's localization rules, which is what a hard-coded-text denial
quotes. Missing keys that would emit a raw key to a user are correctness, not
style.*

47. No hard-coded user-facing text in PHP, Twig/HTML, or JS. Every such string is a
    language key → `[valdeny]` with the coding-guidelines reference.
47a. **Admin UI text specifically.** Walk the ACP surfaces from section S and
    confirm every one of these comes from a language key, not a literal:
    - module and mode titles in `acp/*_info.php` (`'title' => 'ACP_...'`), and the
      matching keys defined in `language/en/info_acp_*.php`
    - config setting labels and their explanation strings
    - section/legend headings, fieldset titles, table column headers
    - submit, reset, and confirm button captions
    - success messages passed to `trigger_error()` and `confirm_box()`
    - validation and error messages, including those built conditionally
    - log entries added via the `log` service (`LOG_*` keys defined in the
      language files)
    - `<option>` labels and any select/radio choice text
    - tooltips, `title=` and `alt=` attribute text, and placeholder text

    These are the strings most often left hard-coded because they read as
    "internal". They are user-facing — an admin is a user.
48. `trigger_error()` receives a valid language key constant (plus an optional
    error type), not a literal sentence, and the key exists in `language/en/`.
48a. **Every key is namespaced with the extension's own prefix**, and no key
    collides with a core one. Two checks:
    - Key names carry a distinctive prefix tied to the extension (`ACP_MYEXT_*`,
      `MYEXT_*`). Short generic names — `PR_MOVE`, `MOVE_UP`, `SETTINGS`,
      `TITLE`, `DELETE_CONFIRM` — are the problem, and a two-letter prefix is not
      a namespace.
    - Diff the extension's key set against core's. Any key also defined in
      `<phpbb_clone>/phpBB/language/en/**` is a collision: whichever loads last
      wins, so the extension silently changes core wording or has its own text
      replaced, and the symptom appears somewhere unrelated. A collision is a
      `[valdeny]`; a key that is merely generic enough to collide with a future
      core key or another extension is `[valinfo]`.

    The core key set is a plain file read from the clone, so this is checkable —
    do not skip it. List every colliding key by name.
49. Every key defined in `language/en/**` is actually used somewhere in the
    codebase (PHP, Twig, JS). Unused keys → `[valinfo]`, listing key and file.
50. Every key used in code exists in `language/en/**`. Missing → `[valdeny]`.
51. Other shipped locales define the same key set as `language/en`. List per-file
    missing keys → `[valinfo]`.
52. Language files use `$lang = array_merge($lang, array(...));`, are guarded with
    the `IN_PHPBB` check, and set `$lang` only.
53. HTML inside language keys is minimal (inline `<strong>`, `<br />`, `<a>`), well
    formed, and cannot be turned into script. Non-minimal or unbalanced markup →
    `[valinfo]`; anything injectable → `[valdeny]`.
54. Placeholders in keys match the arguments passed (`%1$s` count and order).
55. Plural forms use the `array(0 => ..., 1 => ..., 2 => ...)` style with
    `$language->lang()`'s plural handling where counts vary.

## F. Templates and front-end

*Authority: R1 for template syntax; R2 for anything reaching output unescaped.
Cosmetic CSS and JS preferences are advisory.*

56. No mixing of Twig and legacy phpBB template syntax in the same construct
    (e.g. `{% if %}` with `<!-- ENDIF -->`) → `[valdeny]`.
57. `<!-- INCLUDE -->` / `{% include %}` targets exist; every `EVENT` template
    event exists in `<clone>/phpBB/docs/events.md`, and its `Since:` version is
    not newer than the `soft-require` floor.
58. Every style directory the extension adds (`styles/<style>/template/...`)
    follows the expected layout; `prosilver` fallbacks present if other styles are
    shipped.
59. URLs built with `append_sid()` or the controller helper / `{{ U_* }}`, never
    concatenated by hand with a session id.
60. HTML is valid and balanced; no inline `onclick="..."` handlers running
    unescaped data; no inline `<script>` containing templated untrusted values
    without `|e('js')`.
61. JavaScript is ES5/ES6-compatible with phpBB 3.3's bundled jQuery, does not
    pollute globals, uses `phpbb.*` helpers where available, and has no leftover
    `console.log`/`debugger`.
62. CSS does not override core selectors globally in a way that breaks other
    extensions; no `!important` spam. Cosmetic → `[valinfo]`.
63. No remote CDN assets loaded at runtime — see P10, which is the authoritative
    item and covers JS imports, `fetch`, `<script src>`, `@import` and `url()`.
64a. **No duplicated markup or assets.** Compare templates against each other,
    including `adm/style/` against `styles/`: the same popup, overlay, modal or
    button block repeated in several files, the same inline SVG pasted more than
    once, or a partial that exists twice under different names. Repeated inline
    SVG metadata (`<title>`, `<desc>`, `<metadata>`, editor cruft) bloats every
    page that includes it. Where the same block appears more than twice, say so
    once and list the files; the fix is a shared template include. `[valinfo]`
    unless the duplicates have drifted out of step, in which case the
    inconsistency is the finding.

## G. Code quality (normally `[valinfo]`)

*Authority: R1 where it states the rule; otherwise **advisory** — reviewer craft,
not a standard. Nothing in this section is ever a denial. Items R1 does not
cover (query-in-loop, column selection, unused code, undeclared properties) are
observations offered to the author, and must be phrased as such.*

64. phpBB coding style: tabs for indentation, Allman braces, `array()` or `[]` used
    consistently, spaces around operators, one statement per line, lowercase
    keywords, no trailing whitespace, single trailing newline, UTF-8 without BOM,
    Unix line endings.
65. `IN_PHPBB` guard at the top of every standalone PHP file that is not a
    namespaced class.
66. No unused code: unreachable branches, unused private methods, unused `use`
    imports, unused local variables, commented-out blocks, dead files.
67. **All class properties referenced are explicitly declared** in the class (or a
    parent). Undeclared property access → `[valinfo]` (PHP 8.2 deprecation).
68. Constructor-promoted or declared property types are consistent with what is
    injected by `services.yml`.
69. No SQL queries inside loops — collect ids and use `sql_in_set()` instead.
    Flag the loop and the query.
70. Queries select only needed columns, use `LIMIT` where a single row is wanted,
    and free results with `$db->sql_freeresult()`.
71. Docblocks that exist are accurate: `@param`/`@return` types match the
    signature. Missing docblocks are not a finding; wrong ones are.
72. No PHP notices/warnings by construction: undefined index access on arrays,
    string offsets, implicit null → array, `count()` on non-countables.
73. PHP 8 compatibility: no `$var{0}` string offsets, no removed functions
    (`create_function`, `each`, `money_format`), `#[\ReturnTypeWillChange]` where
    needed, named-argument-safe overrides.
74. Class/file/namespace names match (`\vendor\package\...` matching path), files
    are `snake_case.php` per phpBB convention.
75. Spacing and structure consistency across files — group these into the closing
    "formatting improvements" note rather than one finding per line.
