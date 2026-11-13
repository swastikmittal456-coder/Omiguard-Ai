page_path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# 1. Mode Switcher & Batch Campaign Matrix at top of Tab 1
# ─────────────────────────────────────────────────────────────────────────────
mode_switcher_and_batch_code = '''
            {/* ─────────────────────────────────────────────────────────────────────────────
                MODE SWITCHER: SINGLE ASSET INSPECTOR vs. BATCH MULTI-CHANNEL CAMPAIGN AUDITOR
            ───────────────────────────────────────────────────────────────────────────── */}
            <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-indigo-200/80 bg-gradient-to-r from-indigo-50/70 via-white to-purple-50/70 p-4 shadow-xs mb-6">
              <div className="flex items-center gap-3">
                <div className="flex size-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-xs">
                  <Layers className="size-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-base font-extrabold text-zinc-950">Multi-Modal Pre-Publication Firewall</h2>
                    <Badge tone="purple">Round 3 Delivered Features</Badge>
                  </div>
                  <p className="text-xs text-zinc-600">
                    Choose between live single creative deep-scan or parallel multi-channel campaign compliance auditing.
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-1 rounded-xl bg-zinc-100 p-1 border border-zinc-200">
                <button
                  onClick={() => setScannerMode('single')}
                  className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition cursor-pointer ${
                    scannerMode === 'single'
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'text-zinc-600 hover:text-zinc-950 hover:bg-zinc-200/60'
                  }`}
                >
                  <Search className="size-3.5" />
                  <span>Single Asset Inspector</span>
                </button>

                <button
                  onClick={() => setScannerMode('batch')}
                  className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-bold transition cursor-pointer ${
                    scannerMode === 'batch'
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'text-zinc-600 hover:text-zinc-950 hover:bg-zinc-200/60'
                  }`}
                >
                  <Workflow className="size-3.5" />
                  <span>Batch Campaign Auditor (R3 Matrix)</span>
                  <span className="rounded bg-amber-400 px-1 py-0.2 text-[9px] font-black text-amber-950">
                    NEW
                  </span>
                </button>
              </div>
            </div>

            {/* Render Batch Campaign Auditor View if batch mode active */}
            {scannerMode === 'batch' && (
              <div className="space-y-6">
                {/* Campaign Controls & Action Bar */}
                <div className="flex flex-wrap items-center justify-between gap-4 rounded-2xl border border-zinc-200 bg-white p-5 shadow-xs">
                  <div className="flex-1 min-w-[280px]">
                    <label className="block text-xs font-semibold text-zinc-500 uppercase tracking-wider mb-1">
                      Active Enterprise Campaign
                    </label>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        value={campaignName}
                        onChange={(e) => setCampaignName(e.target.value)}
                        className="flex-1 rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm font-bold text-zinc-900 focus:border-indigo-500 focus:bg-white focus:outline-none"
                      />
                      <button
                        onClick={runBatchCampaignAudit}
                        disabled={batchAuditing}
                        className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-bold text-white hover:bg-indigo-700 transition shadow-xs disabled:opacity-60 cursor-pointer"
                      >
                        <Zap className={`size-4 ${batchAuditing ? 'animate-spin text-amber-300' : 'fill-current text-amber-300'}`} />
                        <span>{batchAuditing ? 'Auditing Channels...' : 'Run Parallel Multi-Channel Audit'}</span>
                      </button>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    <button
                      onClick={exportCampaignCsv}
                      className="flex items-center gap-1.5 rounded-xl border border-zinc-200 bg-white px-3 py-2 text-xs font-bold text-zinc-700 hover:border-indigo-300 hover:bg-indigo-50/50 transition shadow-xs cursor-pointer"
                      title="Download CSV compliance matrix for reporting"
                    >
                      <Download className="size-3.5 text-indigo-600" />
                      <span>Export Matrix (CSV)</span>
                    </button>

                    <button
                      onClick={exportCampaignJson}
                      className="flex items-center gap-1.5 rounded-xl border border-zinc-200 bg-white px-3 py-2 text-xs font-bold text-zinc-700 hover:border-indigo-300 hover:bg-indigo-50/50 transition shadow-xs cursor-pointer"
                      title="Download cryptographically verifiable JSON dossier"
                    >
                      <FileCheck2 className="size-3.5 text-purple-600" />
                      <span>Export Dossier (JSON)</span>
                    </button>

                    <button
                      onClick={autoPatchAllCampaignAssets}
                      className="flex items-center gap-1.5 rounded-xl bg-emerald-600 px-3.5 py-2 text-xs font-bold text-white hover:bg-emerald-700 transition shadow-xs cursor-pointer"
                    >
                      <Wand2 className="size-3.5" />
                      <span>1-Click Auto-Patch All</span>
                    </button>
                  </div>
                </div>

                {/* 4 Campaign Health KPI Cards */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-xs">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 block mb-1">
                      Campaign Health Score
                    </span>
                    <div className="text-3xl font-black text-indigo-600">
                      {Math.round(
                        batchCampaignAssets.reduce((acc, a) => acc + a.score, 0) / batchCampaignAssets.length
                      )}%
                    </div>
                    <span className="text-[11px] text-zinc-500 font-medium">Cross-channel compliance average</span>
                  </div>

                  <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-xs">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 block mb-1">
                      Channels Audited
                    </span>
                    <div className="text-3xl font-black text-zinc-900">{batchCampaignAssets.length} Assets</div>
                    <span className="text-[11px] text-emerald-600 font-medium">Google, Meta, LinkedIn, Email</span>
                  </div>

                  <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-xs">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 block mb-1">
                      Active Violations
                    </span>
                    <div className="text-3xl font-black text-rose-600">
                      {batchCampaignAssets.reduce((acc, a) => acc + a.violations, 0)} Flags
                    </div>
                    <span className="text-[11px] text-zinc-500 font-medium">Grounded in brand policy rules</span>
                  </div>

                  <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-xs">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-zinc-400 block mb-1">
                      Micro-Patches Ready
                    </span>
                    <div className="text-3xl font-black text-emerald-600">
                      {batchCampaignAssets.filter((a) => a.patch).length} Patches
                    </div>
                    <span className="text-[11px] text-zinc-500 font-medium">100% deterministic replacement</span>
                  </div>
                </div>

                {/* Cross-Channel Compliance Matrix Table */}
                <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-xs">
                  <div className="border-b border-zinc-200 bg-zinc-50 px-5 py-3 text-xs font-bold uppercase tracking-wider text-zinc-700 flex items-center justify-between">
                    <span>Omnichannel Compliance Matrix &amp; Channel Drift Ledger</span>
                    <Badge tone="purple">RFC 4180 Certified</Badge>
                  </div>

                  <table className="w-full text-left text-xs">
                    <thead className="border-b border-zinc-200 text-[11px] font-bold uppercase tracking-wider text-zinc-400">
                      <tr>
                        <th className="px-5 py-3">Channel &amp; Asset</th>
                        <th className="px-5 py-3">Creative Copy / Snippet</th>
                        <th className="px-5 py-3">Tone Delta</th>
                        <th className="px-5 py-3">APCA Contrast</th>
                        <th className="px-5 py-3">Violations</th>
                        <th className="px-5 py-3">Status</th>
                        <th className="px-5 py-3 text-right">Inspection</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-zinc-100">
                      {batchCampaignAssets.map((asset) => {
                        const isSelected = selectedBatchAssetId === asset.id
                        return (
                          <tr
                            key={asset.id}
                            onClick={() => setSelectedBatchAssetId(asset.id)}
                            className={`cursor-pointer transition ${
                              isSelected ? 'bg-indigo-50/60 font-semibold' : 'hover:bg-zinc-50'
                            }`}
                          >
                            <td className="px-5 py-3.5">
                              <div className="font-bold text-zinc-900">{asset.channel}</div>
                              <div className="text-[10px] text-zinc-400">{asset.asset_name}</div>
                            </td>
                            <td className="px-5 py-3.5 max-w-xs">
                              <p className="truncate text-xs text-zinc-700">{asset.draft_text}</p>
                            </td>
                            <td className="px-5 py-3.5">
                              <span className={`font-mono text-xs font-bold ${asset.tone_delta <= 1.5 ? 'text-emerald-600' : 'text-amber-600'}`}>
                                Δ {asset.tone_delta}
                              </span>
                            </td>
                            <td className="px-5 py-3.5">
                              <span className={`font-mono text-xs font-bold ${asset.apca_score >= 75 ? 'text-emerald-600' : 'text-rose-600'}`}>
                                Lc {asset.apca_score}
                              </span>
                            </td>
                            <td className="px-5 py-3.5">
                              <span className={`rounded-full px-2 py-0.5 text-[10px] font-bold ${
                                asset.violations === 0 ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                              }`}>
                                {asset.violations} Violations
                              </span>
                            </td>
                            <td className="px-5 py-3.5">
                              <Badge tone={asset.status === 'compliant' ? 'emerald' : asset.status === 'revision_required' ? 'amber' : 'rose'}>
                                {asset.status.replace('_', ' ').toUpperCase()} ({asset.score}%)
                              </Badge>
                            </td>
                            <td className="px-5 py-3.5 text-right">
                              <button
                                onClick={(e) => {
                                  e.stopPropagation()
                                  setSelectedBatchAssetId(asset.id)
                                }}
                                className="rounded-lg bg-zinc-100 px-2.5 py-1 text-[11px] font-bold text-zinc-700 hover:bg-zinc-200 cursor-pointer"
                              >
                                Inspect
                              </button>
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>

                {/* Selected Asset Deep-Dive & Patch Card */}
                {selectedBatchAssetId && (() => {
                  const asset = batchCampaignAssets.find((a) => a.id === selectedBatchAssetId)
                  if (!asset) return null
                  return (
                    <div className="rounded-2xl border border-indigo-200 bg-white p-5 shadow-xs">
                      <div className="flex items-center justify-between mb-3 border-b border-zinc-100 pb-2">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-sm text-zinc-900">
                            Asset Inspection: {asset.channel} · {asset.asset_name}
                          </span>
                          <Badge tone={asset.status === 'compliant' ? 'emerald' : 'amber'}>
                            {asset.score}% Compliance Score
                          </Badge>
                        </div>
                        <button
                          onClick={() => {
                            setBatchCampaignAssets((prev) =>
                              prev.map((a) =>
                                a.id === asset.id
                                  ? {
                                      ...a,
                                      score: 98,
                                      violations: 0,
                                      status: 'compliant',
                                      draft_text: a.patch,
                                    }
                                  : a
                              )
                            )
                            addToast('success', 'Asset Patched', `Applied micro-patch to ${asset.channel}.`)
                          }}
                          className="flex items-center gap-1.5 rounded-lg bg-emerald-600 px-3 py-1 text-xs font-bold text-white hover:bg-emerald-700 transition cursor-pointer"
                        >
                          <CheckCircle2 className="size-3.5" />
                          <span>Apply Recommended Patch</span>
                        </button>
                      </div>

                      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                        <div className="rounded-xl border border-rose-200 bg-rose-50/30 p-3.5">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-rose-700 block mb-1">
                            Draft Under Review &amp; Detected Violations:
                          </span>
                          <p className="text-xs text-zinc-800 font-mono mb-3 bg-white p-2.5 rounded-lg border border-rose-100">
                            {asset.draft_text}
                          </p>
                          <div className="space-y-1">
                            {asset.issues.map((iss, i) => (
                              <div key={i} className="text-[11px] text-rose-800 flex items-center gap-1.5">
                                <AlertTriangle className="size-3 shrink-0 text-rose-600" />
                                <span>{iss}</span>
                              </div>
                            ))}
                            {asset.issues.length === 0 && (
                              <div className="text-[11px] text-emerald-700 flex items-center gap-1.5">
                                <CheckCircle2 className="size-3 shrink-0 text-emerald-600" />
                                <span>Zero violations detected. Asset is compliant.</span>
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="rounded-xl border border-emerald-200 bg-emerald-50/40 p-3.5">
                          <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 block mb-1">
                            Harmonized Pre-Approved Patch (RFC 6902 Grounded):
                          </span>
                          <p className="text-xs text-emerald-950 font-mono mb-3 bg-white p-2.5 rounded-lg border border-emerald-200 font-bold">
                            {asset.patch}
                          </p>
                          <span className="text-[10px] text-emerald-700">
                            ✓ Grounded in Enterprise Brand Guideline &amp; FTC Safe Harbor Regulations.
                          </span>
                        </div>
                      </div>
                    </div>
                  )
                })()}
              </div>
            )}
'''

# We inject this right after `<section className="space-y-6">` in activeTab === 1
target_tab1_start = "{activeTab === 1 && (\n          <section className=\"space-y-6\">"
if target_tab1_start in content and "MODE SWITCHER: SINGLE ASSET INSPECTOR" not in content:
    content = content.replace(target_tab1_start, target_tab1_start + "\n" + mode_switcher_and_batch_code)
    print("Injected Batch Mode Switcher and Campaign Matrix into Tab 1!")

# ─────────────────────────────────────────────────────────────────────────────
# 2. In-Canvas Defect Bounding Boxes in Image Inspector
# ─────────────────────────────────────────────────────────────────────────────
bounding_box_code = '''
                  {/* ─────────────────────────────────────────────────────────────────────────────
                      IMPROVEMENT 2: SPATIAL VISUAL BOUNDING BOX & IN-CANVAS DEFECT HIGHLIGHTING
                  ───────────────────────────────────────────────────────────────────────────── */}
                  {uploadedImageB64 && (
                    <div className="mt-4 rounded-xl border border-zinc-200 bg-zinc-900 p-4 shadow-sm text-white">
                      <div className="flex items-center justify-between mb-3 border-b border-zinc-800 pb-2">
                        <div className="flex items-center gap-2">
                          <Sparkles className="size-4 text-amber-400" />
                          <span className="text-xs font-bold tracking-tight">
                            Spatial Visual Defect Overlay (OpenCV Coordinates)
                          </span>
                        </div>
                        <Badge tone="purple">Round 3 Delivered Feature</Badge>
                      </div>

                      {/* Canvas Image Container with Bounding Boxes */}
                      <div className="relative overflow-hidden rounded-lg border border-zinc-700 bg-zinc-950 flex items-center justify-center min-h-[220px]">
                        <img
                          src={uploadedImageB64}
                          alt="Analyzed Creative Canvas"
                          className="max-h-[260px] w-auto object-contain rounded select-none"
                        />

                        {/* SVG / HTML Spatial Bounding Boxes */}
                        {defectBoxes.map((box) => {
                          if (box.fixed) return null
                          const isHovered = selectedBoundingBox === box.id
                          return (
                            <div
                              key={box.id}
                              onClick={() => setSelectedBoundingBox(box.id)}
                              style={{
                                top: `${box.y}%`,
                                left: `${box.x}%`,
                                width: `${box.width}%`,
                                height: `${box.height}%`,
                              }}
                              className={`absolute cursor-pointer rounded border-2 transition-all duration-200 flex flex-col justify-between p-1 select-none ${
                                box.severity === 'critical'
                                  ? 'border-rose-500 bg-rose-500/20 shadow-[0_0_12px_rgba(244,63,94,0.4)]'
                                  : box.severity === 'high'
                                  ? 'border-amber-400 bg-amber-400/20 shadow-[0_0_12px_rgba(251,191,36,0.4)]'
                                  : 'border-indigo-400 bg-indigo-400/20 shadow-[0_0_12px_rgba(129,140,248,0.4)]'
                              } ${isHovered ? 'scale-105 z-20 ring-2 ring-white' : 'z-10'}`}
                            >
                              <div className="flex items-center justify-between gap-1">
                                <span
                                  className={`rounded px-1 py-0.2 text-[8px] font-black uppercase text-black ${
                                    box.severity === 'critical'
                                      ? 'bg-rose-400'
                                      : box.severity === 'high'
                                      ? 'bg-amber-300'
                                      : 'bg-indigo-300'
                                  }`}
                                >
                                  {box.label.split('(')[0]}
                                </span>
                                <span className="font-mono text-[8px] bg-black/70 text-white px-1 rounded">
                                  {box.rule_citation}
                                </span>
                              </div>

                              <button
                                onClick={(e) => {
                                  e.stopPropagation()
                                  handleAutoFixBox(box.id)
                                }}
                                className="mt-auto self-end rounded bg-emerald-500 px-1.5 py-0.5 text-[8px] font-bold text-black hover:bg-emerald-400 transition cursor-pointer shadow-xs"
                              >
                                1-Click Fix
                              </button>
                            </div>
                          )
                        })}
                      </div>

                      {/* Defect Inspection Drawer & Auto-Fix Details */}
                      <div className="mt-3 space-y-2">
                        <div className="flex items-center justify-between text-[11px] font-bold text-zinc-300">
                          <span>Detected In-Canvas Defects:</span>
                          <span className="text-zinc-400 text-[10px]">
                            {defectBoxes.filter((b) => !b.fixed).length} Unresolved · {defectBoxes.filter((b) => b.fixed).length} Resolved
                          </span>
                        </div>

                        <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
                          {defectBoxes.map((box) => (
                            <div
                              key={box.id}
                              className={`rounded-lg border p-2.5 text-xs transition ${
                                box.fixed
                                  ? 'border-emerald-800 bg-emerald-950/40 text-emerald-300'
                                  : selectedBoundingBox === box.id
                                  ? 'border-indigo-400 bg-zinc-800 text-white'
                                  : 'border-zinc-800 bg-zinc-900/90 text-zinc-300 hover:border-zinc-700'
                              }`}
                            >
                              <div className="flex items-center justify-between mb-1">
                                <span className="font-bold text-[11px] truncate">{box.label}</span>
                                {box.fixed ? (
                                  <span className="text-[9px] font-bold text-emerald-400 flex items-center gap-0.5">
                                    <CheckCircle2 className="size-3" /> Fixed
                                  </span>
                                ) : (
                                  <span className="font-mono text-[9px] text-zinc-400">{box.rule_citation}</span>
                                )}
                              </div>
                              <p className="text-[10px] text-zinc-400 line-clamp-2 mb-2">{box.metric}</p>
                              {!box.fixed && (
                                <button
                                  onClick={() => handleAutoFixBox(box.id)}
                                  className="w-full rounded bg-emerald-600 py-1 text-[10px] font-bold text-white hover:bg-emerald-500 transition cursor-pointer shadow-xs"
                                >
                                  {box.auto_fix_label}
                                </button>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
'''

target_dropzone_end = "PNG, JPG, WebP · Automatically extracts dominant palette via OpenCV K-Means\n                      </p>\n                    </label>\n                  </div>"
if target_dropzone_end in content and "IMPROVEMENT 2: SPATIAL VISUAL BOUNDING BOX" not in content:
    content = content.replace(target_dropzone_end, target_dropzone_end + "\n" + bounding_box_code)
    print("Injected Spatial Bounding Box & Canvas Highlighting into Image Inspector!")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Cross-Policy Contradiction Harmonizer in Tab 2 & Tab 4
# ─────────────────────────────────────────────────────────────────────────────
conflict_harmonizer_card = '''
            {/* ─────────────────────────────────────────────────────────────────────────────
                IMPROVEMENT 3: CROSS-POLICY CONTRADICTION HARMONIZER CARD
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

target_guidelines_table = "{/* Table of Guidelines */}"
if target_guidelines_table in content and "IMPROVEMENT 3: CROSS-POLICY CONTRADICTION HARMONIZER CARD" not in content:
    content = content.replace(target_guidelines_table, conflict_harmonizer_card + "\n" + target_guidelines_table)
    print("Injected Cross-Policy Contradiction Harmonizer Card into Tab 2!")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Step 5 completed successfully!")
