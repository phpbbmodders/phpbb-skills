# Report format

The posted report is **findings, then a recommendation** — nothing else. It is
BBCode, ready to be edited and posted to phpBB.com. No scope header, no
reference ledger, no surface table, no coverage matrix, no statistics. Those are
working artifacts; see *Coverage notes* at the end of this file for where they go
instead.

## BBCode, never Markdown

**Read `example-report.txt` in this directory before writing anything.** It is a
complete finished report in the exact syntax required, in a plain-text file with
no Markdown in it. Imitate that file. It is a far more reliable guide than the
rules below, because this file is itself Markdown and its formatting is not the
formatting you want.

The syntax mapping, written without backticks so there is nothing to copy wrongly:

    inline code, path, identifier, key    [c]...[/c]
    multi-line code block                 [code]...[/code]
    bold                                  [b]...[/b]
    italic                                [i]...[/i]
    link                                  [url=https://...]text[/url]
    colour                                [color=#RRGGBB]...[/color]
    horizontal rule                       [hr][/hr]

None of these characters may appear anywhere in the report: the backtick, the
asterisk, the underscore used for emphasis, the hash used as a heading, the pipe
used to draw a table, or the bracket-paren Markdown link form. The board renders
them literally as punctuation.

**Why this keeps going wrong.** You are writing into a chat that renders
Markdown, your default habit is Markdown, and these instructions are themselves
Markdown full of backticks. Every one of those pulls the report toward the wrong
syntax, hardest at the end of a long review. Four habits fix it:

1. **Re-read `example-report.txt` immediately before drafting.** Recency wins
   over rules; make the last formatting you saw be the right formatting.
2. **Deliver the whole report inside one fenced code block.** The fence is the
   delivery wrapper, not part of the report: it stops the client rendering the
   BBCode and lets the reviewer copy the exact text.
3. **No conversational preamble and no prose summary afterwards.** Slipping into
   chat voice is what drags the syntax back to Markdown.
4. **Scan before you send.** Search the drafted report for each forbidden
   character listed above. If you find even one, the report is wrong — rewrite
   the affected part before sending. A deliberate pass, not an intention.

## 1. Findings

Only files that have issues. Never list a clean file, and never add a "looks
good" section. Grouped by file, files in the same order as the inventory; within
a file, `[valdeny]` before `[valinfo]`, then by line number.

One self-contained block per finding — each names its own file, so it can be
quoted on its own:

```
[valdeny]
In [c]path/relative/to/extension/root.php[/c]:

[code]
<up to 3 lines of context>
<the problematic line>
<up to 3 lines of context>
[/code]

<What is wrong, why it matters, and what to do instead. For a security issue,
state the risk and the impact in one or two sentences. For a guideline violation,
quote the guideline text and wrap the quoted text in [url=<direct link>][/url].
Wrap any inline code, keys, or identifiers in [c][/c].>
[/valdeny]

[hr][/hr]
```

Use `[valinfo]` in place of `[valdeny]` for anything that does not block
approval.

Rules for the blocks:

- **Everything belonging to a finding goes inside its `[valdeny]`/`[valinfo]`
  tags** — the file reference first, then the `[code]` block, then the
  explanation. Nothing but `[hr][/hr]` appears between findings.
- The file reference is the first line inside the tags, in the form
  `In [c]relative/path/file.php[/c]:`, followed by a blank line.
- Escape HTML/Twig tags inside `[code]` so they render, and keep the original
  indentation and the file's formatting.
- Non-code findings (a missing file, an unused language key, a packaging problem)
  omit the `[code]` block; the tags then hold the file reference and prose
  describing the location, e.g. `In [c]language/en/info_acp_myextension.php[/c]
  the key [c]ACP_MYEXTENSION[/c] is defined but never used.` Where the finding is
  about the package as a whole rather than one file, the file reference may be
  omitted and the location described in the prose.
- Cite the line number in the prose when the `[code]` block alone is ambiguous.
- `[hr][/hr]` separates findings, including after the last one.

## 2. Formatting note (only if applicable)

If there are several non-blocking formatting or spacing issues, collapse them into
one closing note rather than a finding each:

```
[valinfo]
There are formatting improvements that could be made in a future release —
<brief description> — in: [c]file1[/c], [c]file2[/c], [c]file3[/c]. These do not
affect the validation outcome at this time.
[/valinfo]
```

## 3. Recommendation

Close with the colour-coded recommendation and a one-sentence justification:

```
[b]Recommendation:[/b] [color=#008000][b]Approve[/b][/color]
<one sentence: "no blocking issues found">
```

or

```
[b]Recommendation:[/b] [color=#FF0000][b]Deny[/b][/color]
<one sentence naming the blocking issue(s)>
```

Green `#008000` for Approve, red `#FF0000` for Deny. Exactly one of the two,
never uncoloured, never hedged — the verdict is one word.

If verification was incomplete — no local clone, or a reference that could not be
obtained — add one line saying so, so the reviewer knows which claims are
unconfirmed. Otherwise add nothing.

If there are no findings at all, the whole report is:

```
Validation passed with no findings.

[b]Recommendation:[/b] [color=#008000][b]Approve[/b][/color]
```

## Coverage notes — not part of the posted report

The reference ledger, the action surface table and the checklist coverage matrix
still have to be produced; they are what stops a review from quietly narrowing.
They are just not part of what gets posted to the author.

Output them **after** the report, outside its fenced block, under a plain heading
such as "Coverage notes (internal — not for posting)":

- the reference ledger from step 2, with each row's status and proof column
- the action surface table from checklist section S, every cell filled
- the **per-file ledger**: one row per file in the step-1 inventory, with the
  sections applied to it (from checklist section T) and its result. The count
  must reconcile with the inventory — `22 files inventoried / 22 examined`, and
  if those numbers differ, say which files were not examined and why:

  ```
  Files: 22 inventoried / 22 examined
  composer.json                      A,P        ok
  ext.php                            B,G        ok
  acp/main_info.php                  S,C,E      1 deny (E47a)
  acp/main_module.php                S,C,D,E,G  2 deny
  controller/main.php                S,C,D,G    1 deny
  migrations/release_1_0_0.php       B,D,G      1 info
  language/en/common.php             E,G        ok
  styles/.../myext_body.html         S,D,E,F    ok
  styles/.../images/icon.svg         P5,P6      ok (no script, no href)
  vendor/select2/select2.min.js      P4         not audited line-by-line
  README.md                          P8         1 info (version mismatch)
  ```

  A file with no applicable checks is recorded `n/a` with a reason, never omitted.
  This is the artifact that makes "every file was checked" verifiable instead of
  asserted.
- the **attribution list**: one line per `[valdeny]`, naming the validation-policy
  provision it rests on, quoted or closely paraphrased from the fetched text:

  ```
  Denial attribution
  acp/main_module.php CSRF    R2 — security: extensions must not introduce
                              vulnerabilities (CSRF on a state-changing action)
  acp/main_info.php text      R1 — localization: no hardcoded text
  controller/main.php SQLi    R2 — security: SQL injection
  ```

  A denial with no attributable provision must not be in the report at all — it
  is downgraded or dropped before writing. If the checklist called for a denial
  the policy does not support, say so here as a checklist bug for the team.
- the coverage matrix: every checklist item id with `ok` / `info` / `deny` / `na`
  / `unverified`
- the core symbol resolution count, `N/M`, and the clone path and short sha

These are for the team member reviewing your work. They may be terse, and they
may use plain text rather than BBCode. The exit gate in the skill still requires
all of them to be complete before the report is written — moving them out of the
report does not make them optional.
