path = r"C:\Users\swast\OneDrive\Desktop\vercel\backend\init_db.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Replace the block with separate cur.execute calls
old_block = """    CREATE TABLE rule_citations_map (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guideline_id INTEGER NOT NULL,
        citation_code TEXT NOT NULL UNIQUE,
        clause_title TEXT NOT NULL,
        severity_default TEXT NOT NULL DEFAULT 'medium',
        FOREIGN KEY (guideline_id) REFERENCES guidelines(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS policy_conflicts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_a_title TEXT NOT NULL,
        policy_a_clause TEXT NOT NULL,
        policy_a_text TEXT NOT NULL,
        policy_b_title TEXT NOT NULL,
        policy_b_clause TEXT NOT NULL,
        policy_b_text TEXT NOT NULL,
        conflict_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        suggested_resolution TEXT NOT NULL,
        resolved INTEGER DEFAULT 0,
        resolved_by TEXT,
        resolved_at TEXT
    );

    CREATE TABLE IF NOT EXISTS batch_campaign_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_name TEXT NOT NULL,
        target_channels TEXT NOT NULL,
        total_assets INTEGER NOT NULL,
        compliant_assets INTEGER NOT NULL,
        average_score REAL NOT NULL,
        matrix_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    \"\"\")"""

new_block = """    CREATE TABLE rule_citations_map (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guideline_id INTEGER NOT NULL,
        citation_code TEXT NOT NULL UNIQUE,
        clause_title TEXT NOT NULL,
        severity_default TEXT NOT NULL DEFAULT 'medium',
        FOREIGN KEY (guideline_id) REFERENCES guidelines(id) ON DELETE CASCADE
    );
    \"\"\")

    cur.execute(\"\"\"
    CREATE TABLE IF NOT EXISTS policy_conflicts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_a_title TEXT NOT NULL,
        policy_a_clause TEXT NOT NULL,
        policy_a_text TEXT NOT NULL,
        policy_b_title TEXT NOT NULL,
        policy_b_clause TEXT NOT NULL,
        policy_b_text TEXT NOT NULL,
        conflict_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        suggested_resolution TEXT NOT NULL,
        resolved INTEGER DEFAULT 0,
        resolved_by TEXT,
        resolved_at TEXT
    );
    \"\"\")

    cur.execute(\"\"\"
    CREATE TABLE IF NOT EXISTS batch_campaign_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_name TEXT NOT NULL,
        target_channels TEXT NOT NULL,
        total_assets INTEGER NOT NULL,
        compliant_assets INTEGER NOT NULL,
        average_score REAL NOT NULL,
        matrix_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    \"\"\")"""

if old_block in c:
    c = c.replace(old_block, new_block)
    print("Replaced with separate cur.execute calls!")
else:
    print("Old block not found!")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)
