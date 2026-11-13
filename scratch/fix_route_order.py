path = r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# First, extract the conflicts code block from bottom
conflicts_block = """# =====================================================================
#  Round 3 Improvement 3: Policy Conflict Detector & Diff Merger
# =====================================================================
class ResolveConflictRequest(BaseModel):
    conflict_id: int
    resolution_strategy: str  # merge, adopt_stricter, override
    merged_clause_text: Optional[str] = None
    reviewer_role: Optional[str] = "Office of General Counsel"
    notes: Optional[str] = None

@app.get("/api/v1/guidelines/conflicts")
def get_policy_conflicts():
    \"\"\"
    Detects and returns cross-policy contradictions between indexed brand guidelines
    and regulatory directives with clause texts, severity ratings, and recommended resolutions.
    \"\"\"
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute(\"\"\"
        SELECT id, policy_a_title, policy_a_clause, policy_a_text,
               policy_b_title, policy_b_clause, policy_b_text,
               conflict_type, severity, suggested_resolution,
               resolved, resolved_by, resolved_at
        FROM policy_conflicts
        ORDER BY id ASC
    \"\"\").fetchall()
    conn.close()

    conflicts = []
    for r in rows:
        conflicts.append({
            "id": r[0],
            "policy_a": {
                "title": r[1],
                "clause": r[2],
                "text": r[3],
            },
            "policy_b": {
                "title": r[4],
                "clause": r[5],
                "text": r[6],
            },
            "conflict_type": r[7],
            "severity": r[8],
            "suggested_resolution": r[9],
            "resolved": bool(r[10]),
            "resolved_by": r[11],
            "resolved_at": r[12],
        })
    return {
        "total_conflicts": len(conflicts),
        "unresolved_count": sum(1 for c in conflicts if not c["resolved"]),
        "conflicts": conflicts
    }

@app.post("/api/v1/guidelines/resolve-conflict")
def resolve_policy_conflict(body: ResolveConflictRequest):
    \"\"\"
    Applies resolution to a detected policy conflict, merges conflicting clauses,
    and logs the action to the immutable SQLite review history ledger.
    \"\"\"
    conn = get_db()
    cur = conn.cursor()
    ts = _now()
    cur.execute(\"\"\"
        UPDATE policy_conflicts
        SET resolved = 1, resolved_by = ?, resolved_at = ?
        WHERE id = ?
    \"\"\", (body.reviewer_role, ts, body.conflict_id))

    # Log to immutable review ledger
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
    ))
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "conflict_id": body.conflict_id,
        "resolution_strategy": body.resolution_strategy,
        "resolved_by": body.reviewer_role,
        "resolved_at": ts,
        "message": f"Policy Conflict #{body.conflict_id} resolved and recorded to immutable ledger."
    }
"""

c = c.replace(conflicts_block, "")

# Insert conflicts_block right before @app.get("/api/v1/guidelines/{guideline_id}")
target = '@app.get("/api/v1/guidelines/{guideline_id}")'
c = c.replace(target, conflicts_block + "\n\n" + target)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Moved conflicts route before parameterized {guideline_id} route!")
