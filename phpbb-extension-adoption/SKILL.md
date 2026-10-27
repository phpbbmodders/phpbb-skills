---
name: phpbb-extension-adoption
description: "Plan and verify phpBB extension maintainer or vendor transitions while preserving existing installations, migration dependencies, configuration, and dependent extensions. Use when taking over or transferring an extension, renaming its vendor/namespace, or testing upgrades from the previous maintainer's release."
---

# phpBB Extension Adoption

Verify ownership/transfer and requested identity change from current evidence. Adoption does not necessarily require renaming the Composer package, namespace, extension directory, or migration classes. Preserve established identities unless the task calls for a vendor transition. Describe transferred maintenance accurately rather than automatically calling it a fork.

For a requested rename, inventory old/new extension names, namespaces, configuration keys, services, events, permissions, tables, migration names and dependencies. Search dependent extensions as well as the provider. Preserve existing data and applied migration history; never solve adoption by purging extension data or rewriting previously applied migration definitions.

Inspect the project's actual transition implementation. Renamed migration records can appear not to have run; migrating their identity must also account for every stored `migration_depends_on` reference, including dependencies in other extensions and rollback paths. Work within the existing extension lifecycle and use localized refusal messages for conflicting old installations.

Test both fresh installation and upgrade from a genuine old release with nondefault settings and representative content. Compare configuration, row counts, permissions, extension/migration records, files, and actual routes before and after. Verify migrations do not replay and reset settings. The shared test tooling includes `phpbb-test-board/rename_upgrade.py`; inspect current help and coverage before using it. Do not invoke a helper that resets the database halfway through an upgrade test.

Test dependency order separately: disable hard-dependent extensions before their old provider so the container does not retain dangling service references; enable the new provider and then dependents. Verify optional integrations and event/service names too. A provider-only upgrade test does not prove the dependent chain works.

Run static validation and the relevant runtime/database matrix. For public adoption replies or a new current-maintainer development topic, use the development-topics workflow and verified project records; do not revive a historical maintainer's topic as a substitute.
