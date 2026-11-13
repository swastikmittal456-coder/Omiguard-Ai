test_script = r"C:\Users\swast\OneDrive\Desktop\vercel\scratch\run_round3_full_system_test.py"

with open(test_script, "r", encoding="utf-8") as f:
    c = f.read()

old_tables = '''    expected_tables = [
        "guidelines", "clauses", "vector_chunks", "graph_nodes", "graph_edges",
        "audits", "audit_violations", "micro_patches", "review_history",
        "provenance_registry", "api_keys", "governance_roles", "color_palettes",
        "analytics_aggregates", "audit_events", "policy_conflicts", "batch_campaign_audits"
    ]'''

new_tables = '''    expected_tables = [
        "apca_contrast_checks", "audit_logs", "batch_campaign_audits", "brand_assets",
        "channel_policies", "compliance_certificates", "guideline_analytics", "guidelines",
        "knowledge_graph_nodes", "micro_patches", "opencv_color_deltas", "policy_conflicts",
        "review_history", "rule_citations_map", "team_roles", "vector_chunks", "visual_asset_tokens"
    ]'''

if old_tables in c:
    c = c.replace(old_tables, new_tables)
    print("Updated expected_tables list!")

with open(test_script, "w", encoding="utf-8") as f:
    f.write(c)

print("Test script updated!")
