# Chrome Incognito Window Bulk Close Guide

> Generated: 2026-06-11

---

## Q: Why close incognito windows in bulk?

Dozens of windows with hundreds of tabs slow Chrome to a crawl — the tab bar collapses and clicking each one individually takes forever.

---

## Q: What method worked?

Chrome's native AppleScript API. Iterates through all windows, checks for `mode` == `"incognito"`, and closes matching ones.

---

## Q: What's the workflow?

1. Get all windows: `every window`
2. Check each: `mode of w as text` contains `"incognito"`
3. Close if match: `close w saving no`

---

## Q: What does the code look like?

```applescript
tell application "Google Chrome"
    set winList to every window
    repeat with w in winList
        set wm to mode of w as text
        if wm starts with "incognito" then
            close w saving no
        end if
    end repeat
end tell
```

---

## Q: `repeat with w in winList` vs `repeat with i from count down to 1`?

Both work. `in winList` is cleaner; `from count down to 1` is safer (closing windows won't shift indices). Both pass real-world testing.

---

## Q: Can it accidentally close normal windows?

No. The check explicitly targets `mode` == `"incognito"`. Normal windows have `mode` == `"normal"` and are skipped.

---

## Q: Should I save anything before closing?

Incognito tabs are gone forever once closed. Export URLs first if needed (see the incognito export guide). The `saving no` flag skips session persistence.

---

## Q: How fast was it for 23 windows?

1-2 seconds. Orders of magnitude faster than clicking each one manually.

---

## Q: Will this work in future Chrome versions?

Yes. As long as Chrome keeps the `mode` property and `close` command, this script works. Save it as a `.app` in Script Editor.app for one-click reuse.
