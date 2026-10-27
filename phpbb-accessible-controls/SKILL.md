---
name: phpbb-accessible-controls
description: "Implement or review accessible phpBB board and ACP controls, including icon labels, keyboard focus, clipboard feedback, responsive layouts, and browser verification. Use when adding or reviewing icon-only links/buttons, tooltips, sr-only labels, focus handling, copy-to-clipboard feedback, or a WCAG check of phpBB templates."
---

# phpBB Accessible Controls

## Fixed reference baseline

Before reviewing or changing accessibility behavior, read [the pinned reference guide](references/baseline.md) and verify its local documents with `python3 scripts/verify_references.py` from this skill directory. For screen-reader setup or spoken-output checks, also read [the pinned screen-reader supplement](references/screen-readers.md), including its product/OS versions and JAWS exact-build limitation. The Apple and JAWS copies are local-only and may be absent; then use their publisher links and say so. Use the saved W3C and vendor publications in these guides; do not independently search different sites or editions for routine checks. Keep the baseline fixed until a deliberate update is requested, and report any explicit project target that differs. The guide distinguishes WCAG conformance criteria, ARIA semantics, advisory patterns and phpBB conventions.

## Tooling setup subskill

For installing, preparing, or diagnosing accessibility test tools, use the [accessibility-toolkit-setup subskill](../accessibility-toolkit-setup/SKILL.md). It covers Playwright and axe setup, gradient/state contrast review, bounded browser accessibility-tree inspection, and isolated Linux Orca announcement logging. Read it when the test environment needs setup or repair; routine control changes can reuse an already verified environment.

Keep this skill's fixed standards and vendor-reference baseline authoritative. The setup subskill does not refresh those pins or substitute Linux Orca coverage for the documented NVDA, JAWS, or VoiceOver platforms. Distinguish generated announcements from actual audio playback and human listening, and include standalone exported HTML when it is part of the requested output.

## phpBB controls

Inspect the affected style and current templates. Keep native phpBB semantics, language loading, permissions, and visual conventions. Add accessible behavior within the requested UI scope rather than restyling unrelated pages.

For an icon-only board link/button, provide a localized tooltip and accessible name from the same language string. Prosilver supports an inner `span.sr-only`; mark decorative icons `aria-hidden="true"`. Use `aria-label` where a span is unsuitable. A title alone is insufficient. ACP's standard stylesheet lacks prosilver's `sr-only` class: use `aria-label` there unless the actual ACP stylesheet defines an equivalent visually hidden utility.

Preserve a visible keyboard focus indicator and semantic links/buttons. For a same-page action, verify focus remains at or returns to the meaningful target. Where a fragment change is involved, change the URL fragment before restoring focus; otherwise browser navigation may steal focus. Check the actual result with keyboard and browser accessibility-tree inspection.

For clipboard/actions with transient feedback, test success and failure, unavailable APIs, repeated activation, and reasonable fallback behavior. Ensure status is conveyed without relying only on color or an icon, and the underlying link/content remains usable where JavaScript is unavailable. Do not announce more screen-reader coverage than actually performed.

Use the current `phpbb-test-board/template_a11y.py` when available as a source check, then verify affected board and ACP views in a browser, including keyboard navigation, narrow viewports, and relevant permission states. Static scans and screenshots do not prove spoken output or full accessibility compliance. Keep meaningful reusable interaction checks in the existing test harness.
