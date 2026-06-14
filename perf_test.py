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
