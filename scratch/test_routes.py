import urllib.request
import sys

routes = ["/", "/scanner", "/guidelines", "/governance", "/analytics", "/graph"]
all_ok = True

print("Probing Next.js Dedicated Route Pages on http://localhost:3000 ...")
for r in routes:
    url = f"http://localhost:3000{r}"
    try:
        req = urllib.request.urlopen(url, timeout=10)
        status = req.status
        print(f"  [OK] {url:<32} -> HTTP {status}")
    except Exception as e:
        all_ok = False
        print(f"  [FAIL] {url:<32} -> {e}")

if not all_ok:
    sys.exit(1)
print("\nAll dedicated web routes responded with HTTP 200 OK!")
