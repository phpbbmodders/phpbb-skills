---
name: phpbb-language-pack-releases
description: "Validate and package a phpBB language pack against the matching official phpBB release, checking validator summaries and exact CDB archive contents. Use when validating or building a language pack ZIP, running git-release-langpack.sh or the translation validator, or preparing a CDB language submission."
---

# phpBB Language Pack Releases

Identify the exact phpBB target version, language variant/ISO code and pack version. Verify current official release metadata rather than reusing a remembered stable version. This workflow packages board language packs, not Hugo documentation translations.

Inspect `git-release-langpack.sh` from a [phpbb-release-tools](https://github.com/phpbbmodders/phpbb-release-tools) checkout or its current equivalent and read its help. Use the maintained tool rather than old copies in misc or memory assets. Confirm the source ref and release layout before checking or building.

Use the official phpBB release ZIP as the English reference and verify its published checksum. Do not substitute extension/repository master contents for a stable release reference; that can create false missing-file findings. Select a translation-validator branch supporting the requested phpBB line. Historical guidance used validator 1.6.x for phpBB 3.3 and master for 4.0; verify that mapping against current validator source before use.

Parse the validator's summary as well as the process exit status. Its exit code may represent fatal findings only: check `Fatal` and `Error` counts, preserve warnings for review, and fail the verification if the expected summary is absent. Do not label an error-bearing pack valid because the command exited zero.

Validate the exact distributable roots (`ext/`, `language/`, `styles/` as applicable), excluding repository-only README, SECURITY and development files from the CDB package. Confirm the ZIP and its top-level folder follow the target's language-name/version convention and contain the same candidate just validated. Preserve placeholders, Unicode and variant-specific wording.

For CDB metadata, verify the current submission requirements; retained workflow uses an English description, flag-only screenshot, and no unrelated demo URL. Building an archive does not authorize uploading or publishing it. Report validator counts, reference version/checksum, artifact path and packaging verification separately.
