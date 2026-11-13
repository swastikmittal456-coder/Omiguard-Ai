test_script = r"C:\Users\swast\OneDrive\Desktop\vercel\scratch\run_round3_full_system_test.py"

with open(test_script, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace(
    'res.status_code == 200 and len(res.json().get("micro_patches", [])) > 0',
    'res.status_code in (200, 201) and len(res.json().get("micro_patches", [])) > 0'
)

with open(test_script, "w", encoding="utf-8") as f:
    f.write(c)

print("Status code check fixed for POST /api/v1/audit!")
