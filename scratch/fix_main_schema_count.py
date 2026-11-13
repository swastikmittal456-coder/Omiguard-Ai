main_path = r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py"

with open(main_path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update root to dynamically count tables
old_root = '''@app.get("/")
def root():
    return {
        "service": "OmniGuard AI Production Platform",
        "version": "3.0.0",
        "schema_tables": 15,
        "database": "omniguard.db",
        "status": "operational",
    }'''

new_root = '''@app.get("/")
def root():
    conn = get_db()
    tbl_count = len(conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall())
    conn.close()
    return {
        "service": "OmniGuard AI Production Platform",
        "version": "3.0.0",
        "schema_tables": tbl_count,
        "database": "omniguard.db",
        "status": "operational",
    }'''

if old_root in c:
    c = c.replace(old_root, new_root)
    print("Updated root() to dynamic table count!")

# 2. Update line 542 in create_audit for 'guarantee'
old_audit_check = '''if re.search(r"\\b100\\s*%\\s*(compliance|accuracy|guarantee)", lower_text) or "guarantees" in lower_text:'''
new_audit_check = '''if re.search(r"\\b100\\s*%\\s*(compliance|accuracy|guarantee)", lower_text) or "guarantee" in lower_text or "100%" in lower_text:'''

if old_audit_check in c:
    c = c.replace(old_audit_check, new_audit_check)
    print("Updated legal claim check to catch 'guarantee' and '100%'!")

# 3. Export calculate_apca and cielab_delta_e
export_funcs = '''
# Exported utility aliases for testing
calculate_apca = _apca_contrast
cielab_delta_e = _color_delta_e
'''

if "calculate_apca = _apca_contrast" not in c:
    c = c + export_funcs
    print("Exported calculate_apca and cielab_delta_e!")

with open(main_path, "w", encoding="utf-8") as f:
    f.write(c)

print("backend/main.py updated successfully!")
