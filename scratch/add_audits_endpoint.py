with open('backend/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '@app.post("/api/v1/audit", status_code=201)'
replacement = """@app.get("/api/v1/audits")
def get_recent_audits(limit: int = 15):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, channel, draft_text, compliance_score, tone_status, claim_status, color_status, contrast_status, created_at FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    audits = [
        {
            "id": r["id"],
            "channel": r["channel"],
            "draft_text": r["draft_text"],
            "compliance_score": r["compliance_score"],
            "tone_status": r["tone_status"],
            "claim_status": r["claim_status"],
            "color_status": r["color_status"],
            "contrast_status": r["contrast_status"],
            "created_at": r["created_at"],
        }
        for r in rows
    ]
    return {"audits": audits, "total": len(audits)}


@app.post("/api/v1/audit", status_code=201)"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully added /api/v1/audits to backend/main.py")
else:
    print("Target not found")
