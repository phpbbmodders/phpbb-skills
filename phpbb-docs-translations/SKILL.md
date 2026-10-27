---
name: phpbb-docs-translations
description: "Maintain phpBB documentation translation catalogs, terminology, and generated builds across source and languages repositories using the established gettext workflow. Use when updating PO catalogs, running translations.sh, fixing terminology, adding a docs language, or rebuilding translated phpbbdocs output."
---

# phpBB Documentation Translations

Read the current source repository's translation plan, script help and sibling-language contract before editing. Distinguish implemented commands from planned architecture. For phpBB these are [phpbbdocs-hugo](https://github.com/phpbbmodders/phpbbdocs-hugo) and [phpbbdocs-languages](https://github.com/phpbbmodders/phpbbdocs-languages); verify current paths and do not resurrect retired DocBook/Pandoc or Crowdin workflows from old notes.

Keep canonical PO catalogs and translator terminology in the languages repository; source synchronization, POT generation, reconstruction and documentation builds belong to the source toolchain. Configure `LANGUAGES_REPO` once where the existing tool supports it. Use the current `translations.sh` init/update/status/check/build and developer-docs commands rather than editing generated output as the translation source.

Honor the project's language-code mapping. In these phpbbdocs repositories every per-language directory uses the exact phpBB variant code with underscores, such as `de_x_sie`; do not collapse a formal variant to `de` or a display locale. Filenames can follow their established descriptive naming separately.

Inspect source context and the actual matching phpBB language pack for UI terminology. Preserve PO context, references, placeholders, fuzzy/obsolete state and literals/code blocks. Keep translator-editable prose/glossary fields distinct from mechanical audit material; machine QA does not establish human prose approval.

Before regenerating tracked XML/content, inspect the working tree and preserve unrelated edits. Run update/check/build for affected language and source families, inspect representative rendered output and source links, then check cross-repository and Wiki references after moves. Developer-docs generated output may be ignored and need an explicit build even when end-user XML is tracked.

Where source revision metadata exists, advance it only after successful updates; a failed extraction must not mark translations current. Verify the recorded revision actually corresponds to generated catalogs. Do not introduce planned metadata or tooling as though it already exists.

If Wiki edits are requested, verify manual initialization first; if absent, stop Wiki work and provide its URL for the user to create a first page. Report catalog/build results separately from translation review completeness.
