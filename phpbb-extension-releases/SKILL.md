---
name: phpbb-extension-releases
description: "Prepare, package, publish, and verify phpBB extension releases or explicitly requested rolling development refreshes using the shared release tools. Does not authorize a release from a merge alone. Use when asked to tag, package, publish, or refresh a dev release of an extension, run git-release-api.sh, or check a release ZIP's contents."
---

# phpBB Extension Releases

Establish the requested release type and project versioning policy. A merged PR or support-floor change does not imply release authorization. Preserve existing version strategy; do not refresh a rolling development build after every small merge unless requested.

Fetch and inspect the actual remote default branch and local divergence before packaging. Pin the exact source commit. Verify Composer version, enablement requirements, changelog, release notes and compatibility claims refer to the same candidate. Run the required extension validation and relevant real runtime checks, including informational findings when remediation includes them.

Inspect the current `git-release-api.sh` from a [phpbb-release-tools](https://github.com/phpbbmodders/phpbb-release-tools) checkout and its help. It packages the remote default-branch commit; uncommitted local edits are not release contents. Run its dry-run before an authorized release. Check the archive root, composer identity/version, expected runtime files, and `.gitattributes` export exclusions. Avoid accidentally excluding internal runtime files with broad filename filters.

For a new release, use the tool's existing-tag/release protections and draft/upload/verify/publish sequence. Replacing a published version or moving a rolling tag requires explicit authorization for that behavior; never turn a collision into an automatic overwrite. After an interrupted request, inspect live tag, draft/release, and assets before retrying to avoid duplication.

Verify the published tag resolves to the pinned commit, release notes match it, and the downloadable asset has the expected contents/hash. Report source push, PR merge, tag, release publication, and forum posting as separate actual states, with direct URLs for completed remote actions.

Prepare forum drafts through the development-topics workflow when requested: refresh the existing first post and add an update reply in the same topic. A published development build is not a CDB-validated release. Public draft approval and posting remain governed by the user's current rules.
