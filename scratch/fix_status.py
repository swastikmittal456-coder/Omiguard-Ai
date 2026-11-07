with open("backend/main.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('"delta_e_status": "pass" if color_pass else "fail",', '"delta_e_status": "passed" if color_pass else "failed",')
c = c.replace('"apca_status": "pass" if apca_pass else "fail",', '"apca_status": "passed" if apca_pass else "failed",')

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(c)

with open("scratch/run_full_system_test.py", "r", encoding="utf-8") as f:
    t = f.read()

t = t.replace('data.get("delta_e_status") == "passed" and data.get("apca_status") == "passed"', 'data.get("delta_e_status") in ("pass", "passed") and data.get("apca_status") in ("pass", "passed")')

with open("scratch/run_full_system_test.py", "w", encoding="utf-8") as f:
    f.write(t)

print("Updated status check.")
