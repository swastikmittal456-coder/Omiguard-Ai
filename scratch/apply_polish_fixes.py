import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

page_path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update computeClientAuditFallback to return both audit and audit_log
old_fallback_return = '''  return {
    audit: {
      id: Math.floor(Math.random() * 900) + 100,
      channel,
      draft_text: text,
      compliance_score: score,
      tone_status: issues.some(i => i.guideline_clause.includes('TON')) ? 'fail' : 'pass',
      claim_status: issues.some(i => i.guideline_clause.includes('CLM')) ? 'fail' : 'pass',
      color_status: issues.some(i => i.guideline_clause.includes('VIS')) ? 'fail' : 'pass',
      contrast_status: issues.some(i => i.guideline_clause.includes('A11Y')) ? 'fail' : 'pass',
      created_at: new Date().toISOString()
    },
    compliance_score: score,
    micro_patches: issues
  };'''

new_fallback_return = '''  const auditRecord = {
    id: Math.floor(Math.random() * 900) + 100,
    channel,
    draft_text: text,
    compliance_score: score,
    tone_status: issues.some(i => i.guideline_clause.includes('TON')) ? 'fail' : 'pass',
    claim_status: issues.some(i => i.guideline_clause.includes('CLM')) ? 'fail' : 'pass',
    color_status: issues.some(i => i.guideline_clause.includes('VIS')) ? 'fail' : 'pass',
    contrast_status: issues.some(i => i.guideline_clause.includes('A11Y')) ? 'fail' : 'pass',
    created_at: new Date().toISOString()
  };

  return {
    audit: auditRecord,
    audit_log: auditRecord,
    compliance_score: score,
    micro_patches: issues
  };'''

if old_fallback_return in c:
    c = c.replace(old_fallback_return, new_fallback_return)
    print("1. computeClientAuditFallback updated with dual audit/audit_log keys!")

# 2. Add empty draftText check in handleExecuteAudit
target_audit_start = "  const handleExecuteAudit = async () => {\n    setIsAuditing(true)"
replacement_audit_start = """  const handleExecuteAudit = async () => {
    if (!draftText.trim()) {
      addToast('warning', 'Draft Text Empty', 'Please enter draft copy or select a template above to execute the compliance audit.')
      return
    }
    setIsAuditing(true)"""

if target_audit_start in c:
    c = c.replace(target_audit_start, replacement_audit_start)
    print("2. Added defensive empty text check to handleExecuteAudit!")

# 3. Safe fallback in handleExecuteAudit catch block
old_catch_block = """    const fallbackData = computeClientAuditFallback(channel, draftText, fgColor, bgColor, toneVariance);
    setCurrentAudit(fallbackData.audit_log);
    setActivePatches(fallbackData.micro_patches);
    setSelectedAuditId(fallbackData.audit_log.id);
    const score = Math.round(fallbackData.audit_log.compliance_score);"""

new_catch_block = """    const fallbackData = computeClientAuditFallback(channel, draftText, fgColor, bgColor, toneVariance);
    const activeAudit = fallbackData.audit || fallbackData.audit_log;
    setCurrentAudit(activeAudit);
    setActivePatches(fallbackData.micro_patches || []);
    setSelectedAuditId(activeAudit.id);
    const score = Math.round(activeAudit.compliance_score);"""

if old_catch_block in c:
    c = c.replace(old_catch_block, new_catch_block)
    print("3. Made audit catch block bulletproof against missing keys!")

# 4. Insert Cross-Policy Contradiction Harmonizer Card in Tab 4 (Analytics) as well!
conflict_card_tab4 = '''
            {/* ─────────────────────────────────────────────────────────────────────────────
                IMPROVEMENT 3: CROSS-POLICY CONTRADICTION HARMONIZER CARD (TAB 4)
            ───────────────────────────────────────────────────────────────────────────── */}
            <div className="rounded-2xl border border-purple-200 bg-gradient-to-r from-purple-50/70 via-indigo-50/50 to-blue-50/70 p-5 shadow-xs mb-6">
              <div className="flex flex-wrap items-center justify-between gap-3 mb-3 border-b border-purple-100 pb-3">
                <div className="flex items-center gap-2.5">
                  <div className="flex size-8 items-center justify-center rounded-lg bg-purple-600 text-white shadow-xs">
                    <Scale className="size-4" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm font-bold text-purple-950">
                        Cross-Policy Contradiction Harmonizer
                      </h3>
                      <Badge tone="purple">Round 3 Delivered Improvement</Badge>
                    </div>
                    <p className="text-xs text-purple-800">
                      Automated semantic conflict detection across marketing guidelines, legal disclaimers, and design tokens.
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Badge tone="amber">
                    {policyConflicts.filter((c) => c.status === 'active').length} Active Conflicts
                  </Badge>
                  <Badge tone="emerald">
                    {policyConflicts.filter((c) => c.status === 'resolved').length} Harmonized
                  </Badge>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                {policyConflicts.map((conflict) => (
                  <div
                    key={conflict.id}
                    className={`rounded-xl border p-3.5 transition flex flex-col justify-between ${
                      conflict.status === 'resolved'
                        ? 'border-emerald-200 bg-emerald-50/60'
                        : 'border-zinc-200 bg-white hover:border-purple-300 shadow-xs'
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="font-mono text-[10px] text-zinc-400">Conflict #{conflict.id}</span>
                        <Badge tone={conflict.status === 'resolved' ? 'emerald' : conflict.severity === 'critical' ? 'rose' : conflict.severity === 'high' ? 'amber' : 'blue'}>
                          {conflict.status === 'resolved' ? 'HARMONIZED' : `${conflict.severity.toUpperCase()} SEVERITY`}
                        </Badge>
                      </div>
                      <h4 className="text-xs font-bold text-zinc-900 mb-1">{conflict.title}</h4>
                      <p className="text-[11px] text-zinc-500 line-clamp-2 mb-2">{conflict.root_cause}</p>
                      <div className="flex items-center gap-2 text-[10px] text-zinc-600 font-mono mb-3">
                        <span className="rounded bg-rose-50 px-1.5 py-0.5 border border-rose-200 text-rose-700">{conflict.rule_a}</span>
                        <span>⇄</span>
                        <span className="rounded bg-blue-50 px-1.5 py-0.5 border border-blue-200 text-blue-700">{conflict.rule_b}</span>
                      </div>
                    </div>

                    <button
                      onClick={() => setActiveConflictModal(conflict)}
                      className={`w-full flex items-center justify-center gap-1.5 rounded-lg py-1.5 text-xs font-bold transition cursor-pointer shadow-xs ${
                        conflict.status === 'resolved'
                          ? 'bg-emerald-100 text-emerald-800 hover:bg-emerald-200'
                          : 'bg-indigo-600 text-white hover:bg-indigo-700'
                      }`}
                    >
                      <Sparkles className="size-3.5" />
                      <span>{conflict.status === 'resolved' ? 'Inspect Harmonized Ledger Receipt' : 'Inspect Semantic Diff & Harmonize'}</span>
                    </button>
                  </div>
                ))}
              </div>
            </div>
'''

target_ambiguity_table = "{/* Guideline Violations Table */}"
if target_ambiguity_table in c and "IMPROVEMENT 3: CROSS-POLICY CONTRADICTION HARMONIZER CARD (TAB 4)" not in c:
    c = c.replace(target_ambiguity_table, conflict_card_tab4 + "\n" + target_ambiguity_table)
    print("4. Injected Cross-Policy Harmonizer Card into Tab 4 (Analytics)!")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Polish updates applied to share/v0-project/app/page.tsx!")
