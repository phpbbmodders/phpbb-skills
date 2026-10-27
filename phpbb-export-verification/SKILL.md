---
name: phpbb-export-verification
description: "Validate phpBB personal exports and static archives for visibility, privacy, rendering fidelity, output completeness, and real-data failures before publication. Use when checking a personal data export or static archive (HTML/ZIP/SQL conversion) for leaked private content, broken rendering, or missing data before release."
---

# phpBB Export Verification

Identify whether this is a personal data export or public static archive. Inventory included categories and visibility rules for posts, private messages, attachments, profiles and moderation data. Use an authorized disposable local copy for sensitive real data; do not publish a database, SQL dump, credentials, PM attachment, or private reference document with the output.

Build synthetic fixtures for each relevant permission/visibility case, including deleted/unapproved content, private forums, unavailable attachments and non-ASCII/BBCode content. Apply one consistent eligibility rule to category counts, queries, rendered entries and attachments. Prefer core visibility/log/text-rendering services to reimplementing authorization or unserializing log internals.

Test HTML and ZIP outputs where supported. Validate the archive, relative assets, link/board URL handling, smileys, attachment ordering and filenames, and offline rendering without network-only fonts or assets. Treat dump-derived HTML, URLs and paths as untrusted. Keep temporary databases and manifests containing private information outside publishable output.

A complete ZIP, HTTP 200 and empty server log are insufficient. Inspect generated HTML for rendered PHP warning/notice/fatal markup as well as broken images, empty sections and count mismatches. Exercise both a small fixture and an authorized large representative account/dataset; diagnose output errors and rerun before claiming readiness.

For SQL archive conversion, distinguish structural dump checks from relational fidelity: compare imported row/field counts, missing topic/first-post relationships, Unicode and replacement characters. Test entity and code-block rendering through the real phpBB storage/preview boundary before blaming stored data; a CLI seed tool can itself double-decode entities.

Use the project's incremental render mode for template-only checks if it preserves relevant inputs; run a full export when fetching/import behavior changes. Report the tested dataset scope and a safe real example URL or artifact. Do not expose private content merely to demonstrate a result.
