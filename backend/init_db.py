# -*- coding: utf-8 -*-
"""
OmniGuard AI — 15-Table Enterprise Relational Database Initializer.
Ensures full foreign key constraints, PRAGMA foreign_keys = ON,
and rich enterprise-scale seed datasets.
"""
import os
import sqlite3
import hashlib
from datetime import datetime, timezone, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "omniguard.db")

def _ts(offset_hours=0):
    dt = datetime.now(timezone.utc) - timedelta(hours=offset_hours)
    return dt.strftime("%Y-%m-%d %H:%M:%S+00:00")

def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def init_database():
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except OSError:
            pass

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    # 1. guidelines
    cur.execute("""
    CREATE TABLE guidelines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        file_type TEXT NOT NULL,
        clause_count INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'indexed',
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL
    );
    """)

    # 2. vector_chunks
    cur.execute("""
    CREATE TABLE vector_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guideline_id INTEGER NOT NULL,
        clause_citation TEXT NOT NULL,
        chunk_text TEXT NOT NULL,
        qdrant_embedding_id TEXT NOT NULL,
        similarity_score REAL NOT NULL DEFAULT 0.95,
        FOREIGN KEY (guideline_id) REFERENCES guidelines(id) ON DELETE CASCADE
    );
    """)

    # 3. knowledge_graph_nodes
    cur.execute("""
    CREATE TABLE knowledge_graph_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_clause TEXT NOT NULL,
        target_fact TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        neo4j_node_id TEXT NOT NULL
    );
    """)

    # 4. visual_asset_tokens
    cur.execute("""
    CREATE TABLE visual_asset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_name TEXT NOT NULL,
        hex_color TEXT NOT NULL,
        allowed_delta REAL NOT NULL DEFAULT 3.0,
        min_apca_contrast REAL NOT NULL DEFAULT 75.0,
        rgb_coords TEXT NOT NULL DEFAULT '0,0,0',
        cielab_coords TEXT NOT NULL DEFAULT '0,0,0'
    );
    """)

    # 5. channel_policies
    cur.execute("""
    CREATE TABLE channel_policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_name TEXT NOT NULL UNIQUE,
        max_char_count INTEGER NOT NULL,
        forbidden_words TEXT NOT NULL,
        required_disclaimers TEXT NOT NULL,
        aspect_ratio TEXT NOT NULL DEFAULT '16:9',
        target_audience TEXT NOT NULL DEFAULT 'B2B Enterprise',
        strictness_level TEXT NOT NULL DEFAULT 'high'
    );
    """)

    # 6. audit_logs
    cur.execute("""
    CREATE TABLE audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel TEXT NOT NULL,
        draft_text TEXT NOT NULL,
        compliance_score REAL NOT NULL,
        tone_status TEXT NOT NULL,
        claim_status TEXT NOT NULL,
        color_status TEXT NOT NULL,
        contrast_status TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    # 7. micro_patches
    cur.execute("""
    CREATE TABLE micro_patches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_id INTEGER NOT NULL,
        severity TEXT NOT NULL,
        issue_description TEXT NOT NULL,
        guideline_clause TEXT NOT NULL,
        original_snippet TEXT NOT NULL,
        patched_snippet TEXT NOT NULL,
        patch_applied INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (audit_id) REFERENCES audit_logs(id) ON DELETE CASCADE
    );
    """)

    # 8. review_history
    cur.execute("""
    CREATE TABLE review_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_id INTEGER NOT NULL,
        reviewer_role TEXT NOT NULL,
        action_taken TEXT NOT NULL,
        comment TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (audit_id) REFERENCES audit_logs(id) ON DELETE CASCADE
    );
    """)

    # 9. guideline_analytics
    cur.execute("""
    CREATE TABLE guideline_analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clause_citation TEXT NOT NULL UNIQUE,
        violation_count INTEGER NOT NULL DEFAULT 0,
        ambiguity_flag INTEGER NOT NULL DEFAULT 0,
        last_triggered TEXT NOT NULL
    );
    """)

    # 10. brand_assets
    cur.execute("""
    CREATE TABLE brand_assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_title TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        file_path TEXT NOT NULL,
        approved_by TEXT NOT NULL,
        version TEXT NOT NULL DEFAULT '1.0'
    );
    """)

    # 11. team_roles
    cur.execute("""
    CREATE TABLE team_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE,
        user_name TEXT NOT NULL,
        permission_level TEXT NOT NULL,
        can_approve INTEGER NOT NULL DEFAULT 0
    );
    """)

    # 12. compliance_certificates
    cur.execute("""
    CREATE TABLE compliance_certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_id INTEGER NOT NULL,
        certificate_hash TEXT NOT NULL UNIQUE,
        issued_at TEXT NOT NULL,
        signer_role TEXT NOT NULL,
        FOREIGN KEY (audit_id) REFERENCES audit_logs(id) ON DELETE CASCADE
    );
    """)

    # 13. apca_contrast_checks
    cur.execute("""
    CREATE TABLE apca_contrast_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_id INTEGER NOT NULL,
        fg_hex TEXT NOT NULL,
        bg_hex TEXT NOT NULL,
        apca_score REAL NOT NULL,
        wcag_status TEXT NOT NULL,
        FOREIGN KEY (audit_id) REFERENCES audit_logs(id) ON DELETE CASCADE
    );
    """)

    # 14. opencv_color_deltas
    cur.execute("""
    CREATE TABLE opencv_color_deltas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_id INTEGER NOT NULL,
        detected_hex TEXT NOT NULL,
        target_token TEXT NOT NULL,
        delta_e REAL NOT NULL,
        is_compliant INTEGER NOT NULL,
        FOREIGN KEY (audit_id) REFERENCES audit_logs(id) ON DELETE CASCADE
    );
    """)

    # 15. rule_citations_map
    cur.execute("""
    CREATE TABLE rule_citations_map (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guideline_id INTEGER NOT NULL,
        citation_code TEXT NOT NULL UNIQUE,
        clause_title TEXT NOT NULL,
        severity_default TEXT NOT NULL DEFAULT 'medium',
        FOREIGN KEY (guideline_id) REFERENCES guidelines(id) ON DELETE CASCADE
    );
    """)

    # ─────────────────────────────────────────────────────────────────
    # SEED DATA INSERTION
    # ─────────────────────────────────────────────────────────────────

    # 1. Guidelines (18 rows)
    guidelines_data = [
        ("OmniGuard Master Brand Guidelines v4.2", "visual_identity", "pdf", 18, "indexed", 1, _ts(720)),
        ("Q4 Enterprise Legal Claims Fact Base", "legal_claims", "json", 24, "indexed", 1, _ts(680)),
        ("Global Tone of Voice & Buzzword Policy", "tone_voice", "docx", 14, "indexed", 1, _ts(640)),
        ("WCAG 2.2 AA & APCA Accessibility Spec", "accessibility", "pdf", 12, "indexed", 1, _ts(600)),
        ("Social Media Speed & Brevity Matrix", "social_media", "json", 16, "indexed", 1, _ts(560)),
        ("Packaging & Industrial Print Standards", "print_packaging", "pdf", 20, "indexed", 1, _ts(520)),
        ("Partner Co-Branding & Licensing Rules", "partnerships", "pdf", 10, "indexed", 1, _ts(480)),
        ("Executive Leadership Speech Directives", "pr_communications", "docx", 8, "indexed", 1, _ts(440)),
        ("AI Provenance & Metadata Tagging Charter", "governance_ai", "json", 15, "indexed", 1, _ts(400)),
        ("Omnichannel Video & Motion Graphics Guide", "motion_design", "pdf", 14, "indexed", 1, _ts(360)),
        ("EU / GDPR Regional Marketing Compliance", "regional_legal", "pdf", 22, "indexed", 1, _ts(320)),
        ("Security & SOC 2 Claims Verification Standard", "security_claims", "json", 16, "indexed", 1, _ts(280)),
        ("Investor Relations & Financial Disclosure Guide", "investor_relations", "pdf", 26, "indexed", 1, _ts(240)),
        ("Email Newsletter & CRM Design Directives", "email_crm", "docx", 12, "indexed", 1, _ts(200)),
        ("Employer Branding & Recruitment Tone Policy", "human_resources", "pdf", 10, "indexed", 1, _ts(160)),
        ("Developer Documentation & API Style Sheet", "engineering_docs", "json", 18, "indexed", 1, _ts(120)),
        ("Out-of-Home (OOH) Billboard Legibility Spec", "out_of_home", "pdf", 14, "indexed", 1, _ts(80)),
        ("Micro-Influencer & Ambassador Guidelines", "influencer_marketing", "docx", 12, "indexed", 1, _ts(40)),
    ]
    cur.executemany("""
    INSERT INTO guidelines (title, category, file_type, clause_count, status, is_active, created_at)
    VALUES (?,?,?,?,?,?,?)
    """, guidelines_data)

    # 15. rule_citations_map (25 rows)
    rule_citations = [
        (1, "MBG-4.2-CL-001", "Primary Brand Mark Clear Space Requirement", "high"),
        (1, "MBG-4.2-CL-002", "Secondary Monochrome Wordmark Standard", "medium"),
        (1, "MBG-4.2-CL-005", "Prohibited Gradient & Texture Alterations", "critical"),
        (1, "MBG-4.2-CL-014", "Registered Trademark Symbol First Mention", "medium"),
        (2, "CLM-Q4-FC-001", "Substantiated Violation Reduction Metric (94%)", "critical"),
        (2, "CLM-Q4-FC-003", "Benchmark Cohort Sample Size Disclosure (N=1247)", "high"),
        (2, "CLM-Q4-FC-007", "SOC 2 Type II Certification Scope Restriction", "critical"),
        (2, "CLM-Q4-FC-012", "Proprietary Machine Learning Model Footnote", "high"),
        (2, "CLM-Q4-FC-019", "Comparative Competitor Claims Third-Party Audit", "critical"),
        (2, "CLM-Q4-FC-028", "Superlative Claim Analyst Citation Requirement", "high"),
        (3, "TON-GLO-001", "Confident, Clear, Warm, Expert Voice Pillars", "medium"),
        (3, "TON-GLO-004", "Prohibited Technical Jargon in Public Headlines", "medium"),
        (3, "TON-GLO-009", "Corporate Buzzword Lexicon (disrupt, synergy, needle)", "high"),
        (3, "TON-GLO-012", "Passive Voice Restriction in Hero Copy", "low"),
        (4, "A11Y-STD-001", "APCA Contrast Minimum Lc >= 75 on Primary Surfaces", "critical"),
        (4, "A11Y-STD-004", "APCA Contrast Minimum Lc >= 60 for Body Text", "high"),
        (4, "A11Y-STD-009", "Non-Text UI Component Contrast (3:1 minimum)", "medium"),
        (5, "SOC-SPD-001", "X / Twitter Maximum Character Budget (280 chars)", "critical"),
        (5, "SOC-SPD-005", "Mandatory Asterisk Footnote Link on Social Feeds", "high"),
        (6, "PKG-PRT-003", "CMYK to Spot Color Conversion Tolerances", "high"),
        (7, "PRT-LIC-002", "Co-Branding 50/50 Visual Weight Parity", "medium"),
        (9, "GOV-TAG-001", "Lightweight AI Provenance Header Injection", "high"),
        (11, "GDPR-EU-004", "Cookie & Tracking Explicit Consent Notice", "critical"),
        (12, "SEC-SOC-002", "Encrypted Data at Rest (AES-256) Claim Verification", "critical"),
        (17, "OOH-LEG-001", "Minimum 120pt Headline Legibility at 50 Feet", "high"),
    ]
    cur.executemany("""
    INSERT INTO rule_citations_map (guideline_id, citation_code, clause_title, severity_default)
    VALUES (?,?,?,?)
    """, rule_citations)

    # 2. vector_chunks (45 rows)
    vector_chunks_data = [
        (1, "MBG-4.2-CL-001", "The primary OmniGuard mark must always retain an unobstructed clear space equal to 1.5x the height of the letter O on all sides.", "vec-qdrant-mbg-001", 0.98),
        (1, "MBG-4.2-CL-002", "Secondary wordmark variants may only appear in Zinc-900 on light backgrounds or Pure White (#FFFFFF) on dark backgrounds.", "vec-qdrant-mbg-002", 0.95),
        (1, "MBG-4.2-CL-005", "Applying drop shadows, gradients, skews, or 3D extrusions to the official brand mark is strictly prohibited.", "vec-qdrant-mbg-005", 0.97),
        (1, "MBG-4.2-CL-014", "The registered trademark symbol must be appended to the first prominent occurrence of OmniGuard in all enterprise media.", "vec-qdrant-mbg-014", 0.93),
        (2, "CLM-Q4-FC-001", "The claim 'reduces brand violations by up to 94%' is legally approved only when referencing the Q4-2026 enterprise cohort benchmark.", "vec-qdrant-clm-001", 0.99),
        (2, "CLM-Q4-FC-003", "All quantitative performance claims must disclose the sample size (N=1,247) and audit timeframe in an adjacent footnote.", "vec-qdrant-clm-003", 0.96),
        (2, "CLM-Q4-FC-007", "Claims of 'enterprise-grade security' are substantiated solely by our active SOC 2 Type II audit report dated October 2026.", "vec-qdrant-clm-007", 0.97),
        (2, "CLM-Q4-FC-012", "Marketing references to 'AI-powered' or 'intelligent automation' require explicit disclosure of proprietary machine learning models.", "vec-qdrant-clm-012", 0.94),
        (2, "CLM-Q4-FC-019", "Direct comparative claims against named market competitors require pre-approved third-party legal audit documentation.", "vec-qdrant-clm-019", 0.98),
        (2, "CLM-Q4-FC-028", "Superlative claims including 'industry-leading', 'unmatched', or 'fastest' must cite independent analyst reports published within 12 months.", "vec-qdrant-clm-028", 0.96),
        (3, "TON-GLO-001", "The OmniGuard tone of voice is Confident, Clear, Warm, and Expert. Avoid overly casual slang, aloof academic jargon, or aggressive hype.", "vec-qdrant-ton-001", 0.95),
        (3, "TON-GLO-004", "Do not use internal acronyms or dense engineering shorthand in public headlines; speak to business outcomes.", "vec-qdrant-ton-004", 0.92),
        (3, "TON-GLO-009", "Prohibited corporate buzzword lexicon: disrupting, game-changing, synergy, leverage as a verb, move the needle, pivot, paradigm shift.", "vec-qdrant-ton-009", 0.99),
        (3, "TON-GLO-012", "Hero headlines must employ active verbs and direct address ('Protect your brand across every touchpoint').", "vec-qdrant-ton-012", 0.91),
        (4, "A11Y-STD-001", "Text-on-surface pairings must achieve an APCA contrast score of Lc >= 75 for large copy (>24px) to satisfy WCAG 2.2 AA.", "vec-qdrant-a11y-001", 0.99),
        (4, "A11Y-STD-004", "Body text smaller than 18px requires an APCA contrast rating of Lc >= 60 on all standard desktop and mobile viewports.", "vec-qdrant-a11y-004", 0.97),
        (4, "A11Y-STD-009", "Interactive UI elements and icons must maintain a 3:1 contrast against adjacent background fills.", "vec-qdrant-a11y-009", 0.94),
        (5, "SOC-SPD-001", "Posts on X / Twitter cannot exceed 280 characters under any circumstance; compliance scanner enforces strict truncation.", "vec-qdrant-soc-001", 0.98),
        (5, "SOC-SPD-005", "Social posts with statistical claims must include a verified short-link (*T&C: omniguard.ai/legal) to the primary methodology.", "vec-qdrant-soc-005", 0.93),
        (6, "PKG-PRT-003", "For flexographic packaging print runs, Delta-E tolerances cannot exceed 2.0 when measured against Pantone 2728 C.", "vec-qdrant-pkg-003", 0.96),
        (7, "PRT-LIC-002", "When co-branding with enterprise partners, partner logo height cannot exceed 85% of the OmniGuard primary wordmark.", "vec-qdrant-prt-002", 0.95),
        (8, "PR-EXE-001", "Press release headlines must state the news event objectively within 110 characters, followed by a factual sub-headline.", "vec-qdrant-pr-001", 0.94),
        (9, "GOV-TAG-001", "All media assets vetted by OmniGuard must be stamped with a verifiable SHA-256 provenance hash tag before publishing.", "vec-qdrant-gov-001", 0.97),
        (10, "MOT-VID-002", "Video title cards must hold for at least 1.5 seconds per 8 words to guarantee viewer cognitive legibility.", "vec-qdrant-mot-002", 0.93),
        (11, "GDPR-EU-004", "Campaign assets targeted to EU member states must not promise unconditional profiling without explicit affirmative opt-in.", "vec-qdrant-gdp-004", 0.98),
        (12, "SEC-SOC-002", "Technical communications may state 'Zero Customer Data Retained for Model Training' backed by our air-gapped Qdrant architecture.", "vec-qdrant-sec-002", 0.99),
        (13, "IR-FIN-001", "All non-GAAP financial forward metrics must be immediately preceded by the standard safe-harbor cautionary statement.", "vec-qdrant-ir-001", 0.96),
        (14, "CRM-EML-003", "Marketing email preview preheaders must be under 85 characters and complement rather than duplicate the subject line.", "vec-qdrant-crm-003", 0.92),
        (15, "HR-REC-002", "Recruitment job postings must refrain from biased gender-coded words ('rockstar', 'dominant', 'guru').", "vec-qdrant-hr-002", 0.94),
        (16, "DEV-API-001", "API documentation must follow the Google Developer Documentation Style Guide with active curl code examples.", "vec-qdrant-dev-001", 0.95),
        (17, "OOH-LEG-001", "Billboard copy must not exceed 7 words total to guarantee safe vehicular reading comprehension at highway speeds.", "vec-qdrant-ooh-001", 0.97),
        (18, "INF-AMB-003", "Influencer partners must place #OmniGuardPartner or #Ad within the first three words of their video descriptions.", "vec-qdrant-inf-003", 0.98),
        (1, "MBG-4.2-CL-008", "The primary brand palette comprises Indigo-600 (#4F46E5), Slate-900 (#0F172A), and Pure White (#FFFFFF).", "vec-qdrant-mbg-008", 0.99),
        (2, "CLM-Q4-FC-015", "Customer logo usage on collateral requires written mutual licensing agreements countersigned within 24 months.", "vec-qdrant-clm-015", 0.95),
        (3, "TON-GLO-006", "Avoid alarmist security fear-mongering; communicate resilience and proactive governance rather than imminent doom.", "vec-qdrant-ton-006", 0.96),
        (4, "A11Y-STD-007", "Color must never be the sole visual means of conveying critical information, errors, or required field states.", "vec-qdrant-a11y-007", 0.98),
        (5, "SOC-SPD-008", "Instagram carousel graphics must maintain 1080x1350 vertical aspect ratio with 120px safety margins top and bottom.", "vec-qdrant-soc-008", 0.94),
        (9, "GOV-TAG-004", "Cryptographic compliance certificates must specify the approving authority role (Creator, Brand Lead, Legal).", "vec-qdrant-gov-004", 0.97),
        (11, "GDPR-EU-008", "Email marketing to French and German business domains must provide single-click double opt-in unsubscription.", "vec-qdrant-gdp-008", 0.96),
        (12, "SEC-SOC-005", "Customer cryptographic keys must be held in dedicated AWS KMS HSM modules with envelope encryption.", "vec-qdrant-sec-005", 0.98),
        (16, "DEV-API-004", "REST endpoints must return standardized RFC 7807 problem details payloads on all 4xx/5xx responses.", "vec-qdrant-dev-004", 0.95),
        (17, "OOH-LEG-004", "Digital billboard animations cannot flash at frequencies between 3Hz and 60Hz to prevent photo-sensitive seizures.", "vec-qdrant-ooh-004", 0.99),
        (18, "INF-AMB-006", "Ambassadors must not make unapproved competitive claims about legacy compliance audit software.", "vec-qdrant-inf-006", 0.97),
        (3, "TON-GLO-015", "Executive thought leadership pieces must focus on empowering creative autonomy through automated guardrails.", "vec-qdrant-ton-015", 0.94),
        (2, "CLM-Q4-FC-035", "Savings claims regarding '70% review time reduction' cite our validated 2026 customer productivity index.", "vec-qdrant-clm-035", 0.98),
    ]
    cur.executemany("""
    INSERT INTO vector_chunks (guideline_id, clause_citation, chunk_text, qdrant_embedding_id, similarity_score)
    VALUES (?,?,?,?,?)
    """, vector_chunks_data)

    # 3. knowledge_graph_nodes (40 rows)
    knowledge_graph = [
        ("MBG-4.2-CL-001", "Primary Indigo-600 Mark", "EXTRACTED_FROM", "neo4j-node-101"),
        ("MBG-4.2-CL-001", "1.5x Letter-O Clear Space", "MANDATES", "neo4j-node-102"),
        ("MBG-4.2-CL-002", "Secondary Wordmark in Zinc-900", "SUBSTANTIATES", "neo4j-node-103"),
        ("MBG-4.2-CL-005", "Drop Shadows & Gradients", "CONTRADICTS", "neo4j-node-104"),
        ("MBG-4.2-CL-014", "Registered Trademark Symbol", "MANDATES", "neo4j-node-105"),
        ("CLM-Q4-FC-001", "Up to 94% Brand Violation Reduction", "SUBSTANTIATES", "neo4j-node-106"),
        ("CLM-Q4-FC-001", "100% Guaranteed Brand Compliance", "CONTRADICTS", "neo4j-node-107"),
        ("CLM-Q4-FC-003", "Enterprise Benchmark Sample N=1247", "EXTRACTED_FROM", "neo4j-node-108"),
        ("CLM-Q4-FC-007", "SOC 2 Type II Security Standard", "SUBSTANTIATES", "neo4j-node-109"),
        ("CLM-Q4-FC-012", "Proprietary Machine Learning Models", "SUBSTANTIATES", "neo4j-node-110"),
        ("CLM-Q4-FC-019", "Unverified Comparative Claims", "CONTRADICTS", "neo4j-node-111"),
        ("CLM-Q4-FC-028", "Superlative Industry-Leading Claims", "EXTRACTED_FROM", "neo4j-node-112"),
        ("TON-GLO-001", "Confident, Clear, Warm, Expert Pillars", "MANDATES", "neo4j-node-113"),
        ("TON-GLO-004", "Dense Engineering Shorthand", "CONTRADICTS", "neo4j-node-114"),
        ("TON-GLO-009", "Corporate Buzzword: Disrupting", "CONTRADICTS", "neo4j-node-115"),
        ("TON-GLO-009", "Corporate Buzzword: Synergy", "CONTRADICTS", "neo4j-node-116"),
        ("TON-GLO-009", "Corporate Buzzword: Move the Needle", "CONTRADICTS", "neo4j-node-117"),
        ("TON-GLO-009", "Corporate Buzzword: Leverage as Verb", "CONTRADICTS", "neo4j-node-118"),
        ("A11Y-STD-001", "WCAG 2.2 AA Contrast Standard", "MANDATES", "neo4j-node-119"),
        ("A11Y-STD-001", "APCA Contrast Minimum Lc >= 75", "SUBSTANTIATES", "neo4j-node-120"),
        ("A11Y-STD-004", "APCA Body Text Minimum Lc >= 60", "SUBSTANTIATES", "neo4j-node-121"),
        ("SOC-SPD-001", "Twitter Character Budget (280 max)", "MANDATES", "neo4j-node-122"),
        ("SOC-SPD-005", "Mandatory Legal Asterisk Link", "MANDATES", "neo4j-node-123"),
        ("PKG-PRT-003", "Delta-E <= 2.0 on Pantone 2728 C", "SUBSTANTIATES", "neo4j-node-124"),
        ("GOV-TAG-001", "Lightweight AI Provenance Hash", "MANDATES", "neo4j-node-125"),
        ("GDPR-EU-004", "EU Explicit Consent Directives", "MANDATES", "neo4j-node-126"),
        ("SEC-SOC-002", "Zero Customer Data Retained Policy", "SUBSTANTIATES", "neo4j-node-127"),
        ("IR-FIN-001", "Safe-Harbor Cautionary Language", "MANDATES", "neo4j-node-128"),
        ("CRM-EML-003", "Preheader Character Budget (85 max)", "MANDATES", "neo4j-node-129"),
        ("HR-REC-002", "Gender-Neutral Job Posting Syntax", "MANDATES", "neo4j-node-130"),
        ("DEV-API-001", "Google Developer Documentation Style", "EXTRACTED_FROM", "neo4j-node-131"),
        ("OOH-LEG-001", "7-Word Maximum Vehicular Legibility", "MANDATES", "neo4j-node-132"),
        ("INF-AMB-003", "Sponsorship Disclosure #OmniGuardPartner", "MANDATES", "neo4j-node-133"),
        ("MBG-4.2-CL-008", "Hex #4F46E5 Primary Brand Mark", "EXTRACTED_FROM", "neo4j-node-134"),
        ("CLM-Q4-FC-035", "70% Review Time Reduction Metric", "SUBSTANTIATES", "neo4j-node-135"),
        ("TON-GLO-012", "Active Voice Hero Headline Syntax", "MANDATES", "neo4j-node-136"),
        ("TON-GLO-015", "Creative Autonomy Over Fear-Mongering", "SUBSTANTIATES", "neo4j-node-137"),
        ("A11Y-STD-007", "Dual Redundancy for Color Semantics", "MANDATES", "neo4j-node-138"),
        ("OOH-LEG-004", "Seizure Prevention Flashing Limits", "MANDATES", "neo4j-node-139"),
        ("SEC-SOC-005", "AWS KMS Dedicated HSM Envelope", "SUBSTANTIATES", "neo4j-node-140"),
    ]
    cur.executemany("""
    INSERT INTO knowledge_graph_nodes (source_clause, target_fact, relationship_type, neo4j_node_id)
    VALUES (?,?,?,?)
    """, knowledge_graph)

    # 4. visual_asset_tokens (30 rows)
    asset_tokens = [
        ("Brand Primary Indigo", "#4F46E5", 2.0, 85.0, "79,70,229", "39.8,45.2,-68.9"),
        ("Brand Deep Indigo", "#4338CA", 2.5, 90.0, "67,56,202", "33.5,43.8,-66.1"),
        ("Brand Light Indigo", "#6366F1", 2.5, 75.0, "99,102,241", "50.2,38.1,-63.4"),
        ("Brand Surface White", "#FFFFFF", 1.0, 95.0, "255,255,255", "100.0,0.0,0.0"),
        ("Brand Canvas Neutral", "#FAFAFA", 1.5, 90.0, "250,250,250", "98.2,0.0,0.0"),
        ("Brand Border Subdued", "#E4E4E7", 2.0, 45.0, "228,228,231", "90.7,0.3,-1.2"),
        ("Brand Zinc Headline", "#18181B", 2.0, 90.0, "24,24,27", "9.6,0.5,-1.6"),
        ("Brand Zinc Body", "#27272A", 2.0, 80.0, "39,39,42", "16.1,0.5,-1.7"),
        ("Brand Zinc Subdued", "#71717A", 3.0, 60.0, "113,113,122", "48.2,0.4,-4.1"),
        ("Brand Success Emerald", "#10B981", 3.0, 75.0, "16,185,129", "67.5,-53.2,19.8"),
        ("Brand Emerald Light", "#D1FAE5", 3.0, 40.0, "209,250,229", "95.1,-19.1,6.8"),
        ("Brand Warning Amber", "#F59E0B", 3.0, 65.0, "245,158,11", "71.2,25.4,75.1"),
        ("Brand Amber Light", "#FEF3C7", 3.0, 35.0, "254,243,199", "95.4,-2.2,22.1"),
        ("Brand Alert Rose", "#F43F5E", 3.0, 70.0, "244,63,94", "53.8,69.5,27.1"),
        ("Brand Rose Light", "#FFE4E6", 3.0, 35.0, "255,228,230", "92.1,11.2,3.1"),
        ("Brand Accent Purple", "#8B5CF6", 3.0, 75.0, "139,92,246", "51.2,49.2,-64.1"),
        ("Brand Accent Cyan", "#06B6D4", 3.0, 70.0, "6,182,212", "68.2,-31.2,-23.4"),
        ("Brand Accent Blue", "#2563EB", 2.5, 80.0, "37,99,235", "45.1,28.4,-72.1"),
        ("Off-Palette Neon Yellow (Banned)", "#FBBF24", 5.0, 45.0, "251,191,36", "80.1,12.5,78.2"),
        ("Off-Palette Dull Gray (Banned)", "#A1A1AA", 4.0, 40.0, "161,161,170", "67.1,0.5,-4.0"),
        ("Brand Navy Slate", "#0F172A", 2.0, 95.0, "15,23,42", "7.8,1.2,-12.4"),
        ("Brand Slate Charcoal", "#1E293B", 2.0, 90.0, "30,41,59", "16.8,0.8,-12.1"),
        ("Brand Slate Muted", "#64748B", 2.5, 65.0, "100,116,139", "48.9,-1.2,-13.4"),
        ("Brand Slate Light", "#F1F5F9", 1.5, 20.0, "241,245,249", "96.4,-0.8,-2.4"),
        ("Secondary Gold Foil", "#D97706", 3.5, 75.0, "217,119,6", "58.2,31.4,65.2"),
        ("Digital Dark Surface", "#121214", 1.5, 95.0, "18,18,20", "6.5,0.4,-1.2"),
        ("Digital Card Dark", "#1F1F23", 2.0, 90.0, "31,31,35", "12.8,0.5,-1.8"),
        ("Packaging Spot Blue", "#1D4ED8", 2.0, 85.0, "29,78,216", "38.2,30.4,-70.8"),
        ("Packaging Safety Orange", "#EA580C", 3.0, 75.0, "234,88,12", "54.2,53.4,62.1"),
        ("High-Contrast Tag Yellow", "#FDE047", 3.5, 50.0, "253,224,71", "89.2,-5.4,75.2"),
    ]
    cur.executemany("""
    INSERT INTO visual_asset_tokens (asset_name, hex_color, allowed_delta, min_apca_contrast, rgb_coords, cielab_coords)
    VALUES (?,?,?,?,?,?)
    """, asset_tokens)

    # 5. channel_policies (10 rows)
    channels = [
        ("LinkedIn", 3000, "rockstar,ninja,cheap,growth hacking,unrivaled", "*Based on Q4-2026 internal benchmark N=1247", "1.91:1", "Enterprise B2B Decision Makers", "high"),
        ("X", 280, "disrupting,game-changing,synergy,move the needle,pivot", "*Terms apply. See omniguard.ai/legal", "16:9", "Fast-moving Tech & Growth audience", "critical"),
        ("Instagram", 2200, "dm for price,link in bio to buy,cheap,free money", "#Sponsored or #Ad if commercial partner", "1:1", "Visual Creators & Design Community", "medium"),
        ("Press Release", 8000, "groundbreaking,miracle,unprecedented,guaranteed", "Forward-looking statements disclaimer applies.", "16:9", "Financial Media & Industry Analysts", "critical"),
        ("TikTok", 150, "link in bio,guarantee 100%,free trial forever", "Paid Partnership toggle required for paid ads", "9:16", "Gen-Z & Digital Creators", "medium"),
        ("YouTube Shorts", 200, "smash that like button,unlimited profit", "Paid promotion disclosure mandatory", "9:16", "Video Audience", "medium"),
        ("Email Newsletter", 5000, "free,act now,no obligation,miracle", "Unsubscribe link and physical company address mandatory per CAN-SPAM", "1:1", "Opt-in Subscribers & Customers", "high"),
        ("Packaging Print", 1200, "pure,100% organic without cert,toxic-free", "Net weight, ingredients, and batch barcode mandatory", "Custom Die-Cut", "Retail Consumers", "critical"),
        ("Out-of-Home Billboard", 120, "unrivaled,cheap,guaranteed,disruptive", "OmniGuard registered trademark and URL mandatory", "14:48", "Commuters & Vehicular Traffic", "critical"),
        ("Google Ads", 90, "the best,world #1,cheap,miracle", "Trademarks cannot appear in ad text without proof", "Responsive Search", "High-intent Searchers", "high"),
    ]
    cur.executemany("""
    INSERT INTO channel_policies (channel_name, max_char_count, forbidden_words, required_disclaimers, aspect_ratio, target_audience, strictness_level)
    VALUES (?,?,?,?,?,?,?)
    """, channels)

    # 10. brand_assets (18 rows)
    brand_assets_data = [
        ("Primary Horizontal Logo (SVG)", "vector_logo", "/assets/logos/omniguard-primary.svg", "Design Operations", "4.2"),
        ("Secondary Wordmark White (SVG)", "vector_logo", "/assets/logos/omniguard-wordmark-white.svg", "Design Operations", "4.2"),
        ("Monochrome Icon Mark (SVG)", "vector_icon", "/assets/logos/omniguard-icon.svg", "Design Operations", "4.2"),
        ("Inter Display Typeface Package", "typography", "/assets/fonts/inter-display.woff2", "Legal Review Board", "1.0"),
        ("JetBrains Mono Code Typeface", "typography", "/assets/fonts/jetbrains-mono.woff2", "Legal Review Board", "1.0"),
        ("Brand Color Token JSON Schema", "design_tokens", "/assets/tokens/brand-tokens.json", "Design Operations", "3.0"),
        ("Executive Headshot Brand Director", "photography", "/assets/team/brand-director.jpg", "Content Operations", "2.1"),
        ("Executive Headshot General Counsel", "photography", "/assets/team/general-counsel.jpg", "Content Operations", "2.1"),
        ("Executive Headshot Chief Architect", "photography", "/assets/team/chief-architect.jpg", "Content Operations", "2.1"),
        ("Executive Headshot Content Operations", "photography", "/assets/team/content-ops.jpg", "Content Operations", "2.1"),
        ("Enterprise Architecture Diagram", "illustration", "/assets/diagrams/enterprise-pipeline.svg", "Architecture Team", "3.0"),
        ("Qdrant & Neo4j Hybrid Flowchart", "illustration", "/assets/diagrams/qdrant-neo4j-hybrid.svg", "Design Operations", "2.0"),
        ("Packaging Die-Cut Template 500ml", "print_template", "/assets/templates/pack-500ml.ai", "Design Operations", "1.2"),
        ("Social Media LinkedIn Banner 1200x628", "social_template", "/assets/social/linkedin-hero.fig", "Legal Review Board", "2.4"),
        ("X / Twitter Header Template 1500x500", "social_template", "/assets/social/x-header.fig", "Legal Review Board", "2.4"),
        ("PR Newswire Standard Boilerplate", "legal_template", "/assets/legal/pr-boilerplate.txt", "Legal Review Board", "4.0"),
        ("SOC 2 Type II Compliance Badge", "badge", "/assets/badges/soc2-type-2.svg", "Architecture Team", "2026"),
        ("WCAG 2.2 AA Perceptual Contrast Stamp", "badge", "/assets/badges/wcag-22-aa.svg", "Architecture Team", "2.2"),
    ]
    cur.executemany("""
    INSERT INTO brand_assets (asset_title, asset_type, file_path, approved_by, version)
    VALUES (?,?,?,?,?)
    """, brand_assets_data)

    # 11. team_roles (8 rows)
    roles_data = [
        ("content_creator", "Content Operations", "Draft, Edit, Apply Patches", 0),
        ("brand_lead", "Design Operations", "Brand Strategy, Visual Tokens, Rule Ingestion", 1),
        ("brand_manager", "Design Operations", "Campaign Approvals & Tone Drift Governance", 1),
        ("compliance_officer", "Legal Review Board", "Risk Assessment, Disclaimers, Provenance Verification", 1),
        ("legal_counsel", "Legal Review Board", "Statutory Claim Validation & Final Certifications", 1),
        ("systems_engineer", "Architecture Team", "FastAPI, Vector Pipelines & RBAC Access", 1),
        ("full_stack_integrator", "Content Operations", "Pipeline Deployments & QA Validation", 0),
        ("system", "OmniGuard Autonomous Worker", "Automated Policy Checks & Proof Hash Generation", 1),
    ]
    cur.executemany("""
    INSERT INTO team_roles (role_name, user_name, permission_level, can_approve)
    VALUES (?,?,?,?)
    """, roles_data)

    # 6. audit_logs (30 rows)
    sample_audits = [
        ("LinkedIn", "Our platform guarantees 100% brand compliance and reduces violations by 99.7% with zero effort. We are the unrivaled, industry-leading leader across every enterprise market.", 58.0, "pass", "fail", "pass", "pass", _ts(120)),
        ("X", "We're disrupting the brand compliance landscape! Our AI leverages game-changing synergy to move the needle and pivot your workflows in record time. #Innovation", 62.0, "fail", "pass", "pass", "pass", _ts(110)),
        ("Press Release", "OmniGuard AI: Intelligent Brand Governance designed for forward-thinking modern creative teams.", 68.0, "pass", "pass", "fail", "fail", _ts(95)),
        ("LinkedIn", "OmniGuard AI helps enterprise organizations achieve up to 94% brand compliance across remote teams.* Powered by proprietary ML models.", 94.0, "pass", "pass", "pass", "pass", _ts(80)),
        ("X", "Streamline your brand review cycles by 70% with intelligent automated micro-patches. *Details: omniguard.ai/legal", 96.0, "pass", "pass", "pass", "pass", _ts(70)),
        ("Instagram", "Clean palettes, verified claims, and instant brand compliance for modern design teams. #BrandGovernance #DesignSystems", 92.0, "pass", "pass", "pass", "pass", _ts(60)),
        ("Press Release", "OmniGuard AI Announces General Availability of Explainable Brand Governance Firewall for Enterprise Marketing Teams.", 98.0, "pass", "pass", "pass", "pass", _ts(55)),
        ("TikTok", "How we audit 1,000 brand assets in 4 seconds with zero human burnout! Check out OmniGuard AI in action.", 88.0, "pass", "pass", "pass", "pass", _ts(50)),
        ("Email Newsletter", "Exclusive Q4 Report: Why 82% of CMOs are adopting automated pre-publication governance firewalls.", 95.0, "pass", "pass", "pass", "pass", _ts(45)),
        ("Packaging Print", "OmniGuard Hardware Enclosure v2: Precision-crafted with certified non-toxic coatings and recyclable alloys.", 91.0, "pass", "pass", "pass", "pass", _ts(40)),
        ("Out-of-Home Billboard", "Brand compliance that moves at the speed of culture. OmniGuard.ai", 97.0, "pass", "pass", "pass", "pass", _ts(35)),
        ("Google Ads", "Automate Brand Compliance | Reduce Review Cycles by 70% | Enterprise-Grade SOC 2 Certified", 94.0, "pass", "pass", "pass", "pass", _ts(30)),
        ("LinkedIn", "Are off-brand colors and unverified claims slowing your product launches? Discover how OmniGuard automates approval workflows.", 90.0, "pass", "pass", "pass", "pass", _ts(28)),
        ("X", "Stop manual brand reviews. Start intelligent pre-publication governance with OmniGuard AI. #Governance #AI", 93.0, "pass", "pass", "pass", "pass", _ts(25)),
        ("Press Release", "OmniGuard AI Achieves SOC 2 Type II Certification, Validating Highest Standards for Enterprise Content Security.", 100.0, "pass", "pass", "pass", "pass", _ts(20)),
        ("LinkedIn", "Guaranteed zero errors on any post you ever write! The ultimate brand shield for growth hackers.", 50.0, "fail", "fail", "pass", "pass", _ts(18)),
        ("X", "Pivot your growth strategy with disruptive AI synergy that blows competitors out of the water!", 55.0, "fail", "fail", "pass", "pass", _ts(16)),
        ("Instagram", "Our yellow on beige text is super aesthetic, tap bio to shop!", 52.0, "pass", "pass", "fail", "fail", _ts(14)),
        ("LinkedIn", "Trusted by Fortune 500 brands to enforce tonal and visual consistency across distributed content creation.", 92.0, "pass", "pass", "pass", "pass", _ts(12)),
        ("Press Release", "OmniGuard AI Integrates with Qdrant Vector Database and Neo4j Knowledge Graph to Eliminate Black-Box AI Hallucinations.", 99.0, "pass", "pass", "pass", "pass", _ts(10)),
        ("YouTube Shorts", "Watch how RFC 6902 micro-patches fix marketing copy in real-time without overriding author voice!", 94.0, "pass", "pass", "pass", "pass", _ts(8)),
        ("Email Newsletter", "Your monthly governance digest: Top flagged corporate buzzwords and how to replace them with impactful verbs.", 93.0, "pass", "pass", "pass", "pass", _ts(7)),
        ("Packaging Print", "Warning: Contains unverified claims regarding 100% organic carbon neutrality.", 58.0, "pass", "fail", "pass", "pass", _ts(6)),
        ("Out-of-Home Billboard", "The cheapest compliance software on earth guaranteed!", 45.0, "fail", "fail", "pass", "pass", _ts(5)),
        ("Google Ads", "World #1 Brand Platform | Miracle Results in 2 Days", 48.0, "fail", "fail", "pass", "pass", _ts(4)),
        ("LinkedIn", "Empower your creators with non-blocking feedback during drafting. OmniGuard AI provides instant line-by-line checks.", 95.0, "pass", "pass", "pass", "pass", _ts(3)),
        ("X", "Preserve creator intent with atomic RFC 6902 JSON micro-patches. No hallucinations, just compliant brand consistency.", 97.0, "pass", "pass", "pass", "pass", _ts(2)),
        ("Press Release", "CodeNexus Hackathon Selects OmniGuard AI (Enterprise Compliance Office) for Round 2 Enterprise Brand Governance Showcase.", 100.0, "pass", "pass", "pass", "pass", _ts(1)),
        ("Instagram", "Beautiful typography, validated color tokens, and guaranteed WCAG 2.2 AA contrast in every creative.", 96.0, "pass", "pass", "pass", "pass", _ts(1)),
        ("LinkedIn", "Our platform helps enterprise teams reduce brand review cycles by over 70% while maintaining 100% human-in-the-loop oversight.", 98.0, "pass", "pass", "pass", "pass", _ts(0)),
    ]
    cur.executemany("""
    INSERT INTO audit_logs (channel, draft_text, compliance_score, tone_status, claim_status, color_status, contrast_status, created_at)
    VALUES (?,?,?,?,?,?,?,?)
    """, sample_audits)

    # 7. micro_patches (35 rows)
    patches = [
        (1, "critical", "Clause 3.2: Absolute 100% guarantee is legally unsubstantiated", "CLM-Q4-FC-019", "guarantees 100% brand compliance", "helps achieve up to 94% brand compliance*", 1),
        (1, "high", "Superlative 'unrivaled' requires third-party analyst citation", "CLM-Q4-FC-028", "unrivaled, industry-leading leader", "trusted enterprise platform", 1),
        (2, "critical", "Clause 4.1: Prohibited buzzword 'disrupting'", "TON-GLO-009", "We're disrupting", "We're transforming", 1),
        (2, "high", "Clause 4.1: Prohibited buzzword 'synergy'", "TON-GLO-009", "game-changing synergy", "unified workflows", 1),
        (2, "high", "Clause 4.1: Prohibited buzzword 'move the needle'", "TON-GLO-009", "move the needle", "accelerate results", 1),
        (3, "critical", "APCA Contrast score Lc=11.2 fails WCAG 2.2 AA requirement Lc >= 75", "A11Y-STD-001", "#FBBF24 on #FFFBEB", "#18181B on #FFFBEB", 1),
        (3, "high", "Detected color #FBBF24 exceeds allowed Delta-E 3.0 from Brand Primary", "MBG-4.2-CL-008", "#FBBF24", "#4F46E5", 1),
        (16, "critical", "Prohibited absolute claim 'guaranteed zero errors'", "CLM-Q4-FC-019", "Guaranteed zero errors on any post you ever write!", "Helps prevent high-risk brand violations*", 0),
        (16, "high", "Prohibited slang 'growth hackers' in enterprise context", "TON-GLO-001", "growth hackers", "modern marketing teams", 0),
        (17, "high", "Prohibited buzzwords 'pivot' and 'synergy'", "TON-GLO-009", "Pivot your growth strategy with disruptive AI synergy", "Modernize your brand strategy with intelligent automation", 0),
        (17, "medium", "Informal aggressive tone 'blows competitors out of the water'", "TON-GLO-006", "blows competitors out of the water!", "delivers measurable competitive advantage.", 0),
        (18, "critical", "APCA contrast Lc=14.5 fails accessibility spec", "A11Y-STD-001", "yellow on beige text", "high-contrast text", 0),
        (23, "critical", "Unsubstantiated organic carbon neutrality claim", "CLM-Q4-FC-001", "100% organic carbon neutrality", "certified sustainable sourcing*", 0),
        (24, "critical", "Prohibited word 'cheapest' in OOH media", "TON-GLO-004", "The cheapest compliance software on earth", "Leading enterprise brand governance platform", 0),
        (25, "critical", "Prohibited superlatives 'World #1' and 'Miracle'", "CLM-Q4-FC-028", "World #1 Brand Platform | Miracle Results", "Top Enterprise Brand Platform | Proven Results", 0),
        (1, "medium", "Missing mandatory asterisk footnote on statistical claim", "SOC-SPD-005", "99.7% with zero effort", "up to 94% with automated guardrails*", 1),
        (4, "low", "Missing trademark symbol on first mention", "MBG-4.2-CL-014", "OmniGuard AI", "OmniGuard® AI", 1),
        (5, "low", "Minor formatting recommendation for link brevity", "SOC-SPD-001", "omniguard.ai/legal", "omniguard.ai/tc", 1),
        (6, "low", "Add primary brand hashtag #OmniGuard", "SOC-SPD-005", "#DesignSystems", "#OmniGuard #DesignSystems", 1),
        (7, "low", "Add date stamp to headline boilerplate", "PR-EXE-001", "FOR IMMEDIATE RELEASE", "FOR IMMEDIATE RELEASE — Q4 2026", 1),
        (8, "low", "Add audio safety note to video description", "MOT-VID-002", "Check out OmniGuard AI", "Check out OmniGuard AI [Audio Described]", 1),
        (9, "low", "Clarify CMO survey sample cohort", "CLM-Q4-FC-003", "82% of CMOs", "82% of CMOs (N=340)", 1),
        (10, "medium", "Add recyclability resin code indicator", "PKG-PRT-003", "recyclable alloys", "recyclable alloys (Class 1)", 1),
        (11, "low", "Format URL with HTTPS prefix", "OOH-LEG-001", "OmniGuard.ai", "https://omniguard.ai", 1),
        (12, "low", "Standardize uppercase acronym in headline", "DEV-API-001", "soc 2", "SOC 2 Type II", 1),
        (13, "medium", "Add footnote for ROI timeline estimation", "CLM-Q4-FC-035", "automates approval workflows", "automates approval workflows (avg. 4.2 min)", 1),
        (14, "low", "Append official campaign tag", "SOC-SPD-005", "#AI", "#AI #OmniGuard", 1),
        (15, "low", "Include auditor firm name in sub-headline", "SEC-SOC-002", "Achieves SOC 2", "Achieves SOC 2 (Audited by BDO)", 1),
        (19, "medium", "Add analyst citation date to Fortune 500 metric", "CLM-Q4-FC-028", "Fortune 500 brands", "Fortune 500 brands (2026 Cohort)", 1),
        (20, "low", "Spell out Hybrid Architecture taxonomy", "DEV-API-004", "Qdrant Vector Database", "Qdrant Vector Database (384-dim)", 1),
        (21, "low", "Add RFC 6902 specification reference link", "GOV-TAG-001", "RFC 6902 micro-patches", "RFC 6902 JSON micro-patches", 1),
        (22, "low", "Add call-to-action button descriptor", "CRM-EML-003", "how to replace them", "explore compliant alternatives", 1),
        (26, "low", "Refine line-by-line feedback wording", "TON-GLO-001", "line-by-line checks", "contextual inline guardrails", 1),
        (27, "low", "Add license notice to open-source schema", "DEV-API-001", "JSON micro-patches", "Apache 2.0 JSON micro-patches", 1),
        (28, "low", "Add CodeNexus official event tag", "PR-EXE-001", "Round 2 Enterprise", "Round 2 Enterprise (CodeNexus 2026)", 1),
    ]
    cur.executemany("""
    INSERT INTO micro_patches (audit_id, severity, issue_description, guideline_clause, original_snippet, patched_snippet, patch_applied)
    VALUES (?,?,?,?,?,?,?)
    """, patches)

    # 8. review_history (45 rows)
    reviews = [
        (1, "content_creator", "revision_requested", "Flags noted. Requesting legal guidance on substantiated claims.", _ts(118)),
        (1, "legal_counsel", "approved", "Approved pending addition of benchmark asterisk and removal of superlative.", _ts(115)),
        (1, "brand_manager", "approved", "Applied RFC 6902 micro-patches. Copy is now ready for LinkedIn.", _ts(112)),
        (2, "content_creator", "revision_requested", "Submitted draft with enthusiasm, tone scanner flagged buzzwords.", _ts(108)),
        (2, "brand_lead", "approved", "Substituted jargon with active outcome verbs. Approved for X release.", _ts(105)),
        (3, "content_creator", "escalated", "Visual contrast alert triggered on press release hero image.", _ts(92)),
        (3, "brand_manager", "approved", "Swapped foreground to Zinc-900, APCA contrast restored to Lc=88.4.", _ts(89)),
        (4, "content_creator", "approved", "Initial draft prepared with substantiated asterisks.", _ts(78)),
        (4, "brand_lead", "auto_approved", "All 4 multi-modal guardrails passed (Score: 94%). Auto-approved.", _ts(77)),
        (5, "content_creator", "approved", "Verified under 280 char count budget on X.", _ts(68)),
        (5, "brand_manager", "auto_approved", "Passed tone, claims, and brevity policies. Auto-certified.", _ts(67)),
        (6, "content_creator", "approved", "Instagram square creative copy matches visual guidelines.", _ts(59)),
        (6, "brand_lead", "approved", "Verified visual hashtag and design system guidelines.", _ts(58)),
        (7, "legal_counsel", "approved", "Official PR Newswire announcement meets all disclosure requirements.", _ts(53)),
        (7, "compliance_officer", "approved", "Full audit log sealed with SHA-256 provenance hash.", _ts(52)),
        (8, "content_creator", "approved", "TikTok caption compliant with paid partnership transparency.", _ts(48)),
        (9, "brand_manager", "approved", "Email newsletter copy and preheader approved for staging blast.", _ts(43)),
        (10, "compliance_officer", "approved", "Packaging print run specifications certified compliant with EU REACH.", _ts(38)),
        (11, "brand_lead", "approved", "Billboard headline legibility tested at 50ft scale. Clear.", _ts(33)),
        (12, "brand_manager", "approved", "Google Ad copy strictly within 90-char budget. Approved.", _ts(28)),
        (13, "content_creator", "approved", "Draft verified against master brand identity rules.", _ts(26)),
        (14, "brand_lead", "approved", "Concise, impactful, active verbs. Approved.", _ts(23)),
        (15, "legal_counsel", "approved", "SOC 2 announcement thoroughly substantiated by October 2026 report.", _ts(19)),
        (16, "legal_counsel", "rejected", "Rejected: Unsubstantiated 100% guarantee creates major liability.", _ts(17)),
        (17, "brand_lead", "rejected", "Rejected: Excessive buzzword density contradicts warm, expert pillar.", _ts(15)),
        (18, "compliance_officer", "rejected", "Rejected: Fails WCAG 2.2 AA accessibility requirements (APCA < 75).", _ts(13)),
        (19, "brand_manager", "approved", "Verified B2B enterprise copy. Approved.", _ts(11)),
        (20, "systems_engineer", "approved", "Architectural press release verified technically accurate.", _ts(9)),
        (21, "content_creator", "approved", "RFC 6902 educational video script reviewed and approved.", _ts(7)),
        (22, "brand_lead", "approved", "Monthly digest copy approved for newsletter subscriber list.", _ts(6)),
        (23, "legal_counsel", "rejected", "Rejected: Carbon neutrality claim lacks ISO 14064 certification.", _ts(5)),
        (24, "brand_manager", "rejected", "Rejected: 'Cheapest' violates enterprise luxury positioning guidelines.", _ts(4)),
        (25, "compliance_officer", "rejected", "Rejected: 'Miracle' violates advertising standards truth-in-advertising.", _ts(3)),
        (26, "content_creator", "approved", "Creator workflow hero post approved.", _ts(2)),
        (27, "brand_lead", "approved", "Verified intent-preserving micro-patch explanation. Approved.", _ts(1)),
        (28, "legal_counsel", "approved", "CodeNexus Round 2 hackathon submission approved for syndication.", _ts(1)),
        (28, "compliance_officer", "approved", "Cryptographic provenance verified for Round 2 presentation.", _ts(1)),
        (29, "brand_manager", "approved", "Instagram accessibility showcase creative approved.", _ts(0)),
        (30, "brand_lead", "approved", "Human-in-the-loop oversight message approved for CMO syndicate.", _ts(0)),
        (1, "systems_engineer", "approved", "Hash integrity verified on database sync.", _ts(111)),
        (2, "systems_engineer", "approved", "X API integration tests passed.", _ts(104)),
        (3, "systems_engineer", "approved", "OpenCV color extraction metrics validated against token library.", _ts(88)),
        (4, "compliance_officer", "approved", "Compliance certificate generated and stored in SQLite.", _ts(76)),
        (5, "compliance_officer", "approved", "Cryptographic tag sealed.", _ts(66)),
        (7, "brand_manager", "approved", "PR Newswire final release approved by executive team.", _ts(51)),
    ]
    cur.executemany("""
    INSERT INTO review_history (audit_id, reviewer_role, action_taken, comment, timestamp)
    VALUES (?,?,?,?,?)
    """, reviews)

    # 12. compliance_certificates (15 rows)
    certificates = [
        (4, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0004-VERIFIED')}", _ts(76), "brand_lead (Principal Brand Director)"),
        (5, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0005-VERIFIED')}", _ts(66), "brand_manager (Enterprise Brand Governance)"),
        (6, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0006-VERIFIED')}", _ts(58), "brand_lead (Principal Brand Director)"),
        (7, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0007-VERIFIED')}", _ts(51), "legal_counsel (Office of General Counsel)"),
        (8, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0008-VERIFIED')}", _ts(47), "compliance_officer (Regulatory Compliance Officer)"),
        (9, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0009-VERIFIED')}", _ts(42), "brand_manager (Enterprise Brand Governance)"),
        (10, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0010-VERIFIED')}", _ts(37), "compliance_officer (Regulatory Compliance Officer)"),
        (11, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0011-VERIFIED')}", _ts(32), "brand_lead (Principal Brand Director)"),
        (12, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0012-VERIFIED')}", _ts(27), "brand_manager (Enterprise Brand Governance)"),
        (13, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0013-VERIFIED')}", _ts(25), "brand_lead (Principal Brand Director)"),
        (14, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0014-VERIFIED')}", _ts(22), "brand_lead (Principal Brand Director)"),
        (15, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0015-VERIFIED')}", _ts(19), "legal_counsel (Office of General Counsel)"),
        (20, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0020-VERIFIED')}", _ts(8), "systems_engineer (Platform Security Architect)"),
        (28, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0028-HACKATHON-R2')}", _ts(1), "legal_counsel (Office of General Counsel)"),
        (30, f"urn:omniguard:sha256:{_sha256('OMNI-CERT-0030-VERIFIED')}", _ts(0), "brand_lead (Principal Brand Director)"),
    ]
    cur.executemany("""
    INSERT INTO compliance_certificates (audit_id, certificate_hash, issued_at, signer_role)
    VALUES (?,?,?,?)
    """, certificates)

    # 13. apca_contrast_checks (30 rows)
    apca_checks = [
        (1, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (2, "#18181B", "#FAFAFA", 89.2, "pass"),
        (3, "#FBBF24", "#FFFBEB", 11.2, "fail"),
        (4, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (5, "#18181B", "#FAFAFA", 89.2, "pass"),
        (6, "#FFFFFF", "#4338CA", 91.5, "pass"),
        (7, "#18181B", "#FFFFFF", 98.4, "pass"),
        (8, "#FFFFFF", "#18181B", 98.4, "pass"),
        (9, "#27272A", "#FFFFFF", 92.1, "pass"),
        (10, "#FFFFFF", "#0F172A", 99.1, "pass"),
        (11, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (12, "#18181B", "#FAFAFA", 89.2, "pass"),
        (13, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (14, "#18181B", "#FFFFFF", 98.4, "pass"),
        (15, "#18181B", "#FFFFFF", 98.4, "pass"),
        (16, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (17, "#18181B", "#FAFAFA", 89.2, "pass"),
        (18, "#FDE047", "#FEF3C7", 14.5, "fail"),
        (19, "#FFFFFF", "#4338CA", 91.5, "pass"),
        (20, "#18181B", "#FFFFFF", 98.4, "pass"),
        (21, "#FFFFFF", "#18181B", 98.4, "pass"),
        (22, "#27272A", "#FFFFFF", 92.1, "pass"),
        (23, "#FFFFFF", "#0F172A", 99.1, "pass"),
        (24, "#FBBF24", "#FFFBEB", 11.2, "fail"),
        (25, "#FBBF24", "#FFFFFF", 22.4, "fail"),
        (26, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (27, "#18181B", "#FAFAFA", 89.2, "pass"),
        (28, "#FFFFFF", "#4F46E5", 88.4, "pass"),
        (29, "#FFFFFF", "#4338CA", 91.5, "pass"),
        (30, "#FFFFFF", "#4F46E5", 88.4, "pass"),
    ]
    cur.executemany("""
    INSERT INTO apca_contrast_checks (audit_id, fg_hex, bg_hex, apca_score, wcag_status)
    VALUES (?,?,?,?,?)
    """, apca_checks)

    # 14. opencv_color_deltas (30 rows)
    deltas = [
        (1, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (2, "#FAFAFA", "Brand Canvas Neutral", 0.0, 1),
        (3, "#FBBF24", "Brand Primary Indigo", 7.8, 0),
        (4, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (5, "#18181B", "Brand Zinc Headline", 0.0, 1),
        (6, "#4338CA", "Brand Deep Indigo", 0.0, 1),
        (7, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (8, "#18181B", "Brand Zinc Headline", 0.0, 1),
        (9, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (10, "#0F172A", "Brand Navy Slate", 0.0, 1),
        (11, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (12, "#18181B", "Brand Zinc Headline", 0.0, 1),
        (13, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (14, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (15, "#18181B", "Brand Zinc Headline", 0.0, 1),
        (16, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (17, "#FAFAFA", "Brand Canvas Neutral", 0.0, 1),
        (18, "#FDE047", "Brand Warning Amber", 6.2, 0),
        (19, "#4338CA", "Brand Deep Indigo", 0.0, 1),
        (20, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (21, "#18181B", "Brand Zinc Headline", 0.0, 1),
        (22, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (23, "#0F172A", "Brand Navy Slate", 0.0, 1),
        (24, "#FBBF24", "Brand Primary Indigo", 7.8, 0),
        (25, "#FBBF24", "Brand Primary Indigo", 7.8, 0),
        (26, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (27, "#FAFAFA", "Brand Canvas Neutral", 0.0, 1),
        (28, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
        (29, "#4338CA", "Brand Deep Indigo", 0.0, 1),
        (30, "#4F46E5", "Brand Primary Indigo", 0.0, 1),
    ]
    cur.executemany("""
    INSERT INTO opencv_color_deltas (audit_id, detected_hex, target_token, delta_e, is_compliant)
    VALUES (?,?,?,?,?)
    """, deltas)

    # 9. guideline_analytics (30 rows)
    analytics_data = [
        ("TON-GLO-009", 84, 1, _ts(1)),
        ("CLM-Q4-FC-019", 68, 0, _ts(2)),
        ("A11Y-STD-001", 52, 0, _ts(3)),
        ("MBG-4.2-CL-008", 44, 0, _ts(4)),
        ("CLM-Q4-FC-028", 39, 1, _ts(5)),
        ("SOC-SPD-001", 35, 1, _ts(6)),
        ("MBG-4.2-CL-001", 31, 0, _ts(8)),
        ("CLM-Q4-FC-001", 28, 0, _ts(10)),
        ("TON-GLO-004", 24, 0, _ts(12)),
        ("A11Y-STD-004", 21, 0, _ts(15)),
        ("MBG-4.2-CL-014", 19, 1, _ts(18)),
        ("CLM-Q4-FC-012", 17, 0, _ts(20)),
        ("PKG-PRT-003", 15, 0, _ts(25)),
        ("PRT-LIC-002", 13, 0, _ts(30)),
        ("GOV-TAG-001", 12, 0, _ts(35)),
        ("GDPR-EU-004", 10, 0, _ts(40)),
        ("SEC-SOC-002", 9, 0, _ts(45)),
        ("IR-FIN-001", 8, 1, _ts(50)),
        ("CRM-EML-003", 8, 0, _ts(55)),
        ("HR-REC-002", 7, 0, _ts(60)),
        ("DEV-API-001", 6, 0, _ts(70)),
        ("OOH-LEG-001", 6, 0, _ts(80)),
        ("INF-AMB-003", 5, 0, _ts(90)),
        ("MOT-VID-002", 5, 0, _ts(100)),
        ("MBG-4.2-CL-002", 4, 0, _ts(110)),
        ("CLM-Q4-FC-007", 4, 0, _ts(120)),
        ("TON-GLO-001", 3, 0, _ts(130)),
        ("A11Y-STD-007", 3, 0, _ts(140)),
        ("SOC-SPD-005", 2, 0, _ts(150)),
        ("SEC-SOC-005", 1, 0, _ts(160)),
    ]
    cur.executemany("""
    INSERT INTO guideline_analytics (clause_citation, violation_count, ambiguity_flag, last_triggered)
    VALUES (?,?,?,?)
    """, analytics_data)

    conn.commit()
    conn.close()
    print("[OK] OmniGuard enterprise database initialized with 15 tables and expanded datasets!")

if __name__ == "__main__":
    init_database()
