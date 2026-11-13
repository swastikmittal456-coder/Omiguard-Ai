import sqlite3
import datetime

db_path = r"C:\Users\swast\OneDrive\Desktop\vercel\backend\omniguard.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Create policy_conflicts table
cur.execute("""
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
""")

# 2. Create batch_campaign_audits table
cur.execute("""
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
""")

# Seed policy_conflicts
cur.execute("DELETE FROM policy_conflicts")
conflicts = [
    (
        "Global Digital Advertising Standards",
        "Clause 3.2 (CLM-Q4-FC-019)",
        "Performance claims are permitted across enterprise channels when substantiated by Q4 internal benchmarks or certification #CLM-Q4-FC-019.",
        "EU Regional Consumer Protection & Transparency Directive",
        "Clause 7.1 (GDPR-EU-004)",
        "All consumer-facing marketing must explicitly state 'Results may vary by enterprise tier' with a persistent, non-dismissible disclaimer; unquantified absolute performance claims are prohibited regardless of internal certification.",
        "direct_contradiction",
        "critical",
        "Harmonize: Require qualifying asterisk disclaimer ('*Results vary by deployment scale') across international variants while referencing benchmark certification.",
        0, None, None
    ),
    (
        "Brand Palette & Visual Identity v2.4",
        "Clause 1.2 (MBG-4.2-CL-008)",
        "Secondary interactive call-to-action buttons should utilize Brand Warning Amber #FBBF24 on pure white backgrounds for maximum brand warmth.",
        "Digital Accessibility & APCA Policy v1.1",
        "Clause 4.3 (A11Y-STD-004)",
        "All interactive UI elements, buttons, and visual overlays must achieve an APCA lightness contrast of at least Lc 75.0 against adjacent surface backgrounds.",
        "contrast_inversion",
        "critical",
        "Contrast Adjustment: Darken Amber token to #D97706 or invert button container to #18181B to achieve APCA Lc = 82.4, satisfying accessibility mandates.",
        0, None, None
    ),
    (
        "Social Media Brand Voice & Brevity",
        "Clause 2.4 (SOC-SPD-001)",
        "Keep all mobile social ad copy under 90 characters for conversion rate optimization, strictly omitting long-form legal footers from the visual banner.",
        "Financial Compliance & FTC Safe Harbor",
        "Clause 5.3 (IR-FIN-001)",
        "Any promotional metric referencing cost savings, ROI, or compliance velocity must provide a prominent footnote disclosure visible in the primary viewport.",
        "jurisdiction_clash",
        "high",
        "Adaptive Footer: Adopt micro-expander footnote convention ('*Details apply') satisfying statutory visibility within mobile character budgets.",
        0, None, None
    ),
    (
        "Executive Communications & Press Standard",
        "Clause 4.1 (PR-EXE-001)",
        "External press releases regarding AI capabilities must name specific model weights and version numbers for technical authority and investor transparency.",
        "Enterprise Security & AI Governance Framework",
        "Clause 8.4 (SEC-SOC-002)",
        "Model architecture details, proprietary weights, and raw vector dimensions must remain classified as Confidential Intellectual Property and never be named in external distribution.",
        "direct_contradiction",
        "high",
        "IP Boundary: Authorize high-level capability terminology ('Enterprise-grade neural retrieval') while redacting internal model weights and vector dimensions.",
        0, None, None
    )
]

cur.executemany("""
INSERT INTO policy_conflicts (
    policy_a_title, policy_a_clause, policy_a_text,
    policy_b_title, policy_b_clause, policy_b_text,
    conflict_type, severity, suggested_resolution,
    resolved, resolved_by, resolved_at
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
""", conflicts)

# Seed batch_campaign_audits
cur.execute("DELETE FROM batch_campaign_audits")
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sample_matrix = [
    {
        "asset_id": 1,
        "asset_name": "Q4 Enterprise Hero Banner",
        "channel": "google_ads",
        "status": "warning",
        "compliance_score": 68.0,
        "violations": ["Prohibited 100% guarantee (Clause 3.2)", "Amber on White contrast (APCA Lc: 27.8)"],
        "patch_available": True
    },
    {
        "asset_id": 2,
        "asset_name": "LinkedIn B2B Leadership Post",
        "channel": "linkedin",
        "status": "compliant",
        "compliance_score": 94.0,
        "violations": [],
        "patch_available": False
    },
    {
        "asset_id": 3,
        "asset_name": "Instagram Story Promo Carousel",
        "channel": "meta",
        "status": "critical",
        "compliance_score": 52.0,
        "violations": ["Unsubstantiated 'unrivaled leader' claim (Clause 5.1)", "Safe margin boundary incursion"],
        "patch_available": True
    },
    {
        "asset_id": 4,
        "asset_name": "Executive Email Digest Blast",
        "channel": "email",
        "status": "compliant",
        "compliance_score": 96.0,
        "violations": [],
        "patch_available": False
    }
]

import json
cur.execute("""
INSERT INTO batch_campaign_audits (
    campaign_name, target_channels, total_assets, compliant_assets, average_score, matrix_json, created_at
) VALUES (?,?,?,?,?,?,?)
""", (
    "Q4 Global Enterprise Launch Campaign",
    "google_ads,meta,linkedin,email",
    4, 2, 77.5, json.dumps(sample_matrix), now
))

conn.commit()
conn.close()
print("Updated omniguard.db with policy_conflicts and batch_campaign_audits tables!")
