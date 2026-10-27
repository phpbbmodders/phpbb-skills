# Pinned accessibility reference set

Reference set: **phpbb-a11y-2026-10-23**. These are deliberately selected publication snapshots, not a claim that every document is the newest edition. Use this set consistently until the user requests a reference-set update or explicitly specifies another target.

| Document | Pinned publication | Role | Local copy |
| --- | --- | --- | --- |
| [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/) | 12/12/2024 | Normative success criteria and conformance rules | [HTML](snapshots/wcag-2.2-2024-12-12.html) |
| [WAI-ARIA 1.2](https://www.w3.org/TR/2023/REC-wai-aria-1.2-20230606/) | 06/06/2023 | Normative ARIA roles, states and properties | [HTML](snapshots/wai-aria-1.2-2023-06-06.html) |
| [Accessible Name and Description Computation 1.1](https://www.w3.org/TR/2018/REC-accname-1.1-20181218/) | 12/18/2018 | Normative accessible-name computation | [HTML](snapshots/accname-1.1-2018-12-18.html) |
| [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/TR/2021/NOTE-wai-aria-practices-1.2-20211129/) | 11/29/2021 | Advisory widget and keyboard patterns | [HTML](snapshots/aria-practices-1.2-2021-11-29.html) |

## Use the local baseline

Read only the relevant sections of the saved HTML, using its headings/IDs to search. For ordinary reviews use WCAG 2.2 Level A and AA as the reference target unless the project specifies otherwise. Identify the actual criterion, level, evidence, and scope for findings. AAA criteria may inform optional recommendations but must be labeled AAA; do not silently make them AA requirements. Limited control checks do not establish whole-page/site conformance.

Start with WCAG criteria relevant to the changed control: non-text content (1.1.1), use of color (1.4.1), text contrast (1.4.3), reflow (1.4.10), non-text contrast (1.4.11), hover/focus content (1.4.13), keyboard and traps (2.1.1–2.1.2), focus order/visibility (2.4.3, 2.4.7), focus not obscured minimum (2.4.11), label in name (2.5.3), target size minimum (2.5.8), labels/instructions (3.3.2), name/role/value (4.1.2), and status messages (4.1.3). Read applicability, thresholds, definitions and exceptions in the snapshot before deciding a pass/fail; this list is a navigation aid, not replacement criteria.

Consult ARIA for semantics and accessible-name computation for naming questions. Consult the saved Authoring Practices note for the relevant button, link, dialog or other actual widget pattern. It is advisory guidance, not another conformance standard, and it must not override normative requirements. Prefer native HTML controls when they provide the required behavior. The tooltip-plus-localized-name rule in this skill is a phpBB project convention, not a universal WCAG requirement for every control to have a tooltip.

Do not follow a snapshot's links to “latest”, editor drafts, live Understanding/Techniques pages or changing example sites and silently treat those destinations as part of this set. The four standards/pattern documents above form the W3C baseline; additional manifest-listed screen-reader snapshots form a separate vendor supplement. Linked example source, CSS, scripts, referenced HTML specifications and errata are not mirrored by this bundle; the saved HTML is a local text reference, not a fully offline interactive example site. If another source is needed to resolve a gap, identify that gap and record its exact version/source separately; do not change the baseline implicitly. If the pinned standards conflict or leave an issue unresolved, report the ambiguity rather than inventing a rule.

## Screen-reader operation references

For NVDA, JAWS or VoiceOver setup, commands and actual spoken-output checks, read [the pinned screen-reader supplement](screen-readers.md). Its product/OS pins and explicit JAWS build limitation must be retained. Vendor operation guidance is separate from normative accessibility criteria.

## Integrity and updates

[manifest.json](manifest.json) records each dated source URL, title, publication date, retrieval date, byte length and SHA-256. The W3C HTML bytes retain their original copyright/license notices; vendor snapshots retain their respective notices. Do not remove those notices or present downloaded documents as original project material.

Run `python3 scripts/verify_references.py` from the skill directory before relying on the reference bundle. It verifies local bytes without network access and never refreshes files. The four W3C documents here are always stored with the skill. Only the Apple and JAWS screen-reader documents may be absent (they are local-only; see [the screen-reader supplement](screen-readers.md)). Any other missing file or a hash mismatch is a reference-integrity failure; restore the recorded exact bytes or report the problem rather than fetching an arbitrary substitute.

Upgrade deliberately: establish the requested new target, use official dated publications or a pinned official repository commit for undated material, review relevant changed requirements, save the new bytes and provenance, update the manifest and this guide together, run integrity checks and skill validation, then describe the changed baseline. Never auto-update on skill invocation. Keep the user's approved scope and review requirements for the update.

In a review report name **phpbb-a11y-2026-10-23 / WCAG 2.2 A and AA** (or the explicit project target), distinguish normative findings from advisory/project conventions, and cite the dated official document plus section. Do not claim assistive-technology testing that was not performed.
