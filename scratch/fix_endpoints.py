import re

with open("backend/main.py", "r", encoding="utf-8") as f:
    c = f.read()

# 1. apply_patch
old_apply = '"message": "RFC 6902 patch applied successfully",'
new_apply = '"status": "success",\n            "applied": True,\n            "patch_applied": 1,\n            "message": "RFC 6902 patch applied successfully",'
c = c.replace(old_apply, new_apply, 1)

# 2. submit_review_action
old_review = 'return {\n        "message": f"Sign-off recorded:'
new_review = 'return {\n        "status": "success",\n        "id": latest_review.get("id"),\n        "message": f"Sign-off recorded:'
c = c.replace(old_review, new_review, 1)

# 3. image audit contrast & return keys
old_apca = 'apca_score = _apca_contrast("#FFFFFF", dominant_hex) if len(palette) == 1 else _apca_contrast(dominant_hex, secondary_hex)'
new_apca = 'apca_score = _apca_contrast(palette[0]["hex"], palette[1]["hex"]) if (len(palette) > 1 and _color_delta_e(palette[0]["hex"], palette[1]["hex"]) > 10.0) else _apca_contrast("#FFFFFF", dominant_hex)'
c = c.replace(old_apca, new_apca, 1)

old_ret = '"color_status": "pass" if color_pass else "fail",\n        "apca_score": round(apca_score, 1),\n        "contrast_status": "pass" if apca_pass else "fail",'
new_ret = '"color_status": "pass" if color_pass else "fail",\n        "delta_e_status": "pass" if color_pass else "fail",\n        "apca_score": round(apca_score, 1),\n        "contrast_status": "pass" if apca_pass else "fail",\n        "apca_status": "pass" if apca_pass else "fail",'
c = c.replace(old_ret, new_ret, 1)

with open("backend/main.py", "w", encoding="utf-8") as f:
    f.write(c)

print("backend/main.py successfully patched.")
