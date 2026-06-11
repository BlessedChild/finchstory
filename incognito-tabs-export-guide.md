# Chrome Incognito Tabs Bulk Export Guide

> Generated: 2026-06-11

---

## Q: Why export incognito tabs?

Incognito mode discards all tabs when closed — no auto-restore. If you have 200+ tabs open, export URLs before shutting down or you lose them all.

---

## Q: What method worked?

Chrome's native AppleScript API. `URL of tab t of window w` reads each tab's address directly, and this interface remains accessible in incognito mode.

---

## Q: What tools are involved?

- **osascript** — macOS built-in, runs AppleScript
- **Python 3** — data processing and HTTP requests
- **Local HTTP server** — collection and deduplication

---

## Q: Why not use a browser extension?

Chrome blocks extensions from reading incognito tab data by design. No workaround.

---

## Q: Why not simulate keystrokes (Cmd+L → Cmd+C)?

System Events keystroke simulation requires Accessibility permissions and is slow + unreliable for 200+ tabs.

---

## Q: Why not use the Accessibility API?

The low-level AX API requires the calling process to have Accessibility privileges. Finch's Python backend doesn't have it.

---

## Q: What's the full workflow?

1. AppleScript loops through all Chrome windows, checks `mode of window` for `"incognito"`, processes only incognito windows.
2. Reads URL + title for each tab, writes to a temp file.
3. Python reads the temp file, sends entries via curl to a local HTTP server with automatic dedup.

---

## Q: What does the core AppleScript look like?

```applescript
tell application "Google Chrome"
    repeat with w from 1 to count of windows
        if mode of window w is "incognito" then
            repeat with t from 1 to count of tabs of window w
                set tabUrl to URL of tab t of window w
                set tabTitle to title of tab t of window w
                -- write to file or send to server
            end repeat
        end if
    end repeat
end tell
```

---

## Q: What if a tab hangs?

AppleScript's `try` block catches exceptions. Hanging tabs are skipped without breaking the loop. This is why the per-tab `try` approach succeeds where a single bulk call times out.

---

## Q: How long did 353 tabs take?

About 10-20 seconds — an order of magnitude faster than clicking each bookmark manually.

---

## Q: Will this work in future Chrome versions?

Yes, as long as Chrome maintains its AppleScript dictionary. The API is stable.
