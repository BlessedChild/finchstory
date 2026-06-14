# Finch Frontend Performance Test · MacBook Pro 2017

> Date: 2026-06-14
> Device: MacBook Pro 2017 · 16GB RAM · i7-7920HQ · macOS
> Finch v1.4.3

---

## Part A: Quantitative Benchmark

| Test | Result |
|------|--------|
| Throughput avg (ms) | 0.24 |
| Throughput variance | 0.03 |
| 10000 lines render (ms) | 6.6 |
| Finch Renderer MEM% | 34.8% (5.7GB) |
| 20 concurrent tasks (ms) | 4.0 |

## Part B: User Experience Rating (1-5)

| # | Test | Score | Notes |
|---|------|:-----:|-------|
| B1 | Quick chat | 2-3 | Click-to-focus lag (seconds), message delay <1s, scrolling stutters |
| B2 | Large content rendering | 2 | No freeze during generation, scrolling is not smooth |
| B3 | App switching (Cmd+Tab) | 5 | Instant switch, no blank frames, no degradation |
| B4 | Search / query load | 1 | Input almost unusable during search, scrolling stutters |
| B5 | Consecutive file operations | 4 | ~0.5s perceived delay per operation |
| B6 | Scroll conversation history | 3 | No blank placeholders, scroll slightly stutters |

## Summary

| Metric | Score |
|--------|:-----:|
| Average UX score | **2.8 / 5** |
| Best | B3 (App switching: 5/5) |
| Worst | B4 (Search load: 1/5) |
| Bottleneck identified | Finch Renderer process memory (5.7GB, 34.8%) |

### Key Finding

The toolchain itself is fast (0.24ms avg). The UI lag is caused by the Electron renderer process consuming 5.7GB of memory, which impacts:
- Input responsiveness
- Scrolling smoothness
- Concurrent task handling
