# macOS System Cleanup & Performance Optimization Guide

> Generated: 2026-06-11
> Tested on: MacBook Pro 2017 (Intel, 16GB)

---

## Q: My Mac is slow and feels bloated. What should I do?

Follow this order: **Cache → Unused apps → Startup items → Browser processes → Reboot**

This plan improves things without rebooting, but the final reboot is the most effective single step.

---

## 1. Cache Cleanup

### Q: Can I just delete user caches?

Mostly yes. Browser caches, package manager caches (Yarn/pip), and dev tool caches are all rebuildable.

### Q: Which caches take the most space?

Common culprits:

- **Google/Chrome cache** — 1-2 GB
- **VisualStudio cache** — 2 GB
- **Yarn / pip caches** — ~1 GB each
- **Browser caches (Edge/Firefox)** — ~500 MB each
- **WeChat dev tools / electron** — 200-500 MB each

### Q: How to clean?

Quit the app first, then remove directories under `~/Library/Caches/`:

```bash
rm -rf ~/Library/Caches/Google/
rm -rf ~/Library/Caches/VisualStudio/
rm -rf ~/Library/Caches/Yarn/
rm -rf ~/Library/Caches/pip/
```

For permission-locked files (e.g. electron cache), use `sudo rm -rf` or delete via Finder.

### Q: What were the real-world results?

**9.4 GB → 2.3 GB**, freeing ~7 GB.

---

## 2. Unused App Cleanup

### Q: How to decide what to remove?

Three criteria:

1. **Functional duplicates** (multiple browsers, multiple media players)
2. **Long unused** (dev tools, game platforms)
3. **Replaceable by Finch** (light document editing, basic git ops)

### Q: What can Finch replace?

| App | Alternative |
|-----|------------|
| GitHub Desktop | git CLI |
| The Unarchiver | command-line extraction |
| Light Office work | docx/xlsx/pptx skills |
| Xmind / StarUML / Effie | document-based alternatives |

### Q: Typical candidates for removal?

- **Duplicate browsers** (keep at most two)
- **Duplicate media players** (VLC / IINA — pick one)
- **Abandoned dev tools** (Unity / UE4 / Docker / Parallels)
- **Unused conferencing apps**
- **Office suites** (keep one: Office / iWork / LibreOffice)

---

## 3. Startup Item Cleanup

### Q: Where do I find startup items?

| Location | Description |
|----------|-------------|
| System Settings → General → Login Items | Apps that launch at login |
| `~/Library/LaunchAgents/` | User-level daemons |
| `/Library/LaunchAgents/` | System-level agents |
| `/Library/LaunchDaemons/` | System-level boot services |

### Q: Which startup items can be disabled?

- **Residual plists from already-deleted apps** (TeamViewer, conference apps)
- **Unnecessary auto-updaters** (OneDrive, Edge updates)
- **Unused background services** (Steam cleaner, Java updater)

### Q: How to remove them?

User-level:

```bash
rm ~/Library/LaunchAgents/com.xxx.plist
```

System-level (requires admin password):

```bash
sudo rm /Library/LaunchAgents/com.xxx.plist
```

Or with a GUI auth prompt:

```applescript
osascript -e 'do shell script "rm ..." with administrator privileges'
```

---

## 4. Browser Process Management

### Q: Why does Chrome eat so much RAM?

Each tab is a separate OS process. 200+ tabs = 200+ renderer processes, easily consuming 4-8 GB of RAM.

### Q: How to bulk-export incognito tabs?

Use Chrome's native AppleScript:

```applescript
tell application "Google Chrome"
    set tabUrl to URL of tab t of window w
    set tabTitle to title of tab t of window w
end tell
```

This works in incognito mode. See `incognito-tabs-export-guide.md` for details.

### Q: How to bulk-close incognito windows?

```applescript
tell application "Google Chrome"
    repeat with w in every window
        if mode of w contains "incognito" then close w
    end repeat
end tell
```

23 windows closed in 1-2 seconds. See `bulk-close-incognito-guide.md` for details.

---

## 5. The Final Boss

### Q: I did all of the above and it's still sluggish?

**Reboot.** 85 days of uptime accumulate swap bloat, memory fragmentation, and background process cruft that only a restart fully clears.

### Q: How often should I reboot?

At least once a month. If you run heavy dev tools, every 1-2 weeks is ideal.
