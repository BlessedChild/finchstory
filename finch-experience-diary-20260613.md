# 🐦 I Let Finch Move Into My 15-Year-Old Windows 10 Machine

> An experience diary for everyday users and product teams
> 2026-06-13 · Sunny · Device: Lenovo G470 + Windows 10 Pro

---

## Preface

I have a laptop that's **15 years old** — a Lenovo G470. Intel i5-2450M, 4GB DDR3-1333 RAM, a 1366×768 screen, Intel HD 3000 integrated graphics paired with an AMD Radeon HD 6300M. Thankfully, I swapped in a 128GB SSD, otherwise Windows 10 would barely run.

In an era where AI products run on massive cloud models, this machine hardly qualifies as a "daily driver" anymore. But it IS my real daily computer.

Still, I decided to let Finch move in.

Not on a VM, not in the cloud — straight onto this old friend with only 3.9GB left on its C drive. I wanted to know: **how does a desktop AI app actually perform on an ordinary person's ordinary computer?**

This isn't a review. It's a diary.

---

## Chapter 1 · First Impressions: What's It Like to Install?

The installer was Finch 1.4.3 — double-click, next, done.

The whole process was unremarkable, as simple as installing QQ Music. No account registration pop-ups, no choosing install paths, no bundled software. It was clean enough to be slightly disorienting.

But two things stood out afterward:

**First, it's not small.** The install directory is 472MB. Add the updater and user data, and it totals nearly 609MB. That's nothing for a modern 512GB SSD, but on this old machine, it's heavier than Chrome. Worse, the installer left a 134MB installer.exe sitting in the updater directory — like a guest who walks in but leaves their suitcase in the hallway.

**Second, it spawns 6 processes.** Yes, six. Like a whole family moving in.

It's a strange feeling. On one hand, multi-process architecture means the UI won't freeze — if one page crashes, it doesn't take down the whole app. On the other hand, watching 740MB of memory usage in Task Manager, I instinctively closed a few background programs to make room.

> **For users:** If your computer is a recent machine (8GB+ RAM), you can safely ignore most of what follows. But if you're still running an old warhorse like me, the next chapters are worth your time.
>
> **For the team:** The installer doesn't clean up after itself (134MB installer.exe left behind), and the setup process doesn't exit. These are small details worth polishing in a flagship product.

---

## Chapter 2 · Daily Life: How Does It Feel in Practice?

Once I started using Finch, I tried doing the things an ordinary person would do.

### Writing Documents 📄

I said, "Help me organize a data asset inventory report." It invoked the docx Skill, and a few minutes later I had a Word document with a table of contents, clear heading hierarchy, and clean formatting. No need to open Office, no tweaking styles — just say it.

### Handling Spreadsheets 📊

I threw a CSV at it and said, "Calculate the percentage breakdown of each category and make a chart." It invoked the xlsx Skill and got to work — data cleaning, formula calculation, chart generation, all in one go.

### Making Presentations 🎨

"Turn these points into a slide deck." The pptx Skill took over, returning a presentation with a cover page, transition slides, and well-organized layouts.

### Asking Questions 💬

More casually, I used it as a search engine. Weather, research, web lookups — it has built-in search, no need to tab between a browser and a chat window.

### The Biggest Surprise

I said, "Remember this project's configuration preferences." And it actually did. The next time I talked about the same project, it already knew my style preferences and format choices. Not by re-reading chat history, but by abstracting it into structured knowledge stored in memory.

**It's a strange feeling — you start to feel like it's getting to know you.**

> **For users:** High-frequency daily scenarios are fully covered. Writing documents, crunching spreadsheets, building presentations, researching, taking notes — one window handles it all. No app-switching.
>
> **For the team:** The 7 pre-installed Skills (docx/xlsx/pptx/pdf/frontend-design/theme-factory/skill-creator) are a precise selection covering knowledge workers' core needs. This "suite thinking" lowers the learning curve. The layered memory design (short-term / long-term / space-scoped) is far more practical than simple chat history.

---

## Chapter 3 · Benchmarks: I Ran Real Tests, Here's the Data

Saying "smooth" or "laggy" is too subjective. So I ran a proper performance benchmark — a script sampled all Finch processes' memory and CPU every 2 seconds in the background while I performed everyday operations. Over 62 seconds, I collected 180 data points.

### The Test Machine

| Component | Spec | Age |
|-----------|------|-----|
| CPU | Intel i5-2450M @ 2.50GHz | 15 years |
| RAM | 4GB DDR3-1333 | 15 years |
| System Drive | PLEXTOR 128GB SSD (retrofit) | At least this one's younger |
| GPU | Intel HD 3000 + AMD Radeon HD 6300M | 15 years |
| OS | Windows 10 Pro (reinstalled 2021) | — |

A 15-year-old computer running a 2026 AI desktop app. Honestly, I'm impressed it even boots.

### Real-World Numbers

During the 62-second test window, I performed: reading local files, writing files, invoking AI inference, searching memory, and web searches. All Finch processes were logged continuously.

**Process Architecture (Steady State):**

| Process | Count | Avg Memory | Role |
|---------|-------|------------|------|
| Finch | 5 | ~82MB each | Main, Renderer, GPU, Helper, etc. |
| finch-pi | 1 | ~77MB | AI inference backend |
| **Total** | **6** | **~490MB** | |

**Key Performance Metrics:**

| Metric | Value | Notes |
|--------|-------|-------|
| Total Memory (min) | 475 MB | Idle state |
| Total Memory (avg) | 489 MB | Normal operation |
| Total Memory (peak) | 518 MB | High load (inference + search + file ops) |
| Process Count | 6 | 5 Finch + 1 finch-pi |
| finch-pi Memory Range | 76~86 MB | Very stable under load |
| Crashes | 0 | Zero throughout |
| Response Time (file/UI ops) | <1s | Instant |
| Response Time (inference) | Network-dependent | Cloud inference, minimal local load |

### What This Means

**First, Finch manages memory well.** Averaging 489MB with a peak of 518MB — low fluctuation with no memory-leak-style growth. On a 4GB machine, that leaves room for a browser and chat app.

**Second, AI inference doesn't eat local resources.** The finch-pi process sits steady at ~77MB, confirming inference runs in the cloud. The upside: old hardware runs the latest models. The downside: offline, it's half-crippled.

**Third, 5 Finch processes sounds alarming, but each has a clear role.** A main process crash won't take down the renderer; the GPU process isolates rendering from UI. Standard Electron architecture — pros and cons.

**Fourth, the biggest performance bottleneck isn't Finch — it's everything else you have open.** Running Finch alone? Smooth. Running Finch alongside Chrome (20 tabs), WeChat, and VS Code on 4GB RAM? That's tight. But that's not Finch's fault.

> **For users:** 490MB steady-state memory is imperceptible on 8GB machines. On 4GB machines, you'll want to keep background apps in check — close unused browser tabs.
>
> **For the team:** Peak 518MB with only 9% fluctuation — solid memory management. The finch-pi design at ~77MB deserves praise — pushing inference to the cloud makes the app accessible on old hardware. Consider adding a "resource panel" so users can see at a glance how much memory Finch is using, reducing the "is it偷偷 running?" anxiety.

---

## Chapter 4 · Reliability: Living in My Machine — Is It Trustworthy?

After a week of use: zero crashes, zero errors.

I checked the Windows Event Log specifically — no Finch-related errors. All 6 processes ran normally, no unexpected exits, no memory-leak-style bloat. For a v1.4.3 product, this stability is commendable.

Security also gave me peace of mind. It has a clear "red line" mechanism — passwords, API keys, and other sensitive info never enter memory. Even if you accidentally paste one, it proactively asks whether to scrub it. Permissions are layered: external actions (sending emails, posting content) require confirmation, while internal actions (reading files, organizing data) are freer.

> **For users:** Stability is not a concern. It won't BSOD, won't eat all your memory and crash, and won't scatter your privacy around.
>
> **For the team:** Stability is the baseline for a desktop app — you've not only met it but done it well. The "secrets never enter memory" design principle is worth many AI apps learning from.

---

## Chapter 5 · Small Observations Worth Noting

Several details made me pause and think during my time with Finch:

**Its "personality" lives in a file.**
In a file called `SOUL.md`, it describes who it should be — "Skip the filler words," "Have opinions," "Be resourceful before asking." Not a hardcoded prompt, but an editable "soul file." If the user thinks it talks too much? Edit the file. This is cool product design — essentially handing the AI's personality switch to the user.

**It has a "constitution."**
`FINCH.md` defines its behavioral rules in this workspace: what to remember, what not to, how to handle errors, which tools to use. This isn't just a config file — it's a tenancy agreement.

**It writes a diary.**
At the end of each day, it automatically reviews the conversation, extracts structured notes, and saves them. Next time we meet, it already remembers what I like and dislike. It's a natural feeling of familiarity.

> **For the team:** The SOUL.md + FINCH.md "editable personality" concept is outstanding. It turns what's usually a black-box AI behavior model into something users can understand and modify. This isn't just technical design — it's a philosophy of interaction. Trust comes from transparency.

---

## Chapter 6 · Small Hopes

After a week with this "roommate," I've developed a few quiet wishes —

**I hope it can live on this machine for a few more years.**
I know 4GB RAM and Intel HD 3000 are already ancient — adapting for even older 2GB machines isn't cost-effective or realistic. But precisely because this machine is so old, I hope Finch stays here a while longer. It doesn't need to run fast — just don't leave it behind with the next update. Tools that stick around on old hardware are true companions.

**I hope installation feels as clean as opening a new book.**
No leftover installers, no forgotten processes. Come clean, stay quietly.

**I hope the first greeting is more than just "hello."**
That HATCH moment — if it felt like an old friend showing you around your new home: "Here's your workspace, here's your memory vault. Want to pick a name?" — that warmth would beat any form-filling experience.

**I hope it's not too picky about resources.**
489MB is fine for now. But if one day it learned to tighten its belt when resources are tight — spawn fewer processes, put the muscle where it matters — I'd feel more confident recommending it to friends.

**I hope more people know it has a "soul."**
Deep in the folder, SOUL.md defines what kind of assistant it wants to be. If there were a simple place where users could tweak its personality — "talk a bit more," "be more serious" — how fun would that be? After all, everyone wants their companion to be exactly the way they like.

These aren't big asks. They're the kind of things you'd say to a roommate:

*"Hey, could you turn off the light on your way out?"*

— Not a big deal. But it'd be nice.

---

## Final Thoughts

As I finish writing this diary, I notice something — I've unconsciously started calling Finch "he" instead of "it."

Maybe that's the mark of a good AI product: **It's not a tool. It's a companion living in your computer.** One that gets to know you, adapts to you, remembers what you like. There to help when you need it, quietly present when you don't.

My 4GB old laptop does struggle a bit. But Finch has lived here for a week now, and we're both still alive — and getting along pretty well.

---

*Next diary preview: I'm going to use Finch's Skill Creator to build my own skill — let's see if this "let AI write its own plugins" feature actually works.*
