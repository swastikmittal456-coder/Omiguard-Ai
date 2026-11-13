page_path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Diff Merger Modal injection
# ─────────────────────────────────────────────────────────────────────────────
diff_merger_modal = '''
      {/* ─────────────────────────────────────────────────────────────────────────────
          IMPROVEMENT 3: CROSS-POLICY CONTRADICTION INTERACTIVE DIFF MERGER MODAL
      ───────────────────────────────────────────────────────────────────────────── */}
      {activeConflictModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-4xl rounded-2xl border border-zinc-200 bg-white p-6 shadow-2xl animate-in fade-in zoom-in-95 duration-150 max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-zinc-100 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <Badge tone={activeConflictModal.severity === 'critical' ? 'rose' : activeConflictModal.severity === 'high' ? 'amber' : 'blue'}>
                    {activeConflictModal.severity.toUpperCase()} SEVERITY
                  </Badge>
                  <span className="text-xs font-mono text-zinc-400">Conflict #{activeConflictModal.id}</span>
                  <Badge tone="purple">{activeConflictModal.conflict_type}</Badge>
                </div>
                <h3 className="mt-1.5 text-lg font-bold text-zinc-950">
                  {activeConflictModal.title}
                </h3>
                <p className="mt-0.5 text-xs text-zinc-500">
                  Semantic Harmonizer &amp; Deterministic Clause Diff Engine (Round 3 Delivered Feature)
                </p>
              </div>
              <button
                onClick={() => setActiveConflictModal(null)}
                className="rounded-lg p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 cursor-pointer"
              >
                <X className="size-5" />
              </button>
            </div>

            {/* Root Cause Diagnostics */}
            <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50/70 p-3.5 text-xs text-amber-950">
              <div className="flex items-start gap-2">
                <AlertTriangle className="size-4 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Contradiction Diagnostic: </span>
                  {activeConflictModal.root_cause}
                </div>
              </div>
            </div>

            {/* 3-Column Diff View */}
            <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
              {/* Clause A */}
              <div className="rounded-xl border border-rose-200 bg-rose-50/40 p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-rose-700">
                      Conflicting Rule A
                    </span>
                    <span className="font-mono text-[10px] bg-white px-1.5 py-0.5 rounded border border-rose-200 text-rose-700 font-bold">
                      {activeConflictModal.rule_a}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-800 leading-relaxed font-mono bg-white p-2.5 rounded-lg border border-rose-100">
                    &quot;{activeConflictModal.clause_a_text}&quot;
                  </p>
                </div>
                <div className="mt-3 text-[10px] text-rose-600 font-medium">
                  Direct collision with jurisdictional standard.
                </div>
              </div>

              {/* Clause B */}
              <div className="rounded-xl border border-blue-200 bg-blue-50/40 p-4 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-blue-700">
                      Conflicting Rule B
                    </span>
                    <span className="font-mono text-[10px] bg-white px-1.5 py-0.5 rounded border border-blue-200 text-blue-700 font-bold">
                      {activeConflictModal.rule_b}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-800 leading-relaxed font-mono bg-white p-2.5 rounded-lg border border-blue-100">
                    &quot;{activeConflictModal.clause_b_text}&quot;
                  </p>
                </div>
                <div className="mt-3 text-[10px] text-blue-600 font-medium">
                  Enforces mandatory compliance restriction.
                </div>
              </div>

              {/* Merged Consensus */}
              <div className="rounded-xl border border-emerald-300 bg-emerald-50/60 p-4 flex flex-col justify-between ring-1 ring-emerald-500/20">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 flex items-center gap-1">
                      <Sparkles className="size-3 text-emerald-600" /> Harmonized Clause
                    </span>
                    <span className="text-[10px] bg-emerald-600 text-white px-1.5 py-0.5 rounded font-bold">
                      Recommended
                    </span>
                  </div>
                  <p className="text-xs text-emerald-950 leading-relaxed font-mono bg-white p-2.5 rounded-lg border border-emerald-200 font-bold">
                    &quot;{activeConflictModal.harmonized_text}&quot;
                  </p>
                </div>
                <div className="mt-3 text-[10px] text-emerald-700 font-medium flex items-center gap-1">
                  <CheckCircle2 className="size-3 text-emerald-600" />
                  Preserves regulatory integrity without breaking copy virality.
                </div>
              </div>
            </div>

            {/* Resolution Rationale Notes */}
            <div className="mt-4">
              <label className="block text-xs font-semibold text-zinc-700 mb-1">
                Legal Counsel Harmonization Rationale &amp; Audit Trail Note
              </label>
              <input
                type="text"
                value={diffResolutionNotes}
                onChange={(e) => setDiffResolutionNotes(e.target.value)}
                placeholder="e.g. Standardized via qualified safe-harbor exception pursuant to Legal Counsel review..."
                className="w-full rounded-xl border border-zinc-200 bg-zinc-50 p-2.5 text-xs text-zinc-900 focus:border-indigo-500 focus:bg-white focus:outline-none"
              />
            </div>

            {/* Resolution Action Buttons */}
            <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-zinc-100 pt-4">
              <div className="text-[11px] text-zinc-500">
                Resolution creates an immutable entry in SQLite table <code className="font-bold text-zinc-700">policy_conflicts</code>.
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={() => handleResolveConflict(activeConflictModal.id, 'prioritize_b')}
                  disabled={resolvingConflict}
                  className="rounded-lg border border-blue-300 bg-white px-3 py-1.5 text-xs font-bold text-blue-700 hover:bg-blue-50 transition cursor-pointer"
                >
                  Prioritize Rule B
                </button>
                <button
                  onClick={() => handleResolveConflict(activeConflictModal.id, 'prioritize_a')}
                  disabled={resolvingConflict}
                  className="rounded-lg border border-rose-300 bg-white px-3 py-1.5 text-xs font-bold text-rose-700 hover:bg-rose-50 transition cursor-pointer"
                >
                  Prioritize Rule A
                </button>
                <button
                  onClick={() => handleResolveConflict(activeConflictModal.id, 'merge')}
                  disabled={resolvingConflict}
                  className="flex items-center gap-1.5 rounded-lg bg-emerald-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-emerald-700 shadow-xs transition cursor-pointer"
                >
                  <Sparkles className="size-3.5" />
                  <span>Merge &amp; Commit to Ledger</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
'''

target_cert_modal = "{showCertificateModal && ("
if target_cert_modal in content and "IMPROVEMENT 3: CROSS-POLICY CONTRADICTION INTERACTIVE DIFF MERGER MODAL" not in content:
    content = content.replace(target_cert_modal, diff_merger_modal + "\n" + target_cert_modal)
    print("Inserted Diff Merger Modal before Certificate Modal!")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Modal injection done!")
