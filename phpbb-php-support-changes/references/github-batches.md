# GitHub batches

Use this reference when the version change spans multiple repositories. It
supplements the support-consistency checks in `SKILL.md`; it does not grant
permission to post public text, merge, unarchive, or release anything.

## Inventory and scope

- Honor the requested tool. If the user asks for GitHub and `gh`, inventory
  current organization repositories through `gh`, with pagination, instead of
  treating the local clone directory as the complete organization.
- Identify actual phpBB packages from current metadata and source. Account for
  missing `ext.php` files and malformed metadata explicitly. Do not silently
  omit a repository or fix unrelated malformed metadata as a side effect.
- Maintain exclusions and ownership handoffs from the conversation. If an
  exclusion arrives after a branch was created, remove only the task-created
  branch after verifying its expected SHA; preserve default-branch work.
- Record initial archive status. Archived repositories are read-only. Obtain
  authorization before temporary unarchiving, and restore their initial state
  after the approved work or on failure. Keep repositories open for CI only as
  long as the authorized workflow needs them.
- Separate changes per repository. Preserve unrelated local changes and
  concurrent GitHub work. Compare the source blobs to the inventoried revision
  before publishing, and stop on drift rather than overwriting it.

## Publishing and evidence

Follow the applicable public-text approval and attribution rules. A shared PR
draft can be approved for a batch when the same exact text accurately describes
every PR. Keep exceptions explicit. Verify each live posted body and attach
each created PR to the chat when an attachment tool is available.

Persist enough state to resume safely: repository, original archive state,
base SHA, source branch, expected head SHA, PR URL, current checks, and result.
Use bounded concurrency and GitHub rate limits. Never blindly repeat a
non-idempotent create after an uncertain response; read whether it succeeded.

GitHub's PR head field can lag a successful Git ref update. Verify the
authoritative branch ref and use bounded read-only retries for the PR view.
Save the new commit/ref outcome durably before depending on that view. Do not
create a duplicate commit because a PR refresh is delayed.

## CI and merges

- Keep one merge owner per PR where practical. A repair changes the expected
  head; update durable state and ensure a stale worker cannot merge it. Guard
  merges with the exact expected commit, such as `--match-head-commit`, and use
  separate result files for independent workers.
- Check all current relevant results and GitHub merge requirements. Keep
  passing, pending, failed, cancelled, and not-configured checks distinct.
  No checks is not a passing CI run. Do not use admin/force overrides or weaken
  protections. Merge only within the user's existing authorization.
- Continue independent eligible repositories while diagnosing failures. Do not
  assume one PHP-floor repair fixes every extension's custom support tests.
- If a bounded CI wait expires, preserve the pending state and restore any
  authorized temporary archive changes; do not claim the batch complete.
- Follow Codex Process Jobs lifecycle instructions when available. A background
  job may report an earlier failing head after a separate repair has merged.
  Reconcile final counts against live PR states and current heads before
  reporting overall completion.

Verify merged state, intended branch cleanup, and restored archive status.
Provide direct PR links and distinguish completion of the job from completion
of every repository in the batch.

## Observed failure pattern

During a security-floor update, Knowledge Base and Wiki had tests that coupled
their old Composer/README/CI requirements to `ext.php`; updating only the gate
left those tests correctly failing. Ban Hammer also ran functional enablement
tests under a PHP version the new gate rejected. The reusable lesson is to
discover support contracts and provision supported test runtimes before
publishing. The particular version numbers, repository exceptions, and people
handling excluded extensions are task-specific and must not become permanent
defaults.
