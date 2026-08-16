import statistics
import time
import urllib.request
import urllib.parse

URL = "http://localhost:8000/jobs/search?q=python"
REQUESTS = 50

latencies = []
failures = 0

for _ in range(REQUESTS):
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(URL, timeout=5) as response:
            response.read()
            if response.status != 200:
                failures += 1
    except Exception:
        failures += 1
    latencies.append((time.perf_counter() - started) * 1000)

successful = REQUESTS - failures
print(f"requests={REQUESTS}")
print(f"successful={successful}")
print(f"failures={failures}")
print(f"average_ms={statistics.mean(latencies):.2f}")
print(f"max_ms={max(latencies):.2f}")
