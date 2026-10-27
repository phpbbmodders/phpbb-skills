---
name: phpbb-extension-screenshots
description: "Capture phpBB extension board and ACP screenshots with the committed screenshot tooling and produce sized README previews plus a full gallery. Use when adding or refreshing extension screenshots, a README screenshot section, a screenshot gallery, or a dated update-post gallery."
---

# phpBB Extension Screenshots

Inspect the extension's actual feature pages and existing documentation. In this workspace use `phpbb-release-tools/phpbb-test-board/screenshots.py` under the shared repos directory; inspect its help, `SHOTS` mapping, and nearest relevant entry. Use the standard seed-forum fixtures for realistic forum/topic data.

Check a free port and the board/ref/mount before capture. The tool can reset its own disposable board: do not point it at a persistent board or assume it captures an existing board unchanged. Follow the test-board workflow for mount, cache, and cleanup safety.

Extend the committed screenshot scenario for reproducible new scenes. Capture board and ACP states needed to explain the feature. Use full-page ACP captures so lower controls are included. For transient states, automate the action and wait for the actual state selector before capturing; use controlled browser stubs only when they simulate the intended interaction and disclose their limits.

Save original full-size files in `docs/images/screenshots/`. Inspect every image for the right feature/version, crop, missing controls, misleading state, and private content. Keep three or four representative linked previews in the main README and the rest with captions in `docs/images/screenshots/README.md`, linked from the README. Use linked HTML `img` tags with explicit width and height preserving the aspect ratio; do not resize the original files to control display size.

For phpBB release-update posts, create a separate `docs/update/YYYY-MM-DD/README.md` gallery with two or three screenshots of recent changes, using the date of the update being prepared. Follow `docs/forum-update-posts.md` in [phpbb-release-tools](https://github.com/phpbbmodders/phpbb-release-tools). Prepare the dated README, images and BBCode draft together; the update post links to this README and uses these images. A link to the full README screenshot gallery does not replace the dated gallery. Keep the announcement's full-gallery link separate. This established `docs/update/` layout overrides the general image-location preference for update galleries. Preserve full-resolution images, add captions and linked HTML previews with proportional width/height (normally 640 pixels wide), and verify all image and post links. Exclude `docs/update/` from extension ZIPs with `export-ignore`; include the README in any separate screenshot archive. Avoid duplicate copies unless the established dated snapshot requires them.

Before touching a GitHub Wiki, verify it has a manually created first page. If uninitialized, stop Wiki work and give the user its URL to initialize; do not try alternate creation methods. A repository gallery can proceed independently.

Check all expected images exist, inspect rendered previews/links, respect packaging export-ignore rules, and run relevant changed-tool checks. Screenshot success proves only the pictured states, not a full accessibility or compatibility audit.
