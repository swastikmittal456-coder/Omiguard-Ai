with open("scratch/run_full_system_test.py", "r", encoding="utf-8") as f:
    c = f.read()

old_fe = """def test_frontend_live():
    print("\\n=======================================================")
    print("5. FRONTEND SERVER LIVE HYDRATION (Port 3000)")
    print("=======================================================")
    
    tabs = [
        (1, "Multi-Modal Scanner"),
        (2, "Brand Guidelines Knowledge Base"),
        (3, "Governance Hub & Sign-Off"),
        (4, "Compliance Analytics & Policy Drift"),
        (5, "Deterministic Knowledge Graph")
    ]
    
    for tab_num, tab_name in tabs:
        t0 = time.time()
        try:
            req = urllib.request.urlopen(f"http://localhost:3000/?tab={tab_num}", timeout=5)
            elapsed = (time.time() - t0) * 1000
            passed = req.status == 200
            log_test("Frontend Live", f"Module {tab_num}: {tab_name}", passed, f"HTTP Status: {req.status}", elapsed)
        except Exception as e:
            log_test("Frontend Live", f"Module {tab_num}: {tab_name}", False, str(e))"""

new_fe = """def test_frontend_live():
    print("\\n=======================================================")
    print("5. FRONTEND DEDICATED WEBPAGES & HYDRATION (Port 3000)")
    print("=======================================================")
    
    routes = [
        ("/scanner", "Dedicated Page: /scanner (Multi-Modal Scanner)"),
        ("/guidelines", "Dedicated Page: /guidelines (Brand Guidelines Knowledge Base)"),
        ("/governance", "Dedicated Page: /governance (Governance Hub & Sign-Off)"),
        ("/analytics", "Dedicated Page: /analytics (Compliance Analytics & Drift)"),
        ("/graph", "Dedicated Page: /graph (Deterministic Knowledge Graph)"),
        ("/?tab=1", "Tab Query Fallback: /?tab=1"),
        ("/?tab=2", "Tab Query Fallback: /?tab=2"),
        ("/?tab=3", "Tab Query Fallback: /?tab=3"),
        ("/?tab=4", "Tab Query Fallback: /?tab=4"),
        ("/?tab=5", "Tab Query Fallback: /?tab=5"),
    ]
    
    for route, name in routes:
        t0 = time.time()
        try:
            req = urllib.request.urlopen(f"http://localhost:3000{route}", timeout=5)
            elapsed = (time.time() - t0) * 1000
            passed = req.status == 200
            log_test("Frontend Routes", name, passed, f"HTTP Status: {req.status}", elapsed)
        except Exception as e:
            log_test("Frontend Routes", name, False, str(e))"""

c = c.replace(old_fe, new_fe, 1)

with open("scratch/run_full_system_test.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated test_frontend_live in run_full_system_test.py")
