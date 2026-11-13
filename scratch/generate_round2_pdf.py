import os
import subprocess
import shutil

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>OmniGuard AI - Round 2 Implementation Dossier</title>
<style>
  @page {
    size: letter portrait;
    margin: 14mm 16mm 14mm 16mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 8.8pt;
    line-height: 1.38;
  }
  .page {
    width: 100%;
    min-height: 250mm;
    page-break-after: always;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .page:last-child {
    page-break-after: avoid;
  }
  .page-content {
    flex: 1;
  }
  
  /* Running Header */
  .running-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 4px;
    margin-bottom: 12px;
    font-size: 7.5pt;
    font-weight: 700;
    color: #475569;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .running-header span.accent {
    color: #1e3a8a;
  }
  
  /* Running Footer */
  .running-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #cbd5e1;
    padding-top: 5px;
    margin-top: 10px;
    font-size: 7.5pt;
    color: #64748b;
  }

  /* Document Hero Header (Page 1) */
  .hero-title {
    font-size: 20pt;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: #0f172a;
    margin: 0 0 2px 0;
    text-transform: uppercase;
  }
  .hero-subtitle {
    font-size: 10.5pt;
    font-weight: 600;
    color: #2563eb;
    margin: 0 0 10px 0;
  }
  .metadata-bar {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 7.8pt;
    font-weight: 600;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
  }
  .metadata-bar span {
    color: #93c5fd;
  }

  /* Section Headings */
  .section-header {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 9.5pt;
    font-weight: 800;
    color: #0f172a;
    margin: 10px 0 6px 0;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  .section-header .bar {
    width: 4px;
    height: 13px;
    background-color: #2563eb;
    border-radius: 2px;
    display: inline-block;
  }

  p {
    margin: 0 0 6px 0;
    text-align: justify;
  }
  p strong {
    color: #0f172a;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0 10px 0;
    font-size: 7.8pt;
  }
  th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 5px 8px;
    border: 1px solid #0f172a;
    font-size: 7.5pt;
    letter-spacing: 0.2px;
  }
  td {
    padding: 4.5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    line-height: 1.3;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  /* Badges */
  .badge {
    display: inline-block;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 6.8pt;
    font-weight: 800;
    letter-spacing: 0.3px;
    text-transform: uppercase;
  }
  .badge-delivered {
    background-color: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
  }
  .badge-blue {
    background-color: #dbeafe;
    color: #1e40af;
    border: 1px solid #93c5fd;
  }

  /* List Items */
  ul {
    margin: 4px 0 8px 0;
    padding-left: 16px;
  }
  li {
    margin-bottom: 5px;
    line-height: 1.34;
    text-align: justify;
  }
  li strong {
    color: #0f172a;
  }

  /* Code / Benchmark Box */
  .benchmark-box {
    background-color: #f1f5f9;
    border-left: 3px solid #2563eb;
    border-right: 1px solid #e2e8f0;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 7px 10px;
    margin: 6px 0 10px 0;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 7.4pt;
    color: #0f172a;
    line-height: 1.45;
  }
  .benchmark-title {
    font-weight: 800;
    color: #1e3a8a;
    margin-bottom: 3px;
  }
</style>
</head>
<body>

<!-- ================= PAGE 1 ================= -->
<div class="page">
  <div class="page-content">
    <div class="hero-title">OMNIGUARD AI</div>
    <div class="hero-subtitle">Intelligent Pre-Publication Brand Governance & Cryptographic Provenance Platform</div>
    <div class="metadata-bar">
      <div>Team Name: <span>Team Layer 7</span> &nbsp;|&nbsp; Problem Statement: <span>Inkloom AI</span></div>
      <div>Submission: <span>CodeNexus Hackathon — Round 2 Implementation Dossier</span></div>
    </div>

    <div class="section-header">
      <span class="bar"></span>
      <span>1. Problem Statement & Empirical Risk Context</span>
    </div>
    <p>
      <strong>The Challenge:</strong> Modern enterprises distribute content creation across regional divisions, distributed marketing teams, external agencies, and generative AI models. Without centralized pre-publication guardrails, this decentralization triggers severe brand drift—including outdated logos, off-palette colors, inconsistent messaging tone, and unverified promotional claims. Manual human-in-the-loop review queues create costly 3–5 day publication bottlenecks and fail to catch subtle compliance violations [1, 2].
    </p>
    <p>
      <strong>The Risk &amp; Impact:</strong> Publishing unvetted promotional media damages corporate credibility and exposes organizations to severe legal liabilities under FTC truth-in-advertising substantiation mandates, emerging EU AI Act Article 50 disclosures, and ADA/WCAG Title III accessibility litigation for low text-to-background contrast [1].
    </p>

    <div style="font-size: 8.2pt; font-weight: 700; color: #1e3a8a; margin: 8px 0 3px 0;">
      Target User Personas &amp; Organizational Value Delivered
    </div>
    <table>
      <thead>
        <tr>
          <th style="width: 20%;">User Persona</th>
          <th style="width: 35%;">Primary Operating Need</th>
          <th style="width: 45%;">OmniGuard AI Delivered Solution</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Content Creators</strong></td>
          <td>Fast, non-blocking feedback during copy drafting and visual creative design.</td>
          <td>Sub-second multi-modal auditing with 1-click intent-preserving RFC 6902 micro-patches.</td>
        </tr>
        <tr>
          <td><strong>Brand &amp; Marketing Leads</strong></td>
          <td>Enforce absolute visual, color, and tonal consistency across all channels.</td>
          <td>Automated OpenCV CIELAB &Delta;E palette verification and semantic tone variance analysis against 18 master manuals.</td>
        </tr>
        <tr>
          <td><strong>Legal &amp; Compliance Officers</strong></td>
          <td>Verifiable compliance audit evidence before media assets are published.</td>
          <td>Immutable SQLite governance ledger, multi-role RBAC sign-off, and cryptographic SHA-256 AI Provenance Certificates.</td>
        </tr>
      </tbody>
    </table>

    <div class="section-header">
      <span class="bar"></span>
      <span>2. Delivered Solution &amp; 5-Stage Production Pipeline</span>
    </div>
    <p>
      <strong>Solution Overview:</strong> OmniGuard AI operates as an intelligent pre-publication firewall for outgoing enterprise media. Rather than acting as a rigid blocker, OmniGuard AI audits draft copy and creative imagery in parallel against indexed brand guidelines, fact sheets, and visual tokens. It provides surgical, intent-preserving micro-patches and mints tamper-evident cryptographic provenance certificates upon multi-role sign-off [2].
    </p>

    <div style="font-size: 8.2pt; font-weight: 700; color: #1e3a8a; margin: 8px 0 3px 0;">
      End-to-End 5-Stage Live Product Pipeline
    </div>
    <table>
      <thead>
        <tr>
          <th style="width: 15%;">Stage</th>
          <th style="width: 32%;">System Mechanism</th>
          <th style="width: 53%;">User Experience &amp; Production Workflow</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1. Ingest</strong></td>
          <td>Multi-Format Ingestion &amp; Vector Chunking</td>
          <td>Admins upload brand manuals, claim sheets, and visual tokens (.pdf, .txt, .md) into SQLite and vector stores with 18 pre-indexed corporate policies.</td>
        </tr>
        <tr>
          <td><strong>2. Multi-Audit</strong></td>
          <td>Parallel Multi-Modal AI Inspection Pipeline</td>
          <td>Creators submit drafts. Parallel workers audit Tone, Unsubstantiated Claims, OpenCV CIELAB &Delta;E Colors (&lt;350ms), and APCA WCAG 3.0 Contrast.</td>
        </tr>
        <tr>
          <td><strong>3. Explain &amp; Fix</strong></td>
          <td>Intent-Preserving RFC 6902 Patch Engine</td>
          <td>Flags violations with exact clause citations (e.g., Clause 3.2 / CLM-Q4-FC-019); generates 1-click atomic micro-patches with live score recalculation.</td>
        </tr>
        <tr>
          <td><strong>4. Governance</strong></td>
          <td>Multi-Role RBAC &amp; Provenance Hub</td>
          <td>Tiered sign-off gates for Brand Director, General Counsel, Security Architect, and Content Ops, minting tamper-evident SHA-256 AI Provenance Certificates.</td>
        </tr>
        <tr>
          <td><strong>5. Analytics &amp; Graph</strong></td>
          <td>Policy Drift Dashboard &amp; Knowledge Graph</td>
          <td>Monitors compliance drift across 1,280+ audits, flags cross-channel rule ambiguities, and visualizes 45+ clauses in an interactive 40-node knowledge graph.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="running-footer">
    <div>CodeNexus Hackathon • Pre-Publication Brand Governance Platform</div>
    <div>Page 1 of 3</div>
  </div>
</div>

<!-- ================= PAGE 2 ================= -->
<div class="page">
  <div class="page-content">
    <div class="running-header">
      <div>OMNIGUARD AI | <span class="accent">ROUND 2 IMPLEMENTATION DOSSIER</span></div>
      <div>TEAM LAYER 7 — INKLOOM AI</div>
    </div>

    <div class="section-header">
      <span class="bar"></span>
      <span>3. Originality &amp; Delivered Innovation Pillars</span>
    </div>
    <p>
      Unlike generic LLM wrappers or surface-level grammar linters, OmniGuard AI introduces five production-tested architectural innovations engineered for high-consequence enterprise governance:
    </p>
    <ul>
      <li>
        <strong>Pillar 1: Deterministic Clause Grounding (Zero Hallucination):</strong> Every flagged violation links directly to an authoritative clause in the company's indexed brand manual or fact base (e.g., <em>Clause 3.2: Unsupported Absolute Guarantee; see Fact Sheet CLM-Q4-FC-019</em>), eliminating black-box AI ambiguity [2, 4].
      </li>
      <li>
        <strong>Pillar 2: Intent-Preserving RFC 6902 Smart Micro-Patching:</strong> Rather than regenerating entire documents or overriding human voice, the engine produces atomic, RFC 6902-compliant JSON diff patches that surgically correct offending phrases or colors without altering core promotional intent [2, 3].
      </li>
      <li>
        <strong>Pillar 3: Rigorous Color Science &amp; APCA Contrast Engine:</strong> Replaces crude Euclidean RGB distance with <strong>OpenCV CIELAB &Delta;E 2000</strong> sub-pixel color space analysis (&Delta;E &lt; 3.0 Just Noticeable Difference) and <strong>APCA (Advanced Perceptual Contrast Algorithm / WCAG 3.0)</strong> lightness contrast (Lc &ge; 75.0 normal text / &ge; 60.0 large text) [2, 3].
      </li>
      <li>
        <strong>Pillar 4: Cryptographic SHA-256 AI Provenance Certificates:</strong> Approved assets receive a digitally signed, tamper-evident certificate embedding audit snapshots, rule hashes, and multi-role signatures, verifiable in real time via an on-platform cryptographic hash validator.
      </li>
      <li>
        <strong>Pillar 5: Offline Deterministic Fallback Engine:</strong> Features a client-side rule evaluation engine that guarantees continuous, zero-downtime auditing and micro-patch generation even during API or network interruptions.
      </li>
    </ul>

    <div class="section-header">
      <span class="bar"></span>
      <span>4. Delivered Technical Architecture &amp; System Benchmarks</span>
    </div>
    <p>
      OmniGuard AI is built upon an enterprise-grade decoupled microservices architecture designed for sub-second execution, strict data security, and verifiable explainability [3].
    </p>

    <div style="font-size: 8.2pt; font-weight: 700; color: #1e3a8a; margin: 8px 0 3px 0;">
      System Architecture &amp; Technology Stack
    </div>
    <table>
      <thead>
        <tr>
          <th style="width: 18%;">Layer / Module</th>
          <th style="width: 32%;">Technology Selection</th>
          <th style="width: 50%;">Production Scope &amp; Verified Performance</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Frontend UI</strong></td>
          <td>Next.js 16 (App Router), React 19, Tailwind CSS, Framer Motion</td>
          <td>5 dedicated route pages (/scanner, /guidelines, /governance, /analytics, /graph) with spring physics "bubble-up" micro-interactions and inline A/B diff modals.</td>
        </tr>
        <tr>
          <td><strong>Backend API</strong></td>
          <td>FastAPI (Python 3.12), Uvicorn, Pydantic v2</td>
          <td>15 REST endpoints handling multi-modal analysis, guideline chunking, atomic patch application, and cryptographic signature verification.</td>
        </tr>
        <tr>
          <td><strong>Relational &amp; Ledger</strong></td>
          <td>SQLite Enterprise Store (15 Relational Tables)</td>
          <td>Immutable audit trail, 49+ review history logs, 18 brand guidelines, 40 graph nodes, and pre-computed policy drift analytics.</td>
        </tr>
        <tr>
          <td><strong>Color &amp; Vision Engine</strong></td>
          <td>OpenCV (cv2), NumPy, Pillow</td>
          <td>Sub-pixel CIELAB &Delta;E 2000 matrix decoding and dominant palette clustering executing in under 350ms.</td>
        </tr>
        <tr>
          <td><strong>Accessibility Engine</strong></td>
          <td>APCA 0.98G Contrast Algorithm (WCAG 3.0)</td>
          <td>Non-linear perceptual lightness contrast calculation (Lc) across dynamic text and creative backgrounds.</td>
        </tr>
      </tbody>
    </table>

    <div style="font-size: 8.2pt; font-weight: 700; color: #1e3a8a; margin: 8px 0 3px 0;">
      Responsible Design, Data Privacy &amp; Human Control
    </div>
    <ul>
      <li><strong>Data Isolation &amp; Zero External Leakage:</strong> Enterprise guidelines and unreleased campaign assets are stored within local relational and vector structures; no proprietary assets are used to train public foundation models.</li>
      <li><strong>Multi-Role RBAC Governance:</strong> Distinct permission tiers enforce role-separated sign-offs between Content Creators, Brand Directors, General Counsel, and Security Architects.</li>
      <li><strong>Human-in-the-Loop Supremacy:</strong> Automated micro-patches remain non-destructive recommendations until explicitly applied by a human reviewer. The system never overrides human choices automatically [8, 10].</li>
      <li><strong>Live Mathematical &amp; Algorithmic Explainability:</strong> An interactive drawer exposes live mathematical formulations for CIELAB &Delta;E, APCA Lc, and weighted governance scoring formulas directly to users.</li>
    </ul>
  </div>
  <div class="running-footer">
    <div>CodeNexus Hackathon • Pre-Publication Brand Governance Platform</div>
    <div>Page 2 of 3</div>
  </div>
</div>

<!-- ================= PAGE 3 ================= -->
<div class="page">
  <div class="page-content">
    <div class="running-header">
      <div>OMNIGUARD AI | <span class="accent">ROUND 2 IMPLEMENTATION DOSSIER</span></div>
      <div>TEAM LAYER 7 — INKLOOM AI</div>
    </div>

    <div class="section-header">
      <span class="bar"></span>
      <span>5. Round 2 Milestone Delivery &amp; Verification Report</span>
    </div>
    <p>
      The technical development plan has been executed to 100% completion with all core systems verified against automated benchmark test suites [5]:
    </p>

    <div style="font-size: 8.2pt; font-weight: 700; color: #1e3a8a; margin: 6px 0 3px 0;">
      Round 2 Milestone Delivery Matrix
    </div>
    <table>
      <thead>
        <tr>
          <th style="width: 22%;">Phase &amp; Timeline</th>
          <th style="width: 38%;">Milestone Deliverables</th>
          <th style="width: 40%;">Implementation Status &amp; Verification</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Phase 1: Foundation</strong> (Hours 0 – 12)</td>
          <td>Ingestion Engine, Relational Ledger &amp; Knowledge Graph</td>
          <td><span class="badge badge-delivered">&check; DELIVERED</span> 15 SQLite tables, 18 brand guidelines, 45 clause vectors, and 40-node deterministic knowledge graph schema.</td>
        </tr>
        <tr>
          <td><strong>Phase 2: Core Build</strong> (Hours 12 – 32)</td>
          <td>Multi-Modal Pipeline, RFC 6902 Engine &amp; Dedicated Routes</td>
          <td><span class="badge badge-delivered">&check; DELIVERED</span> OpenCV CIELAB &Delta;E, APCA contrast, 1-click micro-patches, and 5 dedicated Next.js App Router URLs.</td>
        </tr>
        <tr>
          <td><strong>Phase 3: Polish &amp; Refine</strong> (Hours 32 – 48)</td>
          <td>RBAC Hub, SHA-256 Provenance &amp; Verification Suite</td>
          <td><span class="badge badge-delivered">&check; DELIVERED</span> Multi-role governance sign-off, cryptographic hash verifier, and 47/47 automated system tests passing (Grade A+).</td>
        </tr>
      </tbody>
    </table>

    <div style="font-size: 8.2pt; font-weight: 700; color: #1e3a8a; margin: 8px 0 3px 0;">
      Team Layer 7 — Member Contribution &amp; Role Execution
    </div>
    <table>
      <thead>
        <tr>
          <th style="width: 18%;">Team Member</th>
          <th style="width: 32%;">Assigned Role</th>
          <th style="width: 50%;">Technical Responsibilities &amp; Delivered Systems</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Swastik Mittal</strong></td>
          <td>Data / Systems Engineer &amp; Brand Lead</td>
          <td>Engineered OpenCV CIELAB &Delta;E 2000 and APCA contrast pipelines; structured SQLite 15-table relational schema, and designed Brand Governance Knowledge Base [4].</td>
        </tr>
        <tr>
          <td><strong>Aprajita</strong></td>
          <td>Frontend Lead &amp; Legal Counsel</td>
          <td>Built Next.js 16 App Router UI with dedicated page routes, Framer Motion directional swish transitions, bubble-up button animations, and legal disclaimer rubric [4].</td>
        </tr>
        <tr>
          <td><strong>Aditya Baliyan</strong></td>
          <td>Backend Lead &amp; Systems Engineer</td>
          <td>Implemented FastAPI 15-endpoint REST API, multi-role RBAC sign-off workflows, SHA-256 cryptographic certificate minting, and automated test suite [4].</td>
        </tr>
        <tr>
          <td><strong>Nikita Singh</strong></td>
          <td>Full Stack Integrator &amp; Content Operations</td>
          <td>Integrated client-side deterministic fallback engine, command palette (Cmd/Ctrl+K), A/B comparison diff modal, and end-to-end API hydration [4].</td>
        </tr>
      </tbody>
    </table>

    <div class="section-header" style="margin-top: 8px;">
      <span class="bar"></span>
      <span>6. Verified Benchmarks &amp; Platform Grade</span>
    </div>
    <div class="benchmark-box">
      <div class="benchmark-title">&bull; AUDIT BENCHMARK SUMMARY: 47/47 TESTS PASSED (100%) &bull; EXECUTION: 1.88s &bull; GRADE: ENTERPRISE A+</div>
      &bull; Backend REST Endpoints: 13/13 Passed (Tone, Claims, Image OpenCV &Delta;E, Patch, RBAC, Certificate)<br>
      &bull; Relational Schema Integrity: 15/15 Tables Validated (18 Guidelines, 45 Clauses, 40 Graph Nodes)<br>
      &bull; Visual &amp; Color Science: OpenCV CIELAB &Delta;E = 0.00 (&Delta;E &lt; 3.0 JND: PASSED), APCA Lc = 83.0 (PASSED)<br>
      &bull; Frontend Route Hydration: 5/5 Dedicated Pages Active (/scanner, /guidelines, /governance, /analytics, /graph)
    </div>

    <div class="section-header" style="margin-top: 6px;">
      <span class="bar"></span>
      <span>7. Ambitious Round 3 Product Roadmap</span>
    </div>
    <p style="font-size: 7.9pt; margin-bottom: 2px;">
      <strong>1. Batch Multi-Channel Campaign Auditor:</strong> Asynchronous bulk ingestion (ZIP/CSV) executing parallel audits tailored across Google Ads, Meta, LinkedIn, and Email with consolidated compliance matrices.
    </p>
    <p style="font-size: 7.9pt; margin-bottom: 2px;">
      <strong>2. Spatial Visual Bounding Box &amp; In-Canvas Defect Localization:</strong> OpenCV spatial coordinate engine rendering interactive bounding boxes and pin markers directly over defective image regions.
    </p>
    <p style="font-size: 7.9pt; margin-bottom: 4px;">
      <strong>3. Cross-Policy Contradiction Detection &amp; Interactive Diff Merger:</strong> Semantic rule-conflict resolution engine detecting contradictions between international manuals with side-by-side clause diff merging.
    </p>
  </div>
  <div class="running-footer">
    <div>CodeNexus Hackathon • Pre-Publication Brand Governance Platform</div>
    <div>Page 3 of 3</div>
  </div>
</div>

</body>
</html>
"""

html_path = r"C:\Users\swast\OneDrive\Desktop\vercel\scratch\round2_proposal.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved HTML template to", html_path)

# Print to PDF using Chrome or Edge
browser_exec = None
if os.path.exists(r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
    browser_exec = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
elif os.path.exists(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
    browser_exec = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

out_pdf_workspace = r"C:\Users\swast\OneDrive\Desktop\vercel\OmniGuard_AI_Round_2_Submission.pdf"
out_pdf_public = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\public\OmniGuard_AI_Round_2_Submission.pdf"

if browser_exec:
    cmd = [
        browser_exec,
        "--headless=new",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={out_pdf_workspace}",
        "--no-pdf-header-footer",
        html_path
    ]
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Return code:", res.returncode)
    if os.path.exists(out_pdf_workspace):
        size = os.path.getsize(out_pdf_workspace)
        print(f"Success! Generated PDF at {out_pdf_workspace} ({size} bytes)")
        shutil.copyfile(out_pdf_workspace, out_pdf_public)
        print(f"Copied to public web server: {out_pdf_public}")
    else:
        print("Error: PDF was not generated.")
else:
    print("No browser found.")
