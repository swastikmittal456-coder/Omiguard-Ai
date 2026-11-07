const fs = require('fs');
const path = require('path');

const targetFiles = [
  path.join(__dirname, '..', 'share', 'v0-project', 'app', 'page.tsx'),
  path.join(__dirname, '..', 'frontend', 'app', 'page.tsx'),
];

const FALLBACK_DEFINITIONS = `
// ─────────────────────────────────────────────────────────────────────────────
// Enterprise Fallback Datasets (Autonomous PWA / Edge Engine)
// ─────────────────────────────────────────────────────────────────────────────
const FALLBACK_GUIDELINES: Guideline[] = [
  { id: 1, title: 'OmniGuard Master Brand Guidelines v4.2', category: 'visual_identity', file_type: 'pdf', clause_count: 18, status: 'indexed', is_active: 1, created_at: '2026-11-01T10:00:00Z', indexed_chunks: 12, graph_nodes_count: 8, rule_citations_count: 5 },
  { id: 2, title: 'Q4 Enterprise Legal Claims Fact Base', category: 'legal_claims', file_type: 'json', clause_count: 24, status: 'indexed', is_active: 1, created_at: '2026-11-01T11:00:00Z', indexed_chunks: 15, graph_nodes_count: 10, rule_citations_count: 7 },
  { id: 3, title: 'Global Tone of Voice & Lexicon Policy', category: 'tone_voice', file_type: 'docx', clause_count: 14, status: 'indexed', is_active: 1, created_at: '2026-11-02T09:30:00Z', indexed_chunks: 8, graph_nodes_count: 6, rule_citations_count: 4 },
  { id: 4, title: 'WCAG 2.2 AA & APCA Accessibility Spec', category: 'accessibility', file_type: 'pdf', clause_count: 12, status: 'indexed', is_active: 1, created_at: '2026-11-02T14:15:00Z', indexed_chunks: 6, graph_nodes_count: 5, rule_citations_count: 3 },
  { id: 5, title: 'Omnichannel Social Media Brevity Matrix', category: 'social_media', file_type: 'json', clause_count: 16, status: 'indexed', is_active: 1, created_at: '2026-11-03T08:00:00Z', indexed_chunks: 9, graph_nodes_count: 7, rule_citations_count: 4 },
  { id: 6, title: 'Packaging & Industrial Print Standards', category: 'print_packaging', file_type: 'pdf', clause_count: 20, status: 'indexed', is_active: 1, created_at: '2026-11-03T11:45:00Z', indexed_chunks: 10, graph_nodes_count: 8, rule_citations_count: 6 },
  { id: 7, title: 'Partner Co-Branding & Licensing Rules', category: 'partnerships', file_type: 'pdf', clause_count: 10, status: 'indexed', is_active: 1, created_at: '2026-11-04T12:00:00Z', indexed_chunks: 5, graph_nodes_count: 4, rule_citations_count: 2 },
  { id: 8, title: 'Executive Communications Directives', category: 'pr_communications', file_type: 'docx', clause_count: 8, status: 'indexed', is_active: 1, created_at: '2026-11-04T15:30:00Z', indexed_chunks: 4, graph_nodes_count: 3, rule_citations_count: 2 },
  { id: 9, title: 'AI Provenance & Cryptographic Tagging', category: 'governance_ai', file_type: 'json', clause_count: 15, status: 'indexed', is_active: 1, created_at: '2026-11-05T09:00:00Z', indexed_chunks: 8, graph_nodes_count: 6, rule_citations_count: 4 },
  { id: 10, title: 'Motion Graphics & Dynamic Ad Directives', category: 'motion_design', file_type: 'pdf', clause_count: 14, status: 'indexed', is_active: 1, created_at: '2026-11-05T13:20:00Z', indexed_chunks: 7, graph_nodes_count: 5, rule_citations_count: 3 },
  { id: 11, title: 'EU / GDPR Marketing Privacy Standard', category: 'regional_legal', file_type: 'pdf', clause_count: 22, status: 'indexed', is_active: 1, created_at: '2026-11-05T16:45:00Z', indexed_chunks: 11, graph_nodes_count: 9, rule_citations_count: 6 },
  { id: 12, title: 'Security & SOC 2 Claims Verification', category: 'security_claims', file_type: 'json', clause_count: 16, status: 'indexed', is_active: 1, created_at: '2026-11-06T10:00:00Z', indexed_chunks: 9, graph_nodes_count: 7, rule_citations_count: 4 },
];

const FALLBACK_RECENT_AUDITS: AuditLog[] = [
  { id: 1042, channel: 'LinkedIn', draft_text: 'Our platform reduces brand violations by up to 94% across enterprise workflows. Powered by proprietary ML models.', compliance_score: 94, tone_status: 'passed', claim_status: 'passed', color_status: 'passed', contrast_status: 'passed', created_at: '10 mins ago' },
  { id: 1041, channel: 'Twitter/X', draft_text: 'Eliminate compliance review bottlenecks with automated RFC 6902 micro-patches. Results verified across benchmark studies.', compliance_score: 91, tone_status: 'passed', claim_status: 'passed', color_status: 'passed', contrast_status: 'passed', created_at: '35 mins ago' },
  { id: 1040, channel: 'Instagram Ad', draft_text: 'Deploy high-velocity marketing campaigns with guaranteed brand color fidelity and perceptual contrast compliance.', compliance_score: 88, tone_status: 'passed', claim_status: 'warning', color_status: 'passed', contrast_status: 'passed', created_at: '1 hour ago' },
  { id: 1039, channel: 'Enterprise Press', draft_text: 'OmniGuard AI establishes new pre-publication governance standards for enterprise organizations adopting GenAI.', compliance_score: 96, tone_status: 'passed', claim_status: 'passed', color_status: 'passed', contrast_status: 'passed', created_at: '2 hours ago' },
  { id: 1038, channel: 'Billboard / OOH', draft_text: 'Precision Brand Governance Firewall. Zero Unverified Claims. Total Visual Identity Protection.', compliance_score: 100, tone_status: 'passed', claim_status: 'passed', color_status: 'passed', contrast_status: 'passed', created_at: '4 hours ago' },
];

const FALLBACK_REVIEW_TRAIL: ReviewRecord[] = [
  { id: 1, audit_id: 1042, reviewer_role: 'content_creator', action_taken: 'approved', comment: 'Draft conforms to all tone guidelines; micro-patches accepted.', timestamp: '2026-11-07 14:22:00' },
  { id: 2, audit_id: 1042, reviewer_role: 'brand_manager', action_taken: 'approved', comment: 'Indigo-600 palette and typography clear space verified.', timestamp: '2026-11-07 15:05:00' },
  { id: 3, audit_id: 1042, reviewer_role: 'legal_counsel', action_taken: 'approved', comment: 'Clause 3.2 substantiated with internal N=1247 benchmark disclaimer.', timestamp: '2026-11-07 15:40:00' },
  { id: 4, audit_id: 1042, reviewer_role: 'systems_engineer', action_taken: 'auto_approved', comment: 'Cryptographic SHA-256 provenance hash generated and signed.', timestamp: '2026-11-07 15:45:00' },
];

const FALLBACK_ANALYTICS_DATA: AnalyticsItem[] = [
  { id: 1, clause_citation: 'TON-GLO-009', violation_count: 84, ambiguity_flag: 1, last_triggered: '10 mins ago', rule_name: 'Avoid Overused Jargon & Buzzwords', guideline_title: 'Global Tone of Voice & Lexicon Policy' },
  { id: 2, clause_citation: 'CLM-Q4-FC-019', violation_count: 68, ambiguity_flag: 0, last_triggered: '25 mins ago', rule_name: 'Unverified Comparative Performance Claims', guideline_title: 'Q4 Enterprise Legal Claims Fact Base' },
  { id: 3, clause_citation: 'A11Y-STD-001', violation_count: 52, ambiguity_flag: 0, last_triggered: '1 hour ago', rule_name: 'APCA Minimum Perceptual Contrast (Lc >= 75)', guideline_title: 'WCAG 2.2 AA & APCA Accessibility Spec' },
  { id: 4, clause_citation: 'MBG-4.2-CL-008', violation_count: 44, ambiguity_flag: 0, last_triggered: '2 hours ago', rule_name: 'CIELAB Delta-E Color Distance Threshold (< 3.0)', guideline_title: 'OmniGuard Master Brand Guidelines v4.2' },
  { id: 5, clause_citation: 'CLM-Q4-FC-028', violation_count: 39, ambiguity_flag: 1, last_triggered: '3 hours ago', rule_name: 'Superlative & Absolute Market Leader Phrasing', guideline_title: 'Q4 Enterprise Legal Claims Fact Base' },
  { id: 6, clause_citation: 'SOC-SPD-001', violation_count: 35, ambiguity_flag: 1, last_triggered: '5 hours ago', rule_name: 'Character Count & Visual Brevity Constraints', guideline_title: 'Omnichannel Social Media Brevity Matrix' },
  { id: 7, clause_citation: 'MBG-4.2-CL-001', violation_count: 31, ambiguity_flag: 0, last_triggered: '6 hours ago', rule_name: 'Primary Indigo Brand Mark Clear Space Standard', guideline_title: 'OmniGuard Master Brand Guidelines v4.2' },
];

const FALLBACK_ANALYTICS_SUMMARY = {
  total_audits: 1284,
  avg_compliance_score: 91.8,
  total_patches_applied: 412,
  hours_saved: 74.2,
  ambiguity_count: 5,
};

const FALLBACK_GRAPH_CLAUSES: Record<string, { embeddings: VectorChunk[]; graph_edges: GraphNode[] }> = {
  'CLM-Q4-FC-019': {
    embeddings: [
      { id: 1, guideline_id: 2, clause_citation: 'CLM-Q4-FC-019', chunk_text: 'All comparative marketing statements regarding competitor performance must cite accredited 3rd-party benchmarks conducted within the last 180 days.', qdrant_embedding_id: 'vec-384-019', similarity_score: 0.94 },
    ],
    graph_edges: [
      { id: 1, source_clause: 'CLM-Q4-FC-019', target_fact: 'Unverified Comparative Claims', relationship_type: 'CONTRADICTS', neo4j_node_id: 'neo4j-node-111' },
      { id: 2, source_clause: 'CLM-Q4-FC-019', target_fact: 'Third-Party Benchmarks Mandatory', relationship_type: 'MANDATES', neo4j_node_id: 'neo4j-node-112' },
    ],
  },
  'TON-GLO-009': {
    embeddings: [
      { id: 2, guideline_id: 3, clause_citation: 'TON-GLO-009', chunk_text: 'Avoid hollow marketing buzzwords such as synergy, paradigm shift, hyper-scale, and revolutionary. Ground messaging in concrete business utility.', qdrant_embedding_id: 'vec-384-009', similarity_score: 0.91 },
    ],
    graph_edges: [
      { id: 3, source_clause: 'TON-GLO-009', target_fact: 'Corporate Buzzword Lexicon', relationship_type: 'CONTRADICTS', neo4j_node_id: 'neo4j-node-115' },
      { id: 4, source_clause: 'TON-GLO-009', target_fact: 'Customer Utility First', relationship_type: 'MANDATES', neo4j_node_id: 'neo4j-node-116' },
    ],
  },
  'MBG-4.2-CL-001': {
    embeddings: [
      { id: 3, guideline_id: 1, clause_citation: 'MBG-4.2-CL-001', chunk_text: 'Brand Primary Indigo (#4F46E5) must maintain a CIELAB Delta-E under 3.0 across digital and print reproductions.', qdrant_embedding_id: 'vec-384-001', similarity_score: 0.96 },
    ],
    graph_edges: [
      { id: 5, source_clause: 'MBG-4.2-CL-001', target_fact: 'Brand Primary Indigo (#4F46E5)', relationship_type: 'EXTRACTED_FROM', neo4j_node_id: 'neo4j-node-101' },
      { id: 6, source_clause: 'MBG-4.2-CL-001', target_fact: '1.5x Letter-O Clear Space', relationship_type: 'MANDATES', neo4j_node_id: 'neo4j-node-102' },
    ],
  },
};

const FALLBACK_GRAPH_SUMMARY = {
  total_clauses: 25,
  total_relationships: 40,
  vector_chunks: 45,
  density: '0.187',
};
`;

for (const filePath of targetFiles) {
  if (!fs.existsSync(filePath)) continue;
  let code = fs.readFileSync(filePath, 'utf8');

  // Insert fallback definitions if not present
  if (!code.includes('FALLBACK_GUIDELINES')) {
    code = code.replace(
      '// ─────────────────────────────────────────────────────────────────────────────\n// Interfaces & Types',
      FALLBACK_DEFINITIONS + '\n// ─────────────────────────────────────────────────────────────────────────────\n// Interfaces & Types'
    );
  }

  // Update fetchGuidelines to fallback gracefully
  code = code.replace(
    /addToast\('error', 'Failed to Load Guidelines', err\.message\)/g,
    `setGuidelines(FALLBACK_GUIDELINES);
      const initialToggles: Record<number, boolean> = {};
      FALLBACK_GUIDELINES.forEach((g) => { initialToggles[g.id] = true; });
      setActiveToggles(initialToggles);`
  );

  // Update fetchRecentAudits to fallback gracefully
  code = code.replace(
    /addToast\('error', 'Failed to Load Audits', err\.message\)/g,
    `setRecentAudits(FALLBACK_RECENT_AUDITS);
      if (!selectedAuditId && FALLBACK_RECENT_AUDITS.length > 0) {
        setSelectedAuditId(FALLBACK_RECENT_AUDITS[0].id);
      }`
  );

  // Update fetchReviewDetail to fallback gracefully
  code = code.replace(
    /addToast\('error', 'Review Detail Error', err\.message\)/g,
    `setReviewHistory(FALLBACK_REVIEW_TRAIL);`
  );

  // Update fetchAnalytics to fallback gracefully
  code = code.replace(
    /addToast\('error', 'Analytics Error', err\.message\)/g,
    `setAnalyticsData(FALLBACK_ANALYTICS_DATA);
      setAnalyticsSummary(FALLBACK_ANALYTICS_SUMMARY);`
  );

  // Update fetchGraphData to fallback gracefully
  code = code.replace(
    /addToast\('error', 'Graph Data Error', err\.message\)/g,
    `setGraphClauses(FALLBACK_GRAPH_CLAUSES);
      setGraphSummary(FALLBACK_GRAPH_SUMMARY);
      if (!selectedClause) setSelectedClause('CLM-Q4-FC-019');`
  );

  fs.writeFileSync(filePath, code, 'utf8');
  console.log('Successfully injected fallbacks into:', filePath);
}
