import sys
import os
sys.path.insert(0, r"C:\Users\swast\OneDrive\Desktop\vercel\backend")

import main as b
from fastapi.testclient import TestClient

client = TestClient(b.app)

# 1. Test conflicts
res_conflicts = client.get("/api/v1/guidelines/conflicts")
print("1. Conflicts status:", res_conflicts.status_code, "Total:", res_conflicts.json().get("total_conflicts"))
assert res_conflicts.status_code == 200

# 2. Test campaign matrix audit
res_campaign = client.post("/api/v1/campaigns/audit", json={"campaign_name": "Test Round 3 Campaign"})
print("2. Campaign status:", res_campaign.status_code, "Assets audited:", res_campaign.json().get("total_assets"))
assert res_campaign.status_code == 200

# 3. Test resolve conflict
res_resolve = client.post("/api/v1/guidelines/resolve-conflict", json={
    "conflict_id": 1,
    "resolution_strategy": "merge",
    "notes": "Harmonized via qualification clause."
})
print("3. Resolve status:", res_resolve.status_code, "Msg:", res_resolve.json().get("message"))
assert res_resolve.status_code == 200

# 4. Use 100% valid 100x100 PNG
valid_b64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAIAAAD/gAIDAAABXklEQVR4Ae3BMQEAAAABMMp59Q+ghwoC2GgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW1oBbehFdyGVnAbWsFtaAW3oRXchlZwG1rBbWgFt6EV3IZWcBtawW0KqUuUDSxQs/oAAAAASUVORK5CYII="

res_image = client.post("/api/v1/audit/image", json={
    "channel": "meta",
    "image_base64": valid_b64,
    "expected_primary_hex": "#4F46E5"
})
print("4. Image Audit status:", res_image.status_code, "Bounding boxes:", len(res_image.json().get("bounding_boxes", [])))
assert res_image.status_code == 200
assert len(res_image.json().get("bounding_boxes", [])) > 0

print("\n>>> ALL ROUND 3 BACKEND API TESTS PASSED! <<<")
