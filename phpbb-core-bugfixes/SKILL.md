---
name: phpbb-core-bugfixes
description: "Investigate and fix phpBB core bugs across maintained branches with focused regressions, preserved legacy behavior, branch-specific source checks, and upstream-ready evidence. Event-only RFCs use the event-RFC skill. Use when reproducing or fixing a phpBB core bug, writing its regression test, porting the fix between 3.3.x and master, or preparing the tracker ticket and PR."
---

# phpBB Core Bug Fixes

Verify the reported trigger against current target-branch source and a minimal reproduction. Trace the complete request/service/storage/render/redirect path and permission checks before choosing the smallest fix. Attribute downstream warnings to their originating failure; a missing language key alone does not prove an entire phpBB upload is incomplete.

Record relevant branch differences and existing behavior. For persisted notification or configuration data, test both newly created and legacy records; new optional fields should not break older serialized data. Preserve identity/deduplication, parent IDs, forum/read permission resolution and unrelated notification types unless changing them is required.

Write focused regression coverage that fails on the original behavior and exercises the real phpBB class lifecycle. Test the supported PHP/database combinations required by the affected component. When a helper API differs between 3.3.x and master, implement the branch-specific fix instead of assuming a clean cherry-pick proves compatibility.

If forward application conflicts, inspect why and prepare separate branch work where appropriate. Do not weaken ACLs, change schema, or broaden templates to avoid understanding a narrow route/identity bug. Inspect actual runtime redirects as well as generated board/email URLs when links are involved.

Use a verified tracker ticket and the repository's upstream workflow. For tracker affects-version fields, choose the appropriate upcoming unreleased version from the live tracker list rather than inventing a version from memory. Draft complete public text with the current required attribution and obtain the user's required approval before posting. Use a verified agent URL; never mechanically substitute an agent name into another vendor's URL.

After an authorized PR, attach and return its direct URL and reconcile live CI for the actual pushed commit. Report baseline failures, new failures and remaining limitations accurately. Event-only additions belong to the existing event-RFC-to-PR workflow rather than duplicating its procedure here.
