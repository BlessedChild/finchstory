# Finch Frontend Performance Test · MacBook Pro 2017

> Date: 2026-06-14  
> Device: MacBook Pro 2017 · 16GB RAM · i7-7920HQ · macOS  
> Finch v1.4.3

---

## Overview

This document contains the full frontend performance test methodology, the test script, and the results from the MacBook Pro 2017. It is designed to be replicated on other devices for comparison.

The test is split into two parts:
- **Part A**: Quantitative benchmark (automated via `perf_test.py`)
- **Part B**: User experience rating (manual, scored 1-5)

---

## Part A: Quantitative Benchmark

### Test Script

Save the following as `perf_test.py` and run it:

```bash
python3 perf_test.py
```

```python
#!/usr/bin/env python3
"""Finch frontend performance test - quantitative toolchain benchmark"""
import subprocess, time, json, os, sys, tempfile

results = {}

# Test 1: Rapid-fire throughput
print("=== Test 1: Rapid-fire throughput ===")
times = []
for i in range(10):
    start = time.time()
    open('/dev/null', 'w').write(str(i))
    mid = time.time()
    # Read a sample config file
    sample = os.path.expanduser('~/finchnest/FINCH.md')
    if os.path.exists(sample):
        with open(sample, 'r') as f:
            _ = f.read(1024)
    else:
        # fallback: read self
        with open(__file__, 'r') as f:
            _ = f.read(1024)
    end = time.time()
    times.append({'write': round((mid-start)*1000, 1), 'read': round((end-mid)*1000, 1), 'total': round((end-start)*1000, 1)})

avg_total = sum(t['total'] for t in times) / len(times)
variance = sum((t['total'] - avg_total)**2 for t in times) / len(times)
results['throughput'] = {
    'avg_write_ms': sum(t['write'] for t in times) / len(times),
    'avg_read_ms': sum(t['read'] for t in times) / len(times),
    'avg_total_ms': avg_total,
    'variance_ms': variance,
    'max_ms': max(t['total'] for t in times),
    'min_ms': min(t['total'] for t in times)
}
print(f"  Avg: {avg_total:.1f}ms, Variance: {variance:.1f}, Range: {results['throughput']['min_ms']}ms-{results['throughput']['max_ms']}ms")

# Test 2: Large content generation
print("\n=== Test 2: Large content generation ===")
for size in [100, 1000, 10000]:
    start = time.time()
    content = '\n'.join([f'line {i}: ' + 'x' * 50 for i in range(size)])
    with open('/dev/null', 'w') as f:
        f.write(content)
    elapsed = (time.time() - start) * 1000
    results[f'render_{size}'] = elapsed
    print(f"  {size} lines: {elapsed:.1f}ms")

# Test 3: System resource sampling
print("\n=== Test 3: System resource sampling ===")
try:
    ps_out = subprocess.run(['ps', '-eo', 'pid,%mem,rss,comm'], capture_output=True, text=True).stdout
    app_lines = [l for l in ps_out.split('\n') if 'Finch' in l and 'Renderer' in l]
    app_mem = []
    for l in app_lines[:5]:
        parts = l.split()
        if len(parts) >= 3:
            try:
                app_mem.append({'pid': parts[0], 'mem_pct': parts[1], 'rss_kb': int(parts[2])})
            except: pass
    results['app_memory'] = app_mem
    for m in app_mem:
        print(f"  PID {m['pid']}: {m['mem_pct']}% mem ({m['rss_kb']//1024}MB)")
except: pass

# Test 4: Concurrent pressure
print("\n=== Test 4: Concurrent pressure ===")
import threading
lock = threading.Lock()
concurrent_times = []

def write_task(idx):
    start = time.time()
    with open('/dev/null', 'w') as f:
        f.write('x' * 10000)
    elapsed = (time.time() - start) * 1000
    with lock:
        concurrent_times.append(elapsed)

threads = [threading.Thread(target=write_task, args=(i,)) for i in range(20)]
start = time.time()
for t in threads: t.start()
for t in threads: t.join()
total = (time.time() - start) * 1000

avg_concurrent = sum(concurrent_times) / len(concurrent_times)
results['concurrent'] = {'total_20_tasks_ms': total, 'avg_per_task_ms': avg_concurrent}
print(f"  20 concurrent tasks: {total:.1f}ms total, {avg_concurrent:.1f}ms avg each")

# Save results (sanitized - no hostname)
output = {'platform': sys.platform, 'python': sys.version, 'results': results}
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'perf-results.json')
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n✅ Results saved to {out_path}")
print(json.dumps(results, indent=2))
```

### MacBook Pro 2017 Results

| Test | Result |
|------|--------|
| Throughput avg (ms) | 0.24 |
| Throughput variance | 0.03 |
| 10000 lines render (ms) | 6.6 |
| Finch Renderer MEM% | 34.8% (5.7GB) |
| 20 concurrent tasks (ms) | 4.0 |

---

## Part B: User Experience Rating

### Test Methodology

Rate each test on a 1-5 scale:
- **5** — Smooth, responsive
- **3** — Slight lag, acceptable
- **1** — Severe lag, nearly unusable

#### B1: Quick Chat

1. Send 5 short messages in rapid succession (2-5 chars each)
2. Observe: typing responsiveness, message display delay, scroll smoothness

#### B2: Large Content Rendering

1. Request a long list (50+ items)
2. Observe: freeze during generation, scroll smoothness, conversation list transition

#### B3: App Switching

1. Switch between Finch and another app (Cmd+Tab), repeat 3 times
2. Observe: window display speed, blank frames, performance degradation

#### B4: Any Task Execution

1. Execute any task (search, file read, etc.) while keeping input focused
2. Observe: input responsiveness during task, result display speed, scroll smoothness
3. **Note**: This test applies to ANY task, not just search

#### B5: Consecutive File Operations

1. Execute 3 file reads in succession
2. Observe: perceived delay from request to result display

#### B6: Scroll History

1. Scroll through current session from bottom to top
2. Observe: blank placeholders, loading indicators, scroll bar responsiveness

### MacBook Pro 2017 Results

| # | Test | Score | Notes |
|---|------|:-----:|-------|
| B1 | Quick chat | 2-3 | Click-to-focus lag (seconds), message delay <1s, scrolling stutters |
| B2 | Large content rendering | 2 | No freeze during generation, scrolling is not smooth |
| B3 | App switching (Cmd+Tab) | 5 | Instant switch, no blank frames, no degradation |
| B4 | Any task execution | 1 | Input freezes or responds very slowly during ANY task. Scrolling stutters. Most impactful issue. |
| B5 | Consecutive file operations | 4 | ~0.5s perceived delay per operation |
| B6 | Scroll conversation history | 3 | No blank placeholders, scroll slightly stutters |

---

## Summary

| Metric | Score |
|--------|:-----:|
| Average UX score | **2.8 / 5** |
| Best | B3 (App switching: 5/5) |
| Worst | B4 (Any task: 1/5) |
| Bottleneck identified | Finch Renderer process memory (5.7GB, 34.8% of 16GB) |

### Key Finding

The toolchain itself is fast (0.24ms avg throughput, 6.6ms for 10K lines). The UI lag is caused by the Electron renderer process consuming excessive memory (5.7GB). This impacts input responsiveness, scrolling smoothness, and concurrent task handling — but does NOT affect app switching or basic file operations.

---

## Device Comparison Table

| Test | MacBook Pro 2017 | Lenovo G470 | Delta |
|------|:---:|:---:|:---:|
| **A: Throughput avg (ms)** | 0.24 | | |
| **A: Throughput variance** | 0.03 | | |
| **A: 10000 lines render (ms)** | 6.6 | | |
| **A: Finch Renderer MEM%** | 34.8% (5.7GB) | | |
| **A: 20 concurrent tasks (ms)** | 4.0 | | |
| **B1: Quick chat** | 2-3/5 | /5 | |
| **B2: Large content** | 2/5 | /5 | |
| **B3: App switching** | 5/5 | /5 | |
| **B4: Any task execution** | 1/5 | /5 | |
| **B5: File ops latency** | 4/5 | /5 | |
| **B6: Scroll history** | 3/5 | /5 | |
| **Overall** | **2.8/5** | **/5** | |
