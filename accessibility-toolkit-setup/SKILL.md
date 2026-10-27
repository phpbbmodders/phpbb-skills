---
name: accessibility-toolkit-setup
description: Set up and diagnose browser accessibility checks, contrast review, and isolated Linux Orca announcement testing. Use when preparing or repairing accessibility test tooling, including for standalone HTML; platform-specific screen readers require their actual supported OS.
---

# Accessibility Toolkit Setup

Prepare reproducible tools for the requested accessibility checks, preserving the user's desktop and application data. This skill prepares and diagnoses the test environment; the calling project skill defines the controls, standards baseline, permissions, and acceptance criteria.

## Select the required evidence

Run `python3 scripts/inspect_tools.py` for a read-only inventory. Verify the actual interpreter, browser binary/build, Playwright package/browser installation, axe-core version, and screen-reader version used. Reuse an existing project test environment when practical. Missing imports in a virtual environment do not prove a package is absent from the host.

Distinguish these outcomes in reports:

- axe findings and incomplete rules;
- keyboard navigation, focus, responsive reflow, names/roles/states, and accessibility-tree checks;
- reviewed contrast calculations, including gradients and hover/focus states;
- real screen-reader-generated announcements;
- actual audio playback or human listening, when performed.

Neither a clean scan nor an accessibility tree establishes spoken output or WCAG conformance. An incomplete axe rule is a review item, not an automatic pass or failure. Record reader/browser compatibility problems separately from defects in the tested application.

## Browser and contrast tools

Use the project's browser harness or the available Playwright skill. Install missing dependencies only where the task permits, preferably in temporary or project-isolated storage. Verify package versions through the relevant package manager before selecting a pin. Do not silently replace a caller's fixed standards or vendor-reference baseline.

Use [browser checks](references/browser-checks.md) for axe, bounded accessibility-tree queries, gradient/button contrast, and private standalone exports. `scripts/contrast.py` computes an opaque sRGB foreground/background ratio; it deliberately does not resolve CSS, alpha compositing, images, or gradients.

## Screen-reader setup

For Linux Orca, read [the isolated setup procedure](references/orca-linux.md). It covers temporary package extraction, private Xvfb/D-Bus sessions, announcement-only logging, process cleanup, and the host-wide single-instance guard. Use `scripts/orca_announcement_runner.py` only inside that isolated session. It preserves Orca's real event handling and announcement generation while disabling the audio backend; never describe this mode as listened-to speech.

For an existing live user desktop, preserve the user's reader, settings, keyboard map, and audio routing. Do not replace or terminate a reader already in use. NVDA/JAWS require Windows and VoiceOver requires its supported Apple OS; Linux Orca coverage cannot substitute for them. Consult the calling skill's pinned vendor guidance before choosing reader navigation commands.

## Completion

Run a small known-good control before testing the target. Then verify its actual changed name, role, state, focus behavior, and relevant announcements. Keep private exports, DOM captures, and announcement logs outside public artifacts. Use synthetic fixtures where sufficient; preserve exact relevant markup when extracting a focused real-data test case, and report that narrowed scope.

For finite checks expected to exceed about a minute, use the environment's durable process-job workflow when available and follow its completion/result rules. Clean up only processes and temporary resources created by the test. Report concrete remaining environment limitations after feasible diagnosis, rather than claiming unavailable checks passed.
