---
name: phpbb-cross-version-compatibility
description: "Implement and verify phpBB extension compatibility across 3.3.x and 4.0 using native routes, version-specific templates, and real branch-specific runtime checks. Use when adding phpBB 4.0 support to an extension, fixing something that works on one branch but not the other, or splitting version-specific templates."
---

# phpBB Cross-Version Compatibility

Identify exact supported branches, current PHP requirements, and the affected interface before editing. Inspect each branch's actual source rather than assuming a shared API. Keep compatibility changes targeted and preserve repository-specific guards and upper bounds; changing PHP support is a separate coupled-declaration workflow.

Use phpBB route helpers instead of hardcoding `app.php`: route entry points differ between 3.3 and 4.0. Check generated URLs, browser redirects, query parameters, permissions and session handling in both runtimes. For notification redirects, inspect `get_redirect_url()` and the caller: HTML-escaped separators can survive a 4.0 redirect even if a 3.3 redirect decoded them.

Twig resolves some functions at compilation time. A 4.0-only function such as `Icon()` can fail on 3.3 even inside an unselected conditional branch. Isolate incompatible syntax into version-specific partials selected through a supported dynamic include, and compile/render both paths on the target branches. Do not hide unsupported code behind a conditional and call it compatible.

Recheck event signatures, services, migration/db_tools behavior, template events, and language keys on each branch. When an extension point is missing, document the required core event under `docs/events/` and use the event-RFC workflow if requested; do not patch core as an extension workaround.

Test the real checkout on separate seed-forum configurations for each supported branch, with actual pages and lifecycle checks. Purge the appropriate cache after changing refs. Run branch-appropriate unit/database suites and browser checks for changed routes/templates. Distinguish syntax/source inspection from runtime coverage and disclose any remaining branch-specific limitation.
