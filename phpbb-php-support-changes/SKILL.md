---
name: phpbb-php-support-changes
description: "Change supported PHP versions in phpBB extensions while keeping enablement checks, Composer requirements, language messages, documentation, CI runtimes, and support tests consistent. Use for PHP minimum/security-floor changes and the resulting CI failures, including organization-wide updates; not for an unrelated extension audit."
---

# phpBB PHP Support Changes

Treat a supported PHP version change as one compatibility change across the
extension's declarations and verification. Updating `ext.php` alone can leave
valid tests failing and functional CI running a PHP version that the extension
now correctly refuses to enable on.

## Establish the intended requirement

- Use the user's requested minimum and comparison policy. Do not permanently
  reuse a minimum from an earlier task. Verify external release/security claims
  when making them yourself.
- Keep PHP requirements separate from phpBB version constraints. Raising the PHP
  floor does not authorize removing phpBB upper bounds, adding a phpBB 4.0
  exclusion, or claiming new phpBB compatibility. Preserve existing bounds
  unless the user asks to change them.
- Preserve package names, namespaces, public helper interfaces, lifecycle
  methods, and additional enablement safeguards: extension dependencies,
  old-package conflicts, DOM, cURL/SSL, and other actual requirements. Do not
  replace a custom `is_enableable()` body with a generic template without
  accounting for every existing guard.
- If the user explicitly restricts editable files, identify conflicting
  declarations before expanding the scope. Otherwise update directly affected
  support declarations together; avoid unrelated modernization.

For an organization-wide GitHub request, also read
[references/github-batches.md](references/github-batches.md).

## Find every affected declaration before editing

Search actual current source using both the old version string and its numeric
ID, plus support-related terms. For example, after identifying the old floor:

```bash
rg -n 'PHP_VERSION_ID|PHP_VERSION|MIN_PHP|check_php_version|is_enableable|PRIMARY_PHP_VERSION|PHP_VERSION_MATRIX|php-version|declared.support|minimum.*PHP|PHP.*minimum' . .github
```

Also search literal constraints such as `>=8.2`, human-readable requirements,
and the old numeric ID, such as `80200`. These are search examples, not defaults.
Inspect:

- `ext.php`, version constants, helpers, and any migration-time version checks.
- `composer.json`: `require.php`, relevant platform overrides, and any existing
  lockfile whose platform metadata is affected. Preserve dependency-management
  strategy; do not re-resolve unrelated packages just to change the floor.
- Installation/enablement language files and their actual language keys,
  including affected translations. Preserve placeholders and formatting.
- README requirements, compatibility notes, and maintained support tables.
  Distinguish historical test results from current support declarations.
- CI workflows, reusable-workflow inputs, setup scripts, primary PHP versions,
  matrices, lint jobs, and functional-test runtimes.
- Tests named for declared support, compatibility, requirements, or version
  matrices, not only tests whose filenames contain `ext` or `enableable`.
  Read assertions that couple Composer, documentation, language, and CI.

GitHub archives can omit `.github/`, `tests/`, or `docs/` through
`.gitattributes` `export-ignore`. An archive is not proof those files are absent.
Use the Git tree/full checkout or fetch exact GitHub blobs before concluding
that no support tests or workflows exist. Verify hashes before using local
copies to supplement a GitHub revision.

## Change the checks and the test environment together

- Compute a numeric PHP floor as `major * 10000 + minor * 100 + patch` when the
  extension uses `PHP_VERSION_ID`. Keep helper constants and string-version
  checks consistent with the requested policy.
- Make failure messages report the new requirement using each extension's own
  language file and package identity. Keep unrelated reasons intact.
- Run enablement and functional tests on PHP that meets the new minimum. Keep
  the existing database, operating-system, and functional test groups; update
  obsolete PHP selections rather than disabling groups to obtain a green run.
- A minor selector such as `8.3` alone does not prove the runner meets a patch
  minimum such as `8.3.36`. Verify how the setup action/script resolves versions,
  provision a sufficiently recent patch release, and check the actual runtime.
  Do not assume a patch selector is honored without checking its implementation
  or documentation. Preserve deliberate older-PHP syntax/rejection tests where
  they still test useful behavior, without trying to enable the extension there.
- Update old support assertions and data providers to the new contract. Add or
  retain rejection immediately below the floor, acceptance at the floor, and
  acceptance of a newer supported PHP line. Do not delete valid assertions or
  replace them with unconditional success. Narrow mocks may isolate an
  unrelated old-package test, but real version-rejection coverage must remain.

## Verify and finish

Run the project's relevant support/enablement tests and normal required CI.
Recheck retained dependency/conflict/DOM/cURL guards and any intentionally
preserved phpBB ceiling. Exercise boundary failures far enough to prove the
language file and key resolve to a useful reason.

Use source scans and simulated version constants as supplementary checks, not
as proof of execution on another PHP runtime or full board compatibility.
Report those distinctions plainly.

If CI fails, inspect the failing job before retrying or merging. An old-floor
assertion or obsolete CI runtime caused by this change belongs in the same PR.
Handle a genuinely independent pre-existing blocker separately under the
project's branch and approval rules. Do not skip a required check, weaken it,
or bypass protection to complete the version change.

Finish with the actual support policy, retained phpBB bounds, test evidence,
and any unresolved CI. Do not infer release authorization from a support change
or merge approval.
