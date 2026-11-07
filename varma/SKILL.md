---
name: varma
description: "Run a full maintenance pass over one phpBB extension and do only what it needs: revendor, phpBB 3.3/4.0 baseline, organization modernization, open PRs and issues, dependent extensions, validation, accessibility, board tests, language packs, screenshots, wiki, and the development-topic announcement or update. Use when the user types /varma, asks for a varma pass, or asks for an extension to be brought fully up to date or given the usual full treatment."
---

# varma: full extension pass

One extension per run. varma decides which steps the extension needs, gets the user's go-ahead on that plan, then runs each step through the skill that owns it. It adds no rules of its own beyond the checks below; the linked skills hold the details, so follow them in full for every step that runs.

## 1. Inventory

Before changing anything, read the extension's current state:

- `composer.json`: vendor and name, version, `require.php`, `extra.soft-require`, `extra.version-check`, authors, homepage, description.
- `ext.php`: the phpBB and PHP minimum checks, and any rename guard.
- Namespaces, service ids, migrations and their `depends_on`, module `auth` strings, routes, cron task names.
- Templates under `styles/` and `adm/style/`, and every page or control the extension adds.
- Language folders other than `language/en/`.
- CI workflows, `.gitattributes` and line endings, `.github/FUNDING.yml`, donation blocks in templates or language files.
- The README against [the organization conventions](references/conventions.md), and `docs/images/screenshots/`.
- On GitHub: open pull requests and their mergeability, open issues and their age, the repository description, topics, labels and Projects setting, and whether the wiki has its first page.
- Other extensions that require this one, use its services or events, or depend on its migrations.
- Whether a current-maintainer development topic exists, through the [development-topics](../phpbb-development-topics/SKILL.md) records.
- The test tools: whether phpbb-release-tools already has a feature check, a screenshot recipe and an upgrade path for this extension.

## 2. Plan, then stop

List only the steps below whose check says they are needed, each with one line saying why, in the order they will run. List the steps that are not needed in a single line, so the user can see they were checked. Then wait for the user's go-ahead. A step the user removes is not run.

## 3. Steps

Run in this order. Each step's check decides whether it runs.

| Step | Runs when | Follow |
| --- | --- | --- |
| Revendor | the vendor is not the organization's | [adoption](../phpbb-extension-adoption/SKILL.md) |
| Baseline | the phpBB or PHP minimum is behind the organization's, or the code fails on phpBB 4.0 | [PHP support](../phpbb-php-support-changes/SKILL.md), [cross-version](../phpbb-cross-version-compatibility/SKILL.md) |
| Modernize | any item in [the conventions](references/conventions.md) differs | the conventions file |
| Open PRs and issues | a PR conflicts with the work or with `main`, or issues are open | below |
| Dependent extensions | another extension depends on this one | [adoption](../phpbb-extension-adoption/SKILL.md), dependency order |
| Validate | always | [validation](../phpbb-extension-validation/SKILL.md) |
| Accessibility | the extension ships templates | [accessible controls](../phpbb-accessible-controls/SKILL.md) |
| Board tests | always | [test boards](../phpbb-test-boards/SKILL.md) |
| Language packs | other languages exist and keys were added, renamed or removed | below |
| Screenshots | the extension has a UI and has no screenshots, or its UI changed | [screenshots](../phpbb-extension-screenshots/SKILL.md) |
| Wiki | the extension needs wiki pages | below |
| Announcement or update | the extension's code or features changed since its last announcement or update post, or the user asks for one | [development topics](../phpbb-development-topics/SKILL.md) |

Step notes:

- **Validate:** fix every finding, advisory ones included, then validate again until the report is clean. Run EPV on both phpBB branches, the code sniffer, `php -l`, and PHPUnit when the extension has tests.
- **Board tests:** phpBB 3.3 and 4.0 boards, the full supported database matrix, the upgrade from the last release under the old name after a revendor, and from the last release otherwise. When the test tools have no feature check or screenshot recipe for this extension, add one to phpbb-release-tools in its own pull request.
- **Open PRs:** rebase a pull request that conflicts with this work after this work is merged, onto the new code, and test it again. Never close or rewrite someone else's pull request without the user's say. Issues: under four years old and fixed, reply that it is fixed and close; four years or older, close; still valid, add to `docs/TODO.md`. Show each reply before posting.
- **Language packs:** add, rename or remove the same keys in every shipped language. Flag any new English text that still needs translating; never machine-translate it into a shipped pack without saying so.
- **Announcement or update:** count every change merged since the last post, including earlier passes and other pull requests, not only this pass. Find the existing development topics on each forum the organization announces on; draft the first-post announcement and the update reply, and a new topic only when none exists. Posting a new topic needs the user's say like any other post.
- **Wiki:** check that the wiki has its first page. If it does not, stop the wiki step, give the user the wiki URL to create that page, and carry on with the other steps.

## 4. Gates

- Show every pull request body, issue or PR comment and forum post in full, and get approval before posting it. Check the live text after posting.
- Merge only when the user says so, after CI passes.
- Never bump the version for a release, tag, publish or refresh a release package as part of a pass. Note it as a decision for the user. A development version such as `x.y.z-dev` that marks a vendor change may be proposed in the plan.
- Remove the test boards after the last merge.

## 5. Report

End with the merged pull requests (title, link, merge commit), anything left for the user (a wiki first page, a version decision, an untranslated string, a forum post not yet made), and the follow-ups the pass found but did not do.
