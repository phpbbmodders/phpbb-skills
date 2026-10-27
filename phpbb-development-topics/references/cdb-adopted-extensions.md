# CDB responses for adopted extensions

Use this sub-workflow when responding to a phpBB Customisation Database discussion/support request about an adopted extension, and a current development announcement is part of the requested response. Read the parent skill's topic lookup, approval, prefix, and recording requirements as well.

## Establish the two destinations

Read the original CDB topic and identify the actual poster/request, extension, repository, current maintainers, and verified development release. Identify the actual current maintainers and describe the adoption accurately; do not mislabel a transferred-maintenance project as a fork. Do not imply that a development build is a phpBB-validated release or update the CDB download listing merely because a development release exists.

Search topic-creation memory and the development forum as the parent skill specifies. Distinguish:

- The original CDB discussion/support topic, where the answer belongs.
- The current-maintainer Extensions in Development topic, which holds the announcement and later development updates.
- The previous maintainer's historical development topic, which must not be revived or edited as a substitute when the user requires a separate current-maintainer topic.

If a verified current-maintainer development topic already exists, reuse it. If lookup remains inconclusive, resolve that before creating a duplicate. Absence from memory alone is insufficient.

## Prepare the linked drafts

When no current-maintainer development topic exists:

1. Prepare the usual announcement and update `.bbcode.txt` files in the repository's canonical release-drafts directory. The announcement is the complete first post for the new maintainers' development topic. The update file remains available for later release-update replies; do not post a redundant update reply just to initialize a new topic.
2. Prepare the answer to the original CDB poster as a separate reply draft in that directory. Keep it focused on the requested change and the verified release; link to the development topic once its real URL is known. Do not replace either canonical announcement/update file with the CDB answer.
3. Preserve the requested scope: discussion stays discussion; preparing drafts or publishing a release does not authorize creating a topic or sending the CDB reply. Follow the user's exact-text approval rules for each public message. Batch review where practical, but an unknown future topic URL is not a verified link and must not be published as a placeholder.

## Publish in dependency order when authorized

Create and verify the new current-maintainer development topic first if the approved CDB answer is meant to link to it. In the new-topic form, select the **[3.3][DEV]** Topic prefix dropdown first, then append the approved subject after the injected prefix, as described in the parent skill.

Record the new development topic in topic-creation memory and return its direct URL in chat immediately. Put that verified URL in the CDB reply draft; obtain any still-required approval for the final public text. Then post the approved answer as a new reply in the original CDB topic, verify the live text and links, and provide its direct post URL in chat.

If topic creation or approval is pending, keep the dependent CDB answer as a draft. Do not claim a topic exists, post an unapproved topic, or revive the old maintainer's topic to work around the dependency. An independently authorized support answer that does not rely on a new development-topic link can still proceed within its own approved scope.

Record the development topic as a newly created topic only after verified creation. The CDB answer is a reply to an existing topic: record its permalink with the draft/status evidence, not as another newly created development topic.

## Future development releases

The forum announcement is the development topic's first post. It is not a separate announcement topic, and a release does not require another topic.

Use the recorded current-maintainer development topic: replace its first post with the latest approved announcement and add the approved update as a new reply in the same topic. Do not create another topic for a version update. Add another CDB reply only when the user's requested response or follow-up calls for one; do not automatically cross-post every release to old support discussions.

## Completion links in chat

After publishing the linked development topic and CDB answer, always include both verified direct links in the final chat response:

- **Development topic:** its canonical topic URL.
- **CDB reply:** the exact posted reply permalink, including its post ID/anchor when available, rather than only the CDB contribution page or topic root.

This also applies when editing an existing approved CDB reply to add the development-topic link: verify the edit and return that reply's permalink. If either action is pending or failed, report the actual status and include only links to verified existing results. Never invent a future URL or imply a draft was posted.
