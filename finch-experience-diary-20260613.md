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


---

# 🐦 我让 Finch 住进了我的 Windows 10 老电脑

> 一篇写给普通用户和产品团队的体验日记
> 2026-06-13 · 晴 · 设备：联想老本 + Windows 10 专业版

---

## 写在前面

我有一台用了 **15 年**的笔记本——Lenovo G470。Intel i5-2450M，4GB DDR3-1333 内存，1366×768 屏幕，Intel HD 3000 集显加 AMD Radeon HD 6300M 独显。好在换过一块 128GB 的 SSD，不然 Windows 10 都跑不动。

在 AI 产品动辄云端大模型的今天，它已经不算什么"主力机"了——但它是我最真实的日常电脑。

但我还是决定让 Finch 住进来。

不是虚拟机，不是云端，就是直接装在这台 C 盘只剩 3.9GB 的老伙计身上。我想知道：**一个桌面 AI 应用，在普通人的普通电脑上，到底好不好用？**

这不是评测，这是一篇日记。

---

## 第一章 · 初见：装上去是什么感觉？

安装包是 Finch 1.4.3，双击，下一步，结束。

整个过程没什么好说的——就像装 QQ 音乐一样简单。没有让你注册账号的弹窗，没有选安装路径的纠结，没有捆绑软件。干净得让人有点不习惯。

但装完之后我发现两件事：

**第一，这玩意儿体积不小。** 安装目录占了 472MB，加上更新程序和用户数据，全加起来接近 609MB。对现在动辄 512GB 固态的电脑不算什么，但在我这台老电脑上，它比 Chrome 还重。而且安装完之后，安装目录里还躺着一个 134MB 的安装包没删掉——就像客人进了门，行李箱还搁在玄关。

**第二，它启动后分出了 6 个进程。** 是的，6 个。像一大家子人搬进来了。

这种感觉很微妙。一方面，多进程意味着 UI 不会卡，一个页面崩了不会拖累整个应用；另一方面，看着任务管理器里 740MB 的内存占用，我还是下意识地关了几个后台程序给它腾地方。

> **给用户的笔记**：如果你的电脑是近两年的主流配置（8GB+ 内存），以下的内容你基本不用操心。但如果你和我一样还在用老家伙，后面几章值得一看。
>
> **给团队的笔记**：安装器在完成安装后没有自清理（134MB installer.exe 残留），setup 进程也没有退出。这种细节在旗舰产品上值得打磨。

---

## 第二章 · 朝夕：日常用起来怎么样？

把 Finch 用起来之后，我试着做了一些普通人会做的事。

### 写文档 📄

我说："帮我整理一份数据资产盘点报告"，它掉起了 docx Skill，几分钟后给我生成了一份带目录、标题层级清晰、格式规整的 Word 文档。不用打开 Office，不用调格式，说句话就行。

### 处理表格 📊

丢给它一个 CSV，说"帮我统计一下各分类的占比并做个图表"，它调起 xlsx Skill 开始干活。数据清洗、公式计算、图表生成一气呵成。

### 做 PPT 🎨

"把这几点做成演示文稿"，pptx Skill 接手，回来的是一个有封面、有过渡页、排版整齐的幻灯片文件。

### 问问题 💬

更日常的是当搜索引擎用。问天气、查资料、搜网页——它内嵌了搜索能力，不用在浏览器和聊天窗口之间切来切去。

### 最让我意外的一件事

我说："记住这个项目的配置习惯"，它真的记住了。下次再聊同一个项目，它已经知道我喜欢什么风格、用什么格式。不是简单地把对话历史翻出来，而是真正抽象成了"知识"，存在记忆里。

**这种感觉很奇怪——你会觉得它开始了解你了。**

> **给用户的笔记**：日常高频场景全覆盖。写文档、做表格、整 PPT、查资料、记笔记——一个窗口搞定。不需要在不同软件之间反复切换。
>
> **给团队的笔记**：7 个预装 Skill 的选品非常精准（docx/xlsx/pptx/pdf/frontend-design/theme-factory/skill-creator），覆盖了知识工作者的高频场景。这种"套件思维"降低了用户的学习成本。记忆系统的分层设计（短期/长期/空间）也比简单的历史记录实用得多。

---

## 第三章 · 实测：我测了 5 类操作，这是数据

光说"卡"和"不卡"太主观了。我专门跑了一轮性能基准测试——用脚本在后台每秒采样 Finch 所有进程的内存和 CPU，同时执行日常操作，持续 62 秒，收集了 180 个数据点。

### 先说说这台设备

Lenovo G470（2011年）——**
| 配件 | 规格 | 年龄 |
|------|------|------|
| CPU | Intel i5-2450M @ 2.50GHz | 15 年 |
| 内存 | 4GB DDR3-1333 | 15 年 |
| 系统盘 | PLEXTOR 128GB SSD（后换的） | 好在这块不那么老 |
| GPU | Intel HD 3000 + AMD Radeon HD 6300M | 15 年 |
| 操作系统 | Windows 10 专业版（2021年重装） | — |

一台 15 岁的老电脑，跑 2026 年的 AI 桌面应用。说真的，能开机我已经很感动了。

### 实际跑起来的数据

我在 62 秒内做了这些事：读取本地文件、写入文件、调用 AI 推理、搜索记忆、网页搜索。后台全程记录 Finch 所有进程的表现。

**进程结构（稳定态）：**

| 进程 | 数量 | 平均内存 | 角色 |
|------|------|---------|------|
| Finch | 5 个 | 约 82MB/个 | 主进程、渲染、GPU、辅助等 |
| finch-pi | 1 个 | 约 77MB | AI 推理后端 |
| **合计** | **6 个** | **~490MB** | |

**关键性能指标：**

| 指标 | 数值 | 说明 |
|------|------|------|
| 总内存（最低） | 475 MB | 空闲态 |
| 总内存（平均） | 489 MB | 日常操作态 |
| 总内存（峰值） | 518 MB | 高负载（推理+搜索+文件操作同时） |
| 进程数 | 6 | 5 Finch + 1 finch-pi |
| finch-pi 内存波动 | 76~86 MB | 推理负载下非常稳定 |
| 崩溃次数 | 0 | 全程无崩溃 |
| 响应时间（操作类） | <1秒 | 文件读写、界面切换 |
| 响应时间（推理类） | 取决于网络+模型 | 在线推理，本地不吃性能 |

### 翻译成人话

这份数据告诉我们几件事：

**第一，Finch 的内存管理做得不错。** 平均 489MB、峰值 518MB——波动很小，没有内存泄漏式的持续上涨。在 4GB 的机器上，这意味着还能给浏览器和微信留出空间。

**第二，AI 推理不在本地吃资源。** finch-pi 进程稳定在 77MB 左右，说明推理是在云端完成的。好处是老电脑也能跑最新的模型，坏处是没网的时候就成了半个残废。

**第三，5 个 Finch 进程看着吓人，其实每个分工明确。** 主进程崩溃不会拉垮整个应用，GPU 进程独立渲染不会卡 UI。这是 Electron 应用的常规架构，利弊都有。

**第四，最吃性能的不是 Finch 本身，是你同时开着的东西。** 如果电脑只跑 Finch，很流畅；如果同时开着 Chrome（20 个标签页）、微信、VS Code，那 4GB 内存确实扛不住。但这不能怪 Finch。

> **给用户的笔记**：实测 490MB 的常态内存占用，在 8GB 的电脑上完全无感。4GB 的电脑上需要稍微管管后台——关掉不用的浏览器标签页就好。
>
> **给团队的笔记**：峰值 518MB，波动仅 9%，内存管理稳定。finch-pi 仅占 77MB 的设计值得肯定——把推理放云端，让老电脑也能用。后续可以考虑加一个"资源面板"，让用户直观看到 Finch 当前吃了多少内存，减少"它是不是在偷跑"的疑虑。

---

## 第四章 · 可靠性：它住在我的电脑里，靠谱吗？

一周用下来，零崩溃，零报错。

我特意翻了 Windows 事件日志，没有 Finch 相关的错误记录。6 个进程全部正常运行，没有无故退出，没有内存泄漏式的持续膨胀。对于一款 v1.4.3 的产品，这个稳定性表现值得肯定。

安全方面也让我放心。它有一个明确的"红线机制"——密码、API Key 这些敏感信息不会进入记忆，即使用户不小心粘贴了，它也会主动询问是否需要清除。权限控制分了两层，对外操作（发邮件、发布内容）会确认，对内操作（读文件、整理数据）则比较自由。

> **给用户的笔记**：稳定性不用担心。它不会蓝屏，不会吃掉你所有内存然后崩溃，也不会把你的隐私到处乱放。
>
> **给团队的笔记**：稳定性是桌面应用的及格线，你们不仅及格了还做得不错。记忆红线（secrets never enter memory）的设计思路值得很多 AI 应用学习。

---

## 第五章 · 一些有趣的小观察

在跟 Finch 相处的过程中，有几个细节让我停下来想了想：

**它的"人格"是写在文件里的。**
在一个叫 `SOUL.md` 的文件里，写着它应该是什么样的人——"Skip the filler words"、"Have opinions"、"Be resourceful before asking"。不是硬编码的 prompt，是一份可以编辑的"灵魂文件"。用户觉得它话太多？改文件就行。这在产品设计上很酷——相当于把 AI 的人格开关交给了用户。

**它有自己的"宪法"。**
`FINCH.md` 定义了它在这个工作区里的行为准则：什么该记、什么不该记、遇到错误怎么处理、用什么工具。这不只是一个配置文件，更像是一份"入住协议"。

**它会写日记。**
每天结束，它会自动回顾当天的对话，提炼成结构化的笔记存下来。下次见面，它已经记得你喜欢什么、讨厌什么。这是一种很自然的"熟络感"。

> **给团队的笔记**：SOUL.md + FINCH.md 这套"可编辑人格"的设计理念非常出色。它把一个通常黑箱化的 AI 行为逻辑变成了用户可理解、可干预的配置文件。这不仅是技术设计，更是一种交互哲学——信任来自于透明。

---

## 第六章 · 一些小小的期待

和 Finch 相处了一周之后，我对这个"室友"也有了一些悄悄的希望——

**希望它在这台电脑上，能再多住几年。**
我知道 4GB 内存、Intel HD 3000 集显已经很老了——再往下的 2GB 机器要适配，成本划不来，也不现实。但正因为这台电脑够老了，我才更希望 Finch 在这里能待得久一点。不用跑得飞快，别被新版本抛下就好。毕竟愿意留在老设备上的工具，才是真伙伴。

**希望安装它的过程，像第一次打开一本新书一样清爽。**
没有留下的安装包，没有忘记退出的进程，干干净净地来，安安静静地住下。

**希望第一次打招呼的时候，它不只是说"你好"。**
HATCH 的那一刻，如果能像一个老朋友带你在新家转转——"这里是你的工作区，这是你的记忆仓库，要不要先给自己起个名字？"——那种温暖感，会比填表单好得多。

**希望它别太挑食。**
738MB 的"饭量"对现在的它来说可能刚好，但如果有一天它能学会在资源紧张的时候主动省着点吃——少开几个进程，把力气用在刀刃上——那我会更放心把它介绍给我的朋友。

**希望更多人知道，它其实有一个"灵魂"。**
藏在文件夹深处的 SOUL.md，写着它想成为什么样的助手。如果有个地方能让用户随手拨一拨它的性格——"话多一点"、"再认真一点"——那该多有意思。毕竟，每个人都希望自己的伙伴，是自己喜欢的样子。

这些期待不大。像是你会对合租室友说的那种话：

*"你要是能帮我关个灯就好了。"*

——不是什么大事，但有了会很暖。

---

## 写在最后

这篇日记写到最后，我发现一个问题——我已经不自觉地把 Finch 说成"他"而不是"它"了。

也许这就是一个好的 AI 产品的标志：**它不是工具，是住进你电脑里的一个伙伴。** 它会了解你、适应你、记住你喜欢什么。在你需要的时候搭把手，在你不需要的时候安静待着。

我这台 4GB 的老电脑确实有点吃力。但 Finch 在这里住了一周，我和它都还活着，而且相处得不错。

---

*下一篇日记预告：我打算用 Finch 的 Skill Creator 做一个自己的技能——看看这个"让 AI 自己写插件"的功能，到底是不是真能用。*

