path = r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

target = """    # Log to immutable review ledger
    cur.execute(\"\"\"
        INSERT INTO review_history (audit_id, reviewer_role, action_taken, comment, user_name, created_at)
        VALUES (?,?,?,?,?,?)
    \"\"\", (
        body.conflict_id,
        "legal_counsel",
        f"conflict_{body.resolution_strategy}",
        body.notes or f"Conflict #{body.conflict_id} resolved via {body.resolution_strategy.upper()} strategy.",
        body.reviewer_role,
        ts
    ))"""

replacement = """    # Log to immutable review ledger
    cur.execute(\"\"\"
        INSERT INTO review_history (audit_id, reviewer_role, action_taken, comment, timestamp)
        VALUES (?,?,?,?,?)
    \"\"\", (
        body.conflict_id,
        "legal_counsel",
        f"conflict_{body.resolution_strategy}",
        body.notes or f"Conflict #{body.conflict_id} resolved by {body.reviewer_role} via {body.resolution_strategy.upper()} strategy.",
        ts
    ))"""

if target in c:
    c = c.replace(target, replacement)
    print("Replaced successfully!")
else:
    print("Target not found!")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)
