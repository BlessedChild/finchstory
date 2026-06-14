#!/usr/bin/env python3
"""Finch 前端性能测试 - 量化工具侧性能"""
import subprocess, time, json, os, sys

results = {}

# Test 1: 连续快速请求 - 测量吞吐量
print("=== Test 1: Rapid-fire throughput ===")
times = []
for i in range(10):
    start = time.time()
    # 模拟快速读写请求
    open('/dev/null', 'w').write(str(i))
    mid = time.time()
    # 模拟小文件读取
    with open('/Users/kingarthur/finchnest/FINCH.md', 'r') as f:
        _ = f.read(1024)
    end = time.time()
    times.append({'write': round((mid-start)*1000, 1), 'read': round((end-mid)*1000, 1), 'total': round((end-start)*1000, 1)})
    
avg_write = sum(t['write'] for t in times) / len(times)
avg_read = sum(t['read'] for t in times) / len(times)
avg_total = sum(t['total'] for t in times) / len(times)
variance = sum((t['total'] - avg_total)**2 for t in times) / len(times)

results['throughput'] = {
    'avg_write_ms': avg_write,
    'avg_read_ms': avg_read,
    'avg_total_ms': avg_total,
    'variance_ms': variance,
    'max_ms': max(t['total'] for t in times),
    'min_ms': min(t['total'] for t in times)
}
print(f"  Avg: {avg_total:.1f}ms, Variance: {variance:.1f}, Range: {results['throughput']['min_ms']}ms-{results['throughput']['max_ms']}ms")

# Test 2: 大内容渲染压力
print("\n=== Test 2: Large content generation ===")
sizes = [100, 1000, 10000]
for size in sizes:
    start = time.time()
    content = '\n'.join([f'line {i}: ' + 'x' * 50 for i in range(size)])
    # 写入文件模拟渲染输出
    with open('/dev/null', 'w') as f:
        f.write(content)
    elapsed = (time.time() - start) * 1000
    results[f'render_{size}'] = elapsed
    print(f"  {size} lines: {elapsed:.1f}ms")

# Test 3: 系统资源采样
print("\n=== Test 3: System resource sampling ===")
# 获取 Finch 进程内存
try:
    import subprocess
    ps_out = subprocess.run(['ps', '-eo', 'pid,%mem,rss,comm'], capture_output=True, text=True).stdout
    finch_lines = [l for l in ps_out.split('\n') if 'Finch' in l and 'Helper' in l]
    finch_mem = []
    for l in finch_lines[:5]:
        parts = l.split()
        if len(parts) >= 3:
            try:
                finch_mem.append({'pid': parts[0], 'mem_pct': parts[1], 'rss_kb': int(parts[2])})
            except: pass
    
    results['finch_memory'] = finch_mem
    for m in finch_mem:
        print(f"  PID {m['pid']}: {m['mem_pct']}% mem ({m['rss_kb']//1024}MB)")
except: pass

# Test 4: 并发压力
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

threads = []
for i in range(20):
    t = threading.Thread(target=write_task, args=(i,))
    threads.append(t)

start = time.time()
for t in threads:
    t.start()
for t in threads:
    t.join()
total = (time.time() - start) * 1000

avg_concurrent = sum(concurrent_times) / len(concurrent_times)
results['concurrent'] = {
    'total_20_tasks_ms': total,
    'avg_per_task_ms': avg_concurrent,
}
print(f"  20 concurrent tasks: {total:.1f}ms total, {avg_concurrent:.1f}ms avg each")

# Save results
output = {
    'device': os.uname().nodename,
    'platform': sys.platform,
    'python': sys.version,
    'results': results
}

with open('/Users/kingarthur/Downloads/finchstory/finch-perf-test-mac.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Results saved to finch-perf-test-mac.json")
print(json.dumps(results, indent=2, ensure_ascii=False))
