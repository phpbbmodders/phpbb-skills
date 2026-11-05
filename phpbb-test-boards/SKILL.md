---
name: phpbb-test-boards
description: "Set up and verify disposable phpBB extension test boards using seed-forum and committed phpbb-test-board tools. Use for runtime, lifecycle, PHPUnit, or database testing; screenshot composition is a separate workflow."
---

# phpBB Test Boards

Inspect the real extension checkout, supported phpBB/PHP/database matrix, and existing harness before setup. Prefer committed tools over scratch replacements. The tools are [seed-forum](https://github.com/phpbbmodders/seed-forum) and `phpbb-test-board/` in [phpbb-release-tools](https://github.com/phpbbmodders/phpbb-release-tools); locate the local checkouts and read their help before using remembered flags.

## Board identity and safety

Check listeners with `ss -ltnp` and select an unused isolated port. Never stop, reuse, or reconfigure a port held by a service the task did not start; it may be one of the user's own services.

Use seed-forum's configured extension bind mounts for interactive boards. Inspect `config/local.yml.example`, validate the board configuration, and use the tool's mount/remount/status operations. Verify `mounted=True`, the source checkout/ref, and actual mount paths before trusting results, especially after reboot or checkout changes. Never repair a stale board by manually copying extension files over it.

A reset must target a confirmed disposable board. Before removing a board directory, unmount its extensions and verify no bind mounts remain; deleting through a bind mount can delete source code. Preserve persistent boards and unrelated services.

## Run the actual checks

Test every code change on a running board before opening its pull request, not after merging it. Lint, EPV and a standalone call of the changed function do not count as that test. seed-forum needs sudo for its bind mounts and nginx sites. Some agent runtimes cannot use sudo at all: Claude Code sets the kernel's no-new-privileges flag (`NoNewPrivs: 1` in `/proc/self/status`), even with its sandbox off. There, run the sudo steps (`--reset`, `--mount`, `--remount`, `--unmount`, `--purge-cache`) in the user's own terminal, which the agent can drive when the app offers that, and read the output from it. Do not build a sudo-free workaround. Never report the board test as skipped because setup was inconvenient.

Use committed `smoke_test.py`, `feature_checks.py`, and `run-unit-tests.sh` where relevant. Inspect their current interfaces and dependency installation options. The unit-test runner manages its own fresh test copies and compatible phpBB/PHPUnit checkout; that is distinct from manually copying an interactive board. Preserve a required `tests/functional/` directory when the framework enumerates it.

Provision supported database cases rather than calling a SQLite pass universal. Run guest/admin routes, real ACP/MCP/UCP actions, cron, permissions, and disable/purge/enable lifecycle cases that the change affects. Add reusable feature checks to the committed harness when appropriate. Do not let a green lint/EPV run stand in for runtime evidence.

Purge through seed-forum or the correct board owner when CLI cannot remove web-owned cache. For `php -S`, disable opcache in the disposable test runtime. Empty pages may hide PHP fatals: inspect response bodies and logs before diagnosing flakiness. Wait for phpBB's form timing/CSRF requirements before submitting browser forms.

If setup blocks a required check, repair feasible scoped infrastructure and rerun. Report the board version, code ref, PHP/database, checks and actual failures. Never substitute an unrelated test file or claim a skipped check passed.
