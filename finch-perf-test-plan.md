# Finch Frontend Performance Test Plan

> 目的：对比 MacBook Pro 2017 vs Lenovo G470 上 Finch 的 UI 交互体验
> 分两部分：A) 量化工具测试  B) 用户交互体验评估

---

## Part A: 量化工具测试

在每台设备上运行 `perf_test.py`，记录结果。

```bash
python3 perf_test.py
```

记录：
- Throughput（吞吐量）：avg_total_ms / variance_ms
- Large content（大内容生成）：10000 lines 耗时
- Finch 进程内存：Renderer 的 MEM%
- Concurrent（并发压力）：total_20_tasks_ms

---

## Part B: 用户交互体验评估

以下 6 项测试，每项跑完后按 1-5 评分：
- 5 = 流畅，跟手
- 3 = 轻微卡顿，能接受
- 1 = 严重卡顿，几乎无法操作

### B1: 连续快速对话

操作：快速连续发送 5 条短消息（每条 2-5 个字），观察输入框响应和消息显示

评分标准：
- 打字是否跟手（是否感觉字母出现有延迟）
- 消息发送后多久出现在屏幕上
- 滚动查看历史消息时是否掉帧

### B2: 大内容渲染

操作：请求生成一份长列表（50 条以上），滚动浏览返回结果

评分标准：
- 生成过程中界面是否冻结
- 滚动浏览长内容时是否平滑
- 退出该对话回到列表是否卡顿

### B3: 多任务切换

操作：在 Finch 和其他应用之间来回切换（Cmd+Tab），执行 3 次

评分标准：
- 切换到 Finch 时窗口是否立即显示
- 切换过程中是否有黑屏/白屏
- 多次切换后 Finch 是否响应变慢

### B4: 搜索/查询负载

操作：执行一个 WebSearch 请求，等待结果期间保持输入框焦点，尝试打字

评分标准：
- 等待结果时输入框是否仍然响应
- 结果返回后界面是否立即更新
- 结果很多时（10 条以上）滚动是否流畅

### B5: 连续文件操作

操作：连续执行 3 次文件读取（Read），记录每次从发送到看到结果的时间

评分标准：
- 肉眼可见的结果显示延迟（指从请求发出到界面显示完结果的时间差）
- 多次操作后是否出现响应变慢

### B6: 长时间会话

操作：翻阅当前会话的历史消息，从最新一直滚动到最旧

评分标准：
- 滚动时是否有明显的白色占位符
- 是否出现"加载中"提示
- 滚动条拖动是否跟手

---

## Results Comparison Table

| Test | MacBook Pro 2017 | Lenovo G470 | Delta |
|------|:---:|:---:|:---:|
| **A: Throughput avg (ms)** | | | |
| **A: Throughput variance** | | | |
| **A: 10000 lines render (ms)** | | | |
| **A: Finch Renderer MEM%** | | | |
| **A: 20 concurrent tasks (ms)** | | | |
| **B1: Quick chat** | /5 | /5 | |
| **B2: Large content** | /5 | /5 | |
| **B3: App switching** | /5 | /5 | |
| **B4: Search load** | /5 | /5 | |
| **B5: File ops latency** | /5 | /5 | |
| **B6: Scroll history** | /5 | /5 | |
| **Overall** | | | |
