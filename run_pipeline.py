import os
import subprocess

root = r"C:\Users\swast\OneDrive\Desktop\vercel"

# 1. Create the dedicated route files
routes = ["scanner", "guidelines", "governance", "analytics", "graph"]
for base in [r"share\v0-project\app", r"frontend\app"]:
    for i, r in enumerate(routes, 1):
        rdir = os.path.join(root, base, r)
        os.makedirs(rdir, exist_ok=True)
        rfile = os.path.join(rdir, "page.tsx")
        with open(rfile, "w", encoding="utf-8") as f:
            f.write(f'''"use client"

import OmniGuardEnterpriseApp from '../page'

export default function {r.capitalize()}RoutePage() {{
  return <OmniGuardEnterpriseApp initialTab={{{i}}} />
}}
''')
        print("Created route page:", rfile)

# 2. Run scripts
cmds = [
    ["node", "scratch/commercialize_complete.js"],
    ["node", "scratch/inject_enterprise_fallbacks.js"],
    ["uv", "run", "python", "scratch/add_audits_endpoint.py"],
    ["node", "scratch/add_micro_polish.js"],
    ["uv", "run", "python", "scratch/fix_endpoints.py"],
    ["uv", "run", "python", "scratch/fix_status.py"],
    ["uv", "run", "python", "scratch/apply_dedicated_pages.py"],
    ["uv", "run", "python", "scratch/inject_swish_animations.py"],
    ["uv", "run", "python", "backend/init_db.py"],
]

for cmd in cmds:
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error output:", res.stderr)
    else:
        print("Output:", res.stdout.strip()[:100])

print("\nPipeline complete!")
