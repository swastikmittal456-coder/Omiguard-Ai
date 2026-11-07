# OmniGuard AI — Intelligent Pre-Publication Brand Governance Platform
> **CodeNexus Enterprise — Round 2 Enterprise Showcase**  
> **Team**: OmniGuard Core Team | **Problem Statement**: Inkloom AI  

![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20Python%203.12-009688)
![SQLite](https://img.shields.io/badge/Database-15%20Relational%20Tables-003B57)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV%20K--Means%20%2B%20APCA-5C3EE8)
![Qdrant](https://img.shields.io/badge/Vectors-Qdrant%20384--dim-DC2626)
![Neo4j](https://img.shields.io/badge/Graph-Neo4j%20Deterministic-008CC1)

---

## 🎯 Executive Overview
Modern organisations distribute content creation across remote employees, regional marketing teams, agencies, and generative AI tools. Without a centralized pre-publication guardrail, this decentralization leads to severe brand drift.

**OmniGuard AI** is an explainable pre-publication brand governance platform that acts as an intelligent firewall for outgoing media. Rather than acting as a rigid blocker, OmniGuard AI inspects drafts against approved brand guidelines, fact sheets, and visual assets, providing instant, actionable **RFC 6902 JSON micro-patches** while preserving creator intent.

---

## 🔄 The 5-Stage Product Pipeline
1. **Stage 1: Ingest (Knowledge Graph + Vector Indexing)**:
   - 18 enterprise brand manuals and claim fact bases indexed into **Qdrant Vector DB** (384-dim semantic chunks) and **Neo4j Graph DB** (40 relationship nodes).
   - Ingestion modal supports uploading new PDFs, TXT, and JSON documents with live chunking animation.

2. **Stage 2: Multi-Audit (Multi-Modal AI Inspection)**:
   - Parallel workers audit **Messaging Tone**, **Unverified Claims**, **Hex Color Palette Adherence via OpenCV**, and **Accessibility Contrast Ratios via APCA (WCAG 2.2 AA)**.
   - Real-time drag-and-drop visual creative scanner extracts dominant 5-color palettes via K-Means and computes pixel-level CIELAB ΔE.

3. **Stage 3: Explain & Fix (Explainable Rule-Tracing Engine)**:
   - Every violation links directly to official guideline clauses (e.g. *Guideline Clause 3.2 / CLM-Q4-FC-019*).
   - Side-by-side red/green diff cards with 1-click atomic **RFC 6902 JSON micro-patching**.

4. **Stage 4: Review (Collaborative Review Workspace)**:
   - Role-Based Access Control (RBAC) review workflow for **Nikita Singh** (Creator), **Swastik Mittal** (Brand Manager), **Aprajita** (Legal Counsel), and **Aditya Baliyan** (Systems Engineer).
   - Generates and verifies cryptographic **SHA-256 AI provenance tags** and downloadable compliance certificates.

5. **Stage 5: Analytics (Guideline Drift & Insight Engine)**:
   - Tracks 1,284 enterprise audits with a 74.2% time reduction.
   - Mines recurring creator errors and highlights ambiguous or contradictory guidelines (e.g. Social Brevity vs. Mandatory Disclaimers).

---

## 🏛️ The 4 Architectural Innovation Pillars
1. **Explainable Rule-Tracing (Graph & Clause Grounding)**: Direct citations to master guidelines eliminate black-box ambiguity.
2. **Intent-Preserving Smart Micro-Patching**: RFC 6902 atomic JSON string replacements fix violations without overriding author voice.
3. **Multi-Modal Visual & Accessibility Guardrails**: Computer vision palette extraction + APCA contrast math guarantee WCAG AA compliance before publishing.
4. **Guideline Drift Analytics**: Mines long-term audit patterns to proactively alert corporate governance teams about unclear policies.

---

## 👥 OmniGuard Core Team
* **Swastik Mittal**: Data / Systems Engineer & Brand Lead
* **Aprajita**: Frontend Lead & Legal Counsel
* **Aditya Baliyan**: Backend Lead & Systems Engineer
* **Nikita Singh**: Full-Stack Integrator & Content Creator

---

## 📦 Deployment & Online Hosting
See [DEPLOYMENT.md](file:///c:/Users/swast/OneDrive/Desktop/vercel/DEPLOYMENT.md) for full instructions on local execution and 1-click cloud deployment to Vercel and Railway/Render.
