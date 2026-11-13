import os
import re

page_path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    content = f.read()

print("Original length:", len(content))

# ─────────────────────────────────────────────────────────────────────────────
# 1. Add DEMO_ACCOUNTS and Data Structures before TEAM_MEMBERS
# ─────────────────────────────────────────────────────────────────────────────
demo_data_code = '''
// ─────────────────────────────────────────────────────────────────────────────
// CodeNexus Hackathon Round 3: Evaluator Demo Accounts & Credentials
// ─────────────────────────────────────────────────────────────────────────────
const DEMO_ACCOUNTS = [
  {
    roleKey: 'brand_manager',
    name: 'Brand Director',
    email: 'brand.director@enterprise.omniguard.ai',
    password: 'OmniGuard#2026!Brand',
    icon: '👑',
    badge: 'Brand Lead',
    description: 'Manages brand voice, CIELAB color gamut, and policy thresholds',
    tone: 'purple' as const,
  },
  {
    roleKey: 'legal_counsel',
    name: 'General Counsel',
    email: 'legal.counsel@enterprise.omniguard.ai',
    password: 'OmniGuard#2026!Legal',
    icon: '⚖️',
    badge: 'Legal Sign-Off',
    description: 'Resolves cross-policy conflicts, regulatory disclosures, and FTC/GDPR compliance',
    tone: 'indigo' as const,
  },
  {
    roleKey: 'systems_engineer',
    name: 'Security Architect',
    email: 'security.arch@enterprise.omniguard.ai',
    password: 'OmniGuard#2026!Sec',
    icon: '🛡️',
    badge: 'Platform Security',
    description: 'Audits SHA-256 provenance chain, Qdrant vectors, and SQLite immutable ledgers',
    tone: 'blue' as const,
  },
  {
    roleKey: 'content_creator',
    name: 'Content Ops Lead',
    email: 'creator.ops@enterprise.omniguard.ai',
    password: 'OmniGuard#2026!Ops',
    icon: '✍️',
    badge: 'Creator Sign-Off',
    description: 'Executes parallel batch campaign scans and applies 1-click micro-patches',
    tone: 'emerald' as const,
  },
]

// ─────────────────────────────────────────────────────────────────────────────
// Improvement 1: Batch Multi-Channel Campaign Matrix Data
// ─────────────────────────────────────────────────────────────────────────────
interface CampaignAsset {
  id: number
  channel: string
  asset_name: string
  creative_type: string
  draft_text: string
  score: number
  status: 'compliant' | 'revision_required' | 'flagged'
  violations: number
  apca_score: number
  tone_delta: number
  issues: string[]
  patch: string
}

const SAMPLE_BATCH_CAMPAIGN: CampaignAsset[] = [
  {
    id: 1,
    channel: 'Google Ads',
    asset_name: 'Search Ad Copy #1 (Lead Gen)',
    creative_type: 'Search Ad Header & Description',
    draft_text: 'Deploy Enterprise AI in 48 Hours. Guaranteed Zero Drift. 100% Autonomous Brand Firewall.',
    score: 64,
    status: 'flagged',
    violations: 2,
    apca_score: 84.2,
    tone_delta: 3.4,
    issues: ['Prohibited 100% absolute guarantee claim (CLM-Q4-FC-019)', 'Unsubstantiated 48 Hours SLA metric (CLM-Q4-FC-028)'],
    patch: 'Deploy Enterprise AI rapidly. Engineered for minimal brand drift across all enterprise workflows.*',
  },
  {
    id: 2,
    channel: 'Meta / Instagram',
    asset_name: 'Carousel Slide #1 (Headline & Hero)',
    creative_type: 'Banner Visual & Copy',
    draft_text: 'Revolutionize your enterprise branding with OmniGuard AI. Disrupting legacy compliance forever. Try free today!',
    score: 72,
    status: 'revision_required',
    violations: 2,
    apca_score: 52.8,
    tone_delta: 4.1,
    issues: ['Prohibited buzzword "disrupting" (TON-GLO-009)', 'Color drift CIELAB ΔE 8.4 on hero accent (VIS-PAL-001)'],
    patch: 'Transform your enterprise branding with OmniGuard AI. Accelerating modern compliance with confidence. Request a demo.',
  },
  {
    id: 3,
    channel: 'LinkedIn',
    asset_name: 'Sponsored Thought Leadership Post',
    creative_type: 'Long-form Social',
    draft_text: 'Our platform reduces brand violations by up to 94% across enterprise workflows. Powered by proprietary ML models. Results may vary by use case.',
    score: 95,
    status: 'compliant',
    violations: 0,
    apca_score: 88.4,
    tone_delta: 0.8,
    issues: [],
    patch: 'Verified compliant with corporate tone and regulatory footnote requirements.',
  },
  {
    id: 4,
    channel: 'Email Newsletter',
    asset_name: 'Executive Decision-Maker Digest',
    creative_type: 'HTML Email Digest',
    draft_text: 'Unlock next-generation enterprise brand security with zero downtime. Click here to claim your exclusive corporate discount.',
    score: 78,
    status: 'revision_required',
    violations: 1,
    apca_score: 74.0,
    tone_delta: 2.2,
    issues: ['Absolute zero-downtime availability claim requires SLA qualification footnote (CLM-Q4-FC-019)'],
    patch: 'Unlock next-generation enterprise brand security with industry-leading reliability (99.9% uptime SLA). Contact enterprise sales.',
  },
]

// ─────────────────────────────────────────────────────────────────────────────
// Improvement 2: Spatial Visual Bounding Box Defect Interface
// ─────────────────────────────────────────────────────────────────────────────
interface BoundingBoxDefect {
  id: string
  label: string
  type: 'color_drift' | 'low_contrast' | 'margin_exclusion'
  x: number // percentage
  y: number // percentage
  width: number // percentage
  height: number // percentage
  severity: 'high' | 'critical' | 'medium'
  metric: string
  rule_citation: string
  auto_fix_label: string
  fixed: boolean
}

// ─────────────────────────────────────────────────────────────────────────────
// Improvement 3: Cross-Policy Contradiction Harmonizer Interface
// ─────────────────────────────────────────────────────────────────────────────
interface PolicyConflictItem {
  id: number
  title: string
  rule_a: string
  clause_a_text: string
  rule_b: string
  clause_b_text: string
  conflict_type: string
  severity: 'critical' | 'high' | 'medium'
  root_cause: string
  harmonized_text: string
  status: 'active' | 'resolved'
}

const DEFAULT_POLICY_CONFLICTS: PolicyConflictItem[] = [
  {
    id: 1,
    title: 'Global Performance Claims vs. EU GDPR / AI Act Local Disclosures',
    rule_a: 'Clause 3.2 (CLM-Q4-FC-019)',
    clause_a_text: 'All external marketing claims may state up to 94% automation without jurisdictional qualification headers.',
    rule_b: 'Clause 8.4 (REG-EU-GDPR-002)',
    clause_b_text: 'Marketing to EEA members must include prominent notices regarding automated processing safeguards.',
    conflict_type: 'Regulatory Jurisdictional Contradiction',
    severity: 'high',
    root_cause: 'Global product team guidelines omit mandatory EU AI Act Article 50 transparent labeling.',
    harmonized_text: 'Our platform helps achieve up to 94% brand compliance across enterprise workflows.* (*EEA/EU: Automated processing safeguards applied pursuant to EU AI Act Art. 50; see omniguard.ai/legal).',
    status: 'active',
  },
  {
    id: 2,
    title: 'Brand Amber Accent (#F59E0B) vs. APCA / WCAG Minimum Contrast Threshold',
    rule_a: 'Clause 1.4 (VIS-PAL-001)',
    clause_a_text: 'Brand Primary Accent Amber (#F59E0B) shall be utilized for critical call-to-action text on white cards.',
    rule_b: 'Clause 6.1 (ACC-WCAG-004)',
    clause_b_text: 'All interactive text elements on white backgrounds (#FFFFFF) must achieve an APCA lightness contrast rating of at least Lc 60.',
    conflict_type: 'Design System vs. Accessibility Standard',
    severity: 'medium',
    root_cause: '#F59E0B achieves only Lc 42.1 on white, directly violating accessibility conformance.',
    harmonized_text: 'Brand Primary Accent Amber (#D97706, APCA Lc 64.2) is authorized for text on white backgrounds; #F59E0B is reserved for non-text graphic accents.',
    status: 'active',
  },
  {
    id: 3,
    title: 'Social Media Brevity Guidelines vs. Mandatory FTC Safe Harbor Disclosures',
    rule_a: 'Clause 4.1 (SOC-X-LEN-008)',
    clause_a_text: 'Social media ad copy on X and Threads must remain strictly under 280 characters to preserve virality.',
    rule_b: 'Clause 2.4 (FTC-COM-SH-011)',
    clause_b_text: 'Any post citing customer ROI or cost reduction metrics must include complete FTC safe harbor disclaimer text (minimum 64 characters).',
    conflict_type: 'Marketing Brevity vs. Federal Disclosure Mandate',
    severity: 'critical',
    root_cause: 'Ad copy writers frequently breach character caps or drop mandatory FTC safe harbors when promoting stats.',
    harmonized_text: 'Social copy may utilize the short-form verified disclaimer link `*FTC: omniguard.ai/legal-roi` (28 chars) satisfying federal safe harbor requirements.',
    status: 'active',
  },
  {
    id: 4,
    title: 'Autonomous Agent Capability Claims vs. Proprietary Model Weights IP Protection',
    rule_a: 'Clause 5.3 (PR-PROD-CAP-012)',
    clause_a_text: 'Press releases must disclose the multi-modal agent architecture and underlying reasoning steps.',
    rule_b: 'Clause 7.1 (IP-SEC-MOD-005)',
    clause_b_text: 'No public-facing release shall reveal internal model routing mechanics, weights, or proprietary prompt schemas.',
    conflict_type: 'Product Transparency vs. Trade Secret IP Protection',
    severity: 'medium',
    root_cause: 'Press team drafts reveal internal routing heuristics that engineering flagged as confidential trade secrets.',
    harmonized_text: 'Public communications shall describe OmniGuard as powered by proprietary multi-stage consensus models without disclosing internal weight parameters or routing tokens.',
    status: 'active',
  },
]
'''

target_team_members = "// Enterprise Production Role Allocations"
if target_team_members in content and "const DEMO_ACCOUNTS" not in content:
    content = content.replace(target_team_members, demo_data_code + "\n" + target_team_members)
    print("Added DEMO_ACCOUNTS and interfaces!")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Step 1 done. New length:", len(content))
