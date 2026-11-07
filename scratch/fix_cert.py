# -*- coding: utf-8 -*-
from pathlib import Path

def main():
    target = Path(r"c:\Users\swast\OneDrive\Desktop\vercel\backend\main.py")
    text = target.read_text(encoding="utf-8")

    # Replace old compliance_certificates insert
    old_insert = """        cur_c = conn.execute(
            \"\"\"INSERT INTO compliance_certificates (audit_id, approved_by, status, ai_provenance_tag, timestamp)
               VALUES (?, 'OmniGuard Governance Engine', ?, ?, ?)\"\"\",
            (audit_id, status, prov_tag, ts),
        )"""

    new_insert = """        cur_c = conn.execute(
            \"\"\"INSERT INTO compliance_certificates (audit_id, certificate_hash, issued_at, signer_role)
               VALUES (?, ?, ?, 'OmniGuard Governance Engine')\"\"\",
            (audit_id, prov_tag, ts),
        )"""

    old_fields = """        "status": cert_dict["status"].upper(),
        "ai_provenance_tag": cert_dict["ai_provenance_tag"],
        "timestamp": cert_dict["timestamp"],
        "approved_by": cert_dict["approved_by"],"""

    new_fields = """        "status": "CERTIFIED",
        "ai_provenance_tag": cert_dict.get("certificate_hash", prov_tag),
        "timestamp": cert_dict.get("issued_at", ts),
        "approved_by": cert_dict.get("signer_role", "OmniGuard Governance Engine"),"""

    if old_insert in text:
        text = text.replace(old_insert, new_insert)
        print("Replaced insert")
    else:
        print("old_insert not matched")

    if old_fields in text:
        text = text.replace(old_fields, new_fields)
        print("Replaced fields")
    else:
        print("old_fields not matched")

    target.write_text(text, encoding="utf-8")
    print("Done")

if __name__ == "__main__":
    main()
