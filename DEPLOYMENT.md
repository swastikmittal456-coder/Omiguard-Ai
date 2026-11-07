# OmniGuard AI — Enterprise Pre-Publication Brand Governance Platform
**Team Name**: Team Layer 7  
**Hackathon**: CodeNexus Hackathon (Round 2 Submission)  
**Problem Statement**: Inkloom AI  

---

## 🚀 Quick Start (Local Development)

### 1. Start the FastAPI Backend (Port 8000)
```bash
cd backend
# With uv (recommended):
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Or with standard pip/python:
pip install -r requirements.txt
python init_db.py
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger API Docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/`

---

### 2. Start the Next.js Frontend (Port 3000)
```bash
cd share/v0-project   # or cd frontend
npm install
npm run dev
```
- Open browser: `http://localhost:3000`

---

## 🌐 1-Click Online Cloud Deployment

### Option A: Frontend on Vercel
1. Push this repository to GitHub.
2. In Vercel, click **"Add New Project"** and select the repository.
3. Set the **Root Directory** to `frontend` (or `share/v0-project`).
4. Under **Environment Variables**, add:
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-domain.up.railway.app
   ```
5. Click **Deploy**.

---

### Option B: Backend on Railway / Render / Fly.io
1. **Railway / Render**: Create a new Web Service from the repository.
2. Set Root Directory: `backend`
3. Start Command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Build Command:
   ```bash
   pip install -r requirements.txt && python init_db.py
   ```
5. Or use the included `backend/Dockerfile` for one-click container builds!

---

## 🏗️ 15-Table Relational Schema (`omniguard.db`)
1. `guidelines` (18 enterprise brand guidelines)
2. `vector_chunks` (45 384-dimensional Qdrant chunks)
3. `knowledge_graph_nodes` (40 Neo4j relationship triplets)
4. `visual_asset_tokens` (30 hex tokens, RGB, CIELAB, min APCA)
5. `channel_policies` (10 social and print publishing channels)
6. `audit_logs` (30 multi-channel audit records)
7. `micro_patches` (35 atomic RFC 6902 JSON patches)
8. `review_history` (45 multi-role RBAC decision trails)
9. `guideline_analytics` (30 drift and ambiguity records)
10. `brand_assets` (18 enterprise logos, typography, diagrams)
11. `team_roles` (8 granular RBAC permission records)
12. `compliance_certificates` (15 cryptographic SHA-256 records)
13. `apca_contrast_checks` (30 WCAG 2.2 AA perceptual checks)
14. `opencv_color_deltas` (30 CIELAB ΔE distance checks)
15. `rule_citations_map` (25 clause-to-rule mappings)

---

## 👥 Team Layer 7 Members
- **Swastik Mittal**: Data / Systems Engineer & Brand Lead
- **Aprajita**: Frontend Lead & Legal Counsel
- **Aditya Baliyan**: Backend Lead & Systems Engineer
- **Nikita Singh**: Full-Stack Integrator & Content Creator
