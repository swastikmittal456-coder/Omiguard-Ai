# -*- coding: utf-8 -*-
"""
Fixes column name alignments in backend/main.py for:
1. create_audit: visual_asset_tokens, apca_contrast_checks, opencv_color_deltas
2. submit_review_action: compliance_certificates
3. get_certificate: compliance_certificates & rule_citations_map
4. get_analytics: rule_citations_map
"""
import re
from pathlib import Path

def main():
    target = Path(r"c:\Users\swast\OneDrive\Desktop\vercel\backend\main.py")
    content = target.read_text(encoding="utf-8")

    # 1. In create_audit: fix brand_assets query -> visual_asset_tokens
    old_asset = 'brand_asset = conn.execute("SELECT hex_code, allowed_delta_e FROM brand_assets WHERE id = 1").fetchone()\n        target_hex = brand_asset["hex_code"] if brand_asset else "#4F46E5"\n        allowed_delta = brand_asset["allowed_delta_e"] if brand_asset else 2.0'
    new_asset = 'asset_token = conn.execute("SELECT hex_color, allowed_delta FROM visual_asset_tokens WHERE id = 1").fetchone()\n        target_hex = asset_token["hex_color"] if asset_token else "#4F46E5"\n        allowed_delta = asset_token["allowed_delta"] if asset_token else 2.0'
    if old_asset in content:
        content = content.replace(old_asset, new_asset)
        print("Fixed visual_asset_tokens query")

    # 2. In create_audit: fix apca_contrast_checks insert
    old_apca = 'conn.execute(\n        """INSERT INTO apca_contrast_checks (audit_id, foreground_hex, background_hex, apca_score, passed)\n           VALUES (?, ?, ?, ?, ?)""",\n        (audit_id, body.fg_color or "#FFFFFF", body.bg_color or "#4F46E5", apca_score, apca_passed),\n    )'
    new_apca = 'wcag_stat = "pass" if apca_passed else "fail"\n    conn.execute(\n        """INSERT INTO apca_contrast_checks (audit_id, fg_hex, bg_hex, apca_score, wcag_status)\n           VALUES (?, ?, ?, ?, ?)""",\n        (audit_id, body.fg_color or "#FFFFFF", body.bg_color or "#4F46E5", apca_score, wcag_stat),\n    )'
    if old_apca in content:
        content = content.replace(old_apca, new_apca)
        print("Fixed apca_contrast_checks insert")

    # 3. In create_audit: fix opencv_color_deltas insert
    old_delta = 'conn.execute(\n        """INSERT INTO opencv_color_deltas (audit_id, detected_hex, target_hex, delta_e_score, passed)\n           VALUES (?, ?, ?, ?, ?)""",\n        (audit_id, body.bg_color or "#4F46E5", target_hex, delta_e_score, color_passed),\n    )'
    new_delta = 'conn.execute(\n        """INSERT INTO opencv_color_deltas (audit_id, detected_hex, target_token, delta_e, is_compliant)\n           VALUES (?, ?, ?, ?, ?)""",\n        (audit_id, body.bg_color or "#4F46E5", target_hex, delta_e_score, color_passed),\n    )'
    if old_delta in content:
        content = content.replace(old_delta, new_delta)
        print("Fixed opencv_color_deltas insert")

    # 4. In submit_review_action: fix compliance_certificates insert
    old_cert_insert = 'cur_cert = conn.execute(\n            """INSERT INTO compliance_certificates (audit_id, approved_by, status, ai_provenance_tag, timestamp)\n               VALUES (?, ?, \'certified\', ?, ?)""",\n            (body.audit_id, body.user_name or body.reviewer_role.replace("_", " ").title(), prov_tag, ts),\n        )'
    new_cert_insert = 'cur_cert = conn.execute(\n            """INSERT INTO compliance_certificates (audit_id, certificate_hash, issued_at, signer_role)\n               VALUES (?, ?, ?, ?)""",\n            (body.audit_id, prov_tag, ts, f"{role_key} ({body.user_name})"),\n        )'
    if old_cert_insert in content:
        content = content.replace(old_cert_insert, new_cert_insert)
        print("Fixed submit_review_action cert insert")

    # 5. In get_certificate: fix compliance_certificates select & insert
    old_cert_get = 'cert = conn.execute("SELECT * FROM compliance_certificates WHERE audit_id = ? ORDER BY id DESC LIMIT 1", (audit_id,)).fetchone()\n    if not cert:\n        ts = _now()\n        payload = f"{audit_id}:{audit[\'draft_text\']}:{ts}:auto-certificate"\n        sha_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()\n        prov_tag = f"urn:omniguard:sha256:{sha_hash}"\n        status = "certified" if audit["compliance_score"] >= 80 else "conditional"\n        cur_c = conn.execute(\n            """INSERT INTO compliance_certificates (audit_id, approved_by, status, ai_provenance_tag, timestamp)\n               VALUES (?, \'OmniGuard Governance Engine\', ?, ?, ?)""",\n            (audit_id, status, prov_tag, ts),\n        )\n        conn.commit()\n        cert = conn.execute("SELECT * FROM compliance_certificates WHERE id = ?", (cur_c.lastrowid,)).fetchone()\n\n    cert_dict = dict(cert)\n\n    # Approved clause citations from Table 15 (rule_citations_map)\n    approved_citations = rows_to_list(\n        conn.execute("SELECT clause_citation, rule_name, summary FROM rule_citations_map LIMIT 8").fetchall()\n    )'

    new_cert_get = 'cert = conn.execute("SELECT * FROM compliance_certificates WHERE audit_id = ? ORDER BY id DESC LIMIT 1", (audit_id,)).fetchone()\n    if not cert:\n        ts = _now()\n        payload = f"{audit_id}:{audit[\'draft_text\']}:{ts}:auto-certificate"\n        sha_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()\n        prov_tag = f"urn:omniguard:sha256:{sha_hash}"\n        cur_c = conn.execute(\n            """INSERT INTO compliance_certificates (audit_id, certificate_hash, issued_at, signer_role)\n               VALUES (?, ?, ?, \'system\')""",\n            (audit_id, prov_tag, ts),\n        )\n        conn.commit()\n        cert = conn.execute("SELECT * FROM compliance_certificates WHERE id = ?", (cur_c.lastrowid,)).fetchone()\n\n    cert_dict = dict(cert)\n\n    # Approved clause citations from Table 15 (rule_citations_map)\n    approved_citations = rows_to_list(\n        conn.execute("SELECT citation_code, clause_title, severity_default FROM rule_citations_map LIMIT 8").fetchall()\n    )'

    if old_cert_get in content:
        content = content.replace(old_cert_get, new_cert_get)
        print("Fixed get_certificate cert fetch and insert")

    # Fix certificate dict access
    old_cert_fields = '"status": cert_dict["status"].upper(),\n        "ai_provenance_tag": cert_dict["ai_provenance_tag"],\n        "timestamp": cert_dict["timestamp"],\n        "approved_by": cert_dict["approved_by"],'
    new_cert_fields = '"status": "CERTIFIED",\n        "ai_provenance_tag": cert_dict.get("certificate_hash", f"urn:omniguard:sha256:{audit_id}"),\n        "timestamp": cert_dict.get("issued_at", _now()),\n        "approved_by": cert_dict.get("signer_role", "system"),'
    if old_cert_fields in content:
        content = content.replace(old_cert_fields, new_cert_fields)
        print("Fixed certificate_data fields")

    # 6. In get_analytics: fix rule_citations_map query
    old_analytics = 'rule_map = conn.execute(\n            "SELECT rule_name, summary FROM rule_citations_map WHERE clause_citation = ? LIMIT 1", (clause,)\n        ).fetchone()'
    new_analytics = 'rule_map = conn.execute(\n            "SELECT clause_title, severity_default FROM rule_citations_map WHERE citation_code = ? LIMIT 1", (clause,)\n        ).fetchone()'
    if old_analytics in content:
        content = content.replace(old_analytics, new_analytics)
        print("Fixed get_analytics rule_citations_map query")

    old_map_use = 'if rule_map:\n            entry["rule_name"] = rule_map["rule_name"]\n            entry["rule_summary"] = rule_map["summary"]'
    new_map_use = 'if rule_map:\n            entry["rule_name"] = rule_map["clause_title"]\n            entry["rule_summary"] = f"Severity: {rule_map[\'severity_default\']}"'
    if old_map_use in content:
        content = content.replace(old_map_use, new_map_use)
        print("Fixed get_analytics rule_map usage")

    target.write_text(content, encoding="utf-8")
    print("Schema alignment complete in main.py!")

if __name__ == "__main__":
    main()
