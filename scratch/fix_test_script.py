with open("scratch/run_full_system_test.py", "r", encoding="utf-8") as f:
    c = f.read()

old_cert = 'payload = json.dumps({"certificate_hash": "urn:omniguard:sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}).encode(\'utf-8\')'
new_cert = '''conn_c = sqlite3.connect(DB_PATH)
        c_row = conn_c.execute("SELECT certificate_hash FROM compliance_certificates LIMIT 1").fetchone()
        conn_c.close()
        test_hash = c_row[0] if c_row else "urn:omniguard:sha256:OMNI-CERT-0004-VERIFIED"
        payload = json.dumps({"certificate_hash": test_hash}).encode('utf-8')'''

c = c.replace(old_cert, new_cert, 1)

with open("scratch/run_full_system_test.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Updated run_full_system_test.py successfully.")
