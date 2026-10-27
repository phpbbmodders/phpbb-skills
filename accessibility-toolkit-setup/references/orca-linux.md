# Isolated Linux Orca announcement checks

## Prepare an isolated runtime

Inspect the OS release and installed tools first. Typical requirements are Orca, Python GI/AT-SPI bindings, GTK, Xvfb, D-Bus, and a browser exposing accessibility. Check package candidates and dependencies with the host package manager. Existing speech-dispatcher and AT-SPI bindings can sometimes be reused even when the `orca` executable is absent.

Prefer the installed supported reader. When temporary extraction is appropriate, obtain the OS repository's actual package URI and expected size/hash through package-manager metadata, download that exact package with a finite timeout, verify its digest, and extract with `dpkg-deb -x` into a fresh temporary directory. Inspect its launcher and dependencies. Do not reuse a remembered URL/version/hash as a universal pin or install an arbitrary newer reader into an older OS.

An Ubuntu Jammy exercise used Orca 42.0 from the matching repository. That is an observed setup, not a recommendation or a substitute for a caller's pinned NVDA, JAWS, or VoiceOver references. Record the actual reader/browser versions and any reader exceptions.

## Launch a private session

Use `xvfb-run -a dbus-run-session -- ...` with isolated XDG config/data/cache/runtime directories and a private Orca preferences directory. Create directories with user-only permissions; use `--user-prefs` rather than the user's live Orca config. A pre-existing `DISPLAY` variable does not establish access to a display; probe it before treating it as usable. A private D-Bus session prevents test AT-SPI events from controlling the user's desktop. Do not run `orca --replace` against a host reader.

A general pattern, with paths replaced by the verified local locations:

```bash
xvfb-run -a dbus-run-session -- env \
  A11Y_ISOLATED_SESSION=1 \
  XDG_CONFIG_HOME="$test_root/config" \
  XDG_DATA_HOME="$test_root/data" \
  XDG_CACHE_HOME="$test_root/cache" \
  XDG_RUNTIME_DIR="$test_root/runtime" \
  NO_AT_BRIDGE=0 \
  /usr/bin/python3 scripts/orca_announcement_runner.py \
    --entrypoint "$orca_root/usr/bin/orca" \
    --module-dir "$orca_root/usr/lib/python3/dist-packages" \
    --prefs-dir "$test_root/preferences" \
    --debug-log "$test_root/announcements.log"
```

Run the browser test inside the **same** private display/D-Bus session. An orchestrator should start the reader as a child, launch a headed Chromium with `--force-renderer-accessibility`, execute the test, then terminate/wait for its reader in `finally`, escalating to a kill only for that owned child after a short grace period. Apply a finite outer timeout with a kill grace period so initialization cannot hang indefinitely. Do not kill processes by a broad `orca` or browser name.

The bundled runner disables only the audio backend. It also bypasses Orca's user-wide process-name single-instance check **only after requiring the isolated-session marker and display/D-Bus environment**; it does not call the launcher's cleanup/replace path. This is needed because that guard can reject a genuinely separate test session when a host reader is present. Never apply this override to the real desktop.

## Observe real reader output

Use Orca's debug `SPEECH OUTPUT:` entries to check actual generated announcements. Assert expected concepts using the application's actual localized strings, not an invented heading; for example, an export section may be named “Poll votes” rather than “Polls.” Verify names, roles, checked states, and expanded/collapsed transitions relevant to the change. Move focus and use the reader's supported navigation mode. Allow a bounded readiness interval instead of assuming immediate event delivery.

Announcement logging with the audio backend disabled verifies generated output only. It does not prove audio playback, intelligibility, human listening, or compatibility with another reader. Preserve logs privately: control names, document titles, and member-authored text may appear in them.

## Diagnose before declaring a limitation

Capture reader stderr and exit status as well as its debug log. Zero announcements can mean startup failure, the global single-instance guard, wrong D-Bus/display, missing browser accessibility, or an event backlog. AT-SPI tree checks alone do not repair or establish reader output. Old Orca/new browser combinations may throw generation errors; report their impact rather than silently suppressing them. Missing optional mouse-review support does not itself invalidate keyboard checks, but document the unavailable feature if relevant.

Clean up private sessions and owned child processes. Retain only the evidence needed for review; do not publish private logs or modify the user's screen-reader settings.
