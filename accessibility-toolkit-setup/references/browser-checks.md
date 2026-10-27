# Browser checks and contrast review

## Setup and evidence

Use an available Playwright installation and its matching browser. A project's virtual environment may already contain Playwright while Pillow or another inspection library exists only in the host interpreter. Verify interpreter/module paths before adding dependencies; avoid changing global Python paths. Prefer a subprocess or an explicitly supplied compatible module location when reusing a host package.

Keep axe-core in isolated storage when it is a test-only dependency. Verify the selected release, record the loaded version, and retain full violations and incomplete-rule details privately. Log only rule IDs and counts when content is sensitive. A successful audit process means the scan ran; inspect its findings separately.

Test the affected UI with keyboard activation and focus movement, plus normal and narrow viewports. Restore the original viewport before the next test; a narrow ACP layout may hide desktop tabs and produce misleading navigation failures. Save and restore any settings changed by a test in `finally` paths. Do not send email or enable outbound services as a side effect of imported-data tests.

After template changes, use the application's cache-purge operation. Check whether generated templates actually disappeared: an unprivileged purge may report success while leaving files owned by another user. Elevate only the scoped cache operation when authorized, rather than restarting shared services or deleting unrelated files.

## Contrast review

Inspect computed foreground, background, font size/weight, and ancestor backgrounds. Test normal, hover, focus, and active states where styles differ. Wait for transitions to settle.

For a simple opaque gradient, evaluate the least favorable background across the gradient, rather than just its base color. Checking stops alone is insufficient for arbitrary multicolor gradients; sample/interpolate the gradient or inspect rendered pixels when luminance may reach an interior extreme. For a repeated background image, examine its actual pixels and positioning. Resolve transparency by compositing with the real ancestor background before calculating contrast. Exclude borders and glyph antialiasing when sampling a text background.

Use the caller's pinned standard for applicable thresholds and exceptions. Decorative `aria-hidden` marks accompanied by equivalent text should be identified as such. For overlapping code blocks or legends flagged as obscured, verify the text's rendered background and that text remains visible; a computed color alone does not establish lack of occlusion.

`python3 scripts/contrast.py --foreground '#105289' --background '#d2d2d2'` computes one opaque color pair. Do not use this helper as a CSS renderer.

## Accessibility tree and standalone HTML

Query the affected nodes with CDP `DOM.querySelector` and `Accessibility.getPartialAXTree` with `fetchRelatives: false`. Avoid whole-document trees for large exports; they can overwhelm a test with thousands of unrelated records. Check actual roles, names, and states as well as the DOM attributes.

For private standalone exports, block HTTP(S) requests before opening the local document so linked images and other assets do not contact external sites. Test local anchors, missing-target behavior, unique IDs, language/direction, landmarks, headings, native disclosure keyboard behavior, tables, and meaningful image alternatives.

If a screen reader cannot process a large document promptly, distinguish an event backlog from missing semantics. A focused fixture may retain the exact exported section and styles while removing unrelated records; record that the focused section, rather than the entire document, was exercised with the reader.
