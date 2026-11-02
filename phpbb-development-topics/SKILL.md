---
name: phpbb-development-topics
description: Prepare, create, or update phpBB extension development forum topics using announcement/update BBCode files, topic-prefix selection, duplicate checks, and a persistent topic-creation record. Use for extension development announcements and release-update posts; also handles CDB responses for adopted extensions that need a new current-maintainer development topic. Ordinary support replies do not create a development-topic record.
---

# phpBB Development Topics

Follow the user's current project-specific instructions and posting approvals. A request to discuss or draft a topic does not authorize posting it. Creating this skill does not authorize creating a forum topic.

## CDB discussion sub-workflow

For a Customisation Database (CDB) discussion/support response concerning an adopted extension, when a development announcement is part of that response and no current-maintainer development topic has been verified, read [CDB responses for adopted extensions](references/cdb-adopted-extensions.md). It coordinates the new development topic with the original CDB reply. After successful posting, include both the development topic URL and the exact CDB reply permalink in the final chat response. A CDB support topic is not a substitute for a development topic; posting a reply does not authorize creating another topic.

## Find the correct topic before writing

Search the topic-creation memory for the project/repository and purpose before creating a topic:

- Search the agent's configured project/user memory for the repository, extension title, and `topic-creation` records. Also check project-owned topic records in the release-drafts directory. Verify records live before acting.
- Open any recorded topic and verify its site, title, project, purpose, and current-maintainer ownership. A support topic, an announcement on another site, or a previous maintainer's topic is not the current development topic.
- If no usable record exists, search the relevant forum for an existing current-maintainer development topic. No memory hit does not prove that no topic exists. If lookup is inconclusive, resolve that uncertainty before creating a duplicate.
- For an adopted extension, distinguish the previous maintainer's historical topic from the current-maintainer development topic. When the user requests a new maintainer topic, leave the historical topic untouched. Describe the actual maintenance relationship accurately; do not call an adopted project a fork without evidence.

An extension can have a current-maintainer development topic on more than one forum, such as the maintainers' own board and phpBB.com. Check each forum the project announces on, and update every one of its topics in the same way.

Use a verified existing current-maintainer topic for updates. Do not open a new topic for each release. Keep extension-specific names, IDs, URLs, ownership history, and created-topic records in project records or the configured persistent memory, not hard-coded into this reusable skill.

## Announcement means the development topic's first post

The "forum announcement" is the first post of the extension's existing Extensions in Development topic, not a separate announcement topic. Create a current-maintainer development topic only when none exists after the duplicate checks. Do not create a new topic for each release or announcement revision.

For subsequent releases, update that same topic's first post from the announcement BBCode file and add the update BBCode as a new reply in that same topic. Keep the required Community section in the updated first post. The two files are drafting sources for these two posts, not instructions to create two topics.

## Prepare the two canonical files

Keep two `.bbcode.txt` files in the release-drafts directory, `repo-releases/<github-repository-name>/` beside the repository checkouts (not inside the extension repository): the complete announcement and the release update. Inspect existing project files and established neighboring templates before choosing names or formatting; preserve unrelated drafts.

- **Announcement:** the complete forum-topic first post reflecting the latest version, current maintainers, real requirements, download, source, relevant documentation/screenshots, and the required Community section below. The BBCode file is the canonical draft; the announcement itself belongs in the forum topic.
- **Update:** a self-contained release-update reply with the actual version, changes, and download/release link. Match the established update format rather than copying the whole announcement.

### Update screenshot gallery

Every update post ends with a screenshot gallery of what changed in that update. Prepare it in the extension repository together with the update draft, not after posting: a `docs/update/YYYY-MM-DD/` folder with two or three screenshots of the recent changes and its own captioned `README.md`, as described in `docs/forum-update-posts.md` in [phpbb-release-tools](https://github.com/phpbbmodders/phpbb-release-tools) and the `phpbb-extension-screenshots` skill. The update post shows those images with `[img]` and links to the dated `README.md`; a link to the full screenshot gallery may be added but does not replace it. Point the `[img]` URLs at the commit that added the gallery (`raw.githubusercontent.com/OWNER/REPO/<commit>/docs/update/...`) rather than a branch, so the post keeps showing the same images if later commits change or move them. That commit must be pushed before the post goes up, so the images load. If an update has nothing visible to show, ask the user before posting it without a gallery.

### One draft, several forums

When the same update goes to more than one forum, reread the draft for each one. Change only wording that would be wrong there, such as "in this topic" for something that happened on another forum, and show the user each changed line for approval.

Use stock phpBB BBCode and the supported `[c]` inline-code tag. Validate tag balancing, links, and claims against current source and verified releases. Do not claim an unpublished release is available. Present drafts in four-backtick fences when displaying their complete text in chat.

### Required Community section

Always include the phpBB Modders forum and Discord links in every forum announcement, including replacement first posts during updates. A source link, issue tracker link, or CDB reply does not replace this section. Preserve the established community block:

```text
[color=#8000BF][size=120][b]Community:[/b][/size][/color]
[url=https://www.phpbbmodders.com/community/][img]https://img.shields.io/badge/Join_Our-Forum-862C23?logo=phpbb&logoColor=white[/img][/url] [url=https://discord.gg/CJab3Asm8z][img]https://img.shields.io/badge/Join_Our-Discord-5865F2?logo=discord&logoColor=white[/img][/url]
```

Check that both destinations and their links survive the rendered preview before posting. Follow a newer user-supplied community destination if the user changes these links. Do not automatically add community promotion to an ordinary CDB support reply or post an announcement without the required wording approval.

Follow the user's current attribution/disclosure rules. Before drafting, look them up in the agent's persistent memory and instructions for each forum the post will go to, since they can differ between forums and between first posts and replies (for example, a closing note naming the AI assistant that wrote a reply), and apply them to every post written for the user. Obtain approval for the complete public wording, including its closing line, before posting or editing. Retain approval already given for unchanged text; a maintainer correction must carry through the draft and actual post. Never infer permission to send from a release publication alone.

## Create a new topic

Only after duplicate checks and posting authorization:

1. Open the correct development forum's new-topic form.
2. Select **[3.3][DEV]** from the **Topic prefix** dropdown first for this phpBB 3.3 development workflow. If the project explicitly targets another prefix, follow that requirement instead. Do not guess an unavailable dropdown value.
3. Let the dropdown insert the subject prefix, then append the approved title after it. Verify the subject contains the prefix once; do not replace the injected prefix or type a duplicate.
4. Insert the approved announcement, preview it, and check rendered BBCode, title, version, links, and attribution. Submit once and verify the resulting live topic and post.
5. Record successful creation as described below, and include the direct topic URL in the chat response.

## Update an existing topic

For the verified current-maintainer development topic:

1. Replace its first post with the latest approved complete announcement. Open the edit form from that post's own ID and check its author first: a moderator or team account can edit other members' posts, so a wrong post ID would overwrite someone else's text.
2. Post the approved update as a **new reply in that same topic**.
3. Verify both live results, including that the update's gallery images load, and provide their direct URLs in chat. Do not create a separate update topic.

If only one action succeeds, report it precisely. Check the live topic before retrying to avoid duplicate replies.

## Record successful topic creation

The user explicitly requested a persistent topic-creation memory to prevent duplicates. Record each topic actually created; never record a draft, intended topic, or reply as a newly created topic.

Record the topic using the agent's configured persistent-memory mechanism and its write rules. Do not write to another agent's memory or configuration, and do not guess a memory path. If no persistent memory is available, save the verified topic record alongside the project's release drafts (or in the task's outputs if that directory is unavailable), return the topic URL, and report that the memory write is pending.

Include:

- Project/extension and repository identity.
- Forum/site and purpose, such as current-maintainer development announcement.
- Exact live topic title and selected prefix.
- Direct canonical topic URL and topic ID when available.
- First-post URL/ID when available, for later announcement edits.
- Verified creation date, using MM/DD/YYYY for human-readable dates.

Always return the direct newly created topic URL in chat, even when the memory write succeeds. If recording fails, the topic still exists: report its URL and the recording failure, and do not create another topic.
