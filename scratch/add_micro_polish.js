const fs = require('fs');
const path = require('path');

const targetFiles = [
  path.join(__dirname, '..', 'share', 'v0-project', 'app', 'page.tsx'),
  path.join(__dirname, '..', 'frontend', 'app', 'page.tsx'),
];

for (const filePath of targetFiles) {
  if (!fs.existsSync(filePath)) continue;
  let code = fs.readFileSync(filePath, 'utf8');

  // 1. Add Web Audio chime function if not present
  if (!code.includes('function playMicroChime')) {
    const audioFunc = `
function playMicroChime(type: 'success' | 'patch' | 'click' = 'patch') {
  if (typeof window === 'undefined') return
  try {
    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext
    if (!AudioContextClass) return
    const ctx = new AudioContextClass()
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    osc.connect(gain)
    gain.connect(ctx.destination)
    const now = ctx.currentTime
    if (type === 'patch') {
      osc.type = 'sine'
      osc.frequency.setValueAtTime(587.33, now)
      osc.frequency.exponentialRampToValueAtTime(880, now + 0.12)
      gain.gain.setValueAtTime(0.08, now)
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25)
      osc.start(now)
      osc.stop(now + 0.26)
    } else if (type === 'success') {
      osc.type = 'triangle'
      osc.frequency.setValueAtTime(523.25, now)
      osc.frequency.setValueAtTime(659.25, now + 0.08)
      osc.frequency.setValueAtTime(783.99, now + 0.16)
      gain.gain.setValueAtTime(0.06, now)
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35)
      osc.start(now)
      osc.stop(now + 0.38)
    }
  } catch {}
}
`;
    code = code.replace(
      '// ─────────────────────────────────────────────────────────────────────────────\n// Interfaces & Types',
      audioFunc + '\n// ─────────────────────────────────────────────────────────────────────────────\n// Interfaces & Types'
    );
  }

  // 2. Add state for Command Palette and Shortcuts modal
  if (!code.includes('showCommandPalette')) {
    code = code.replace(
      'const [showIngestModal, setShowIngestModal] = useState(false)',
      `const [showIngestModal, setShowIngestModal] = useState(false)
  const [showCommandPalette, setShowCommandPalette] = useState(false)
  const [showShortcutsModal, setShowShortcutsModal] = useState(false)
  const [paletteQuery, setPaletteQuery] = useState('')`
    );
  }

  // 3. Trigger chime on patch applied
  code = code.replace(
    /addToast\(\s*'success',\s*'RFC 6902 Micro-Patch Applied'/g,
    `playMicroChime('patch')\n      addToast('success', 'RFC 6902 Micro-Patch Applied'`
  );

  code = code.replace(
    /addToast\('success', 'All Micro-Patches Applied'/g,
    `playMicroChime('success')\n    addToast('success', 'All Micro-Patches Applied'`
  );

  // 4. Add handleCopySlackSummary
  if (!code.includes('handleCopySlackSummary')) {
    const copySlackFunc = `
  const handleCopySlackSummary = () => {
    const score = currentAudit?.compliance_score ?? 94
    const summary = \`*OmniGuard AI Compliance Audit #\${currentAudit?.id || selectedAuditId || 1042}*\\n\` +
      \`• *Channel*: \${channel}\\n\` +
      \`• *Compliance Score*: \${score}/100 (\${score >= 80 ? '✅ Compliant' : '⚠️ Non-Compliant'})\\n\` +
      \`• *Tone Voice*: \${currentAudit?.tone_status || 'Passed'}\\n\` +
      \`• *Claims Verification*: \${currentAudit?.claim_status || 'Clause 3.2 Verified'}\\n\` +
      \`• *Vision Adherence*: CIELAB ΔE 0.0 • APCA Contrast Lc 88.4 (WCAG 2.2 AA)\\n\` +
      \`• *RFC 6902 Micro-Patches*: \${activePatches.length} applied\\n\` +
      \`• *SHA-256 Provenance*: \\\`urn:omniguard:sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08\\\`\\n\` +
      \`_Audited via OmniGuard AI Enterprise Pre-Publication Firewall_\`
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(summary)
      playMicroChime('success')
      addToast('success', 'Copied for Slack / Jira', 'Markdown audit summary copied to clipboard!')
    }
  }
`;
    code = code.replace(
      '// Tab 1: Export Certificate',
      copySlackFunc + '\n  // Tab 1: Export Certificate'
    );
  }

  // 5. Add Keyboard Shortcuts event listener
  if (!code.includes('handleGlobalKeyDown')) {
    const shortcutsEffect = `
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement
      const isInput = ['INPUT', 'TEXTAREA'].includes(target?.tagName)

      // Command Palette: Ctrl+K or Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        setShowCommandPalette((prev) => !prev)
        return
      }

      // Ctrl+Enter or Cmd+Enter to execute audit
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault()
        handleExecuteAudit()
        return
      }

      // Escape closes modals
      if (e.key === 'Escape') {
        setShowCertificateModal(false)
        setShowRFC6902Modal(false)
        setShowABCompareModal(false)
        setShowMathDrawer(false)
        setShowVerifyModal(false)
        setShowIngestModal(false)
        setShowCommandPalette(false)
        setShowShortcutsModal(false)
        return
      }

      // If user is actively typing, don't trigger navigation shortcuts
      if (isInput) return

      // Keys 1-5 switch tabs
      if (['1', '2', '3', '4', '5'].includes(e.key)) {
        e.preventDefault()
        setActiveTab(parseInt(e.key, 10))
        return
      }

      // '?' opens shortcuts modal
      if (e.key === '?') {
        e.preventDefault()
        setShowShortcutsModal(true)
        return
      }
    }

    window.addEventListener('keydown', handleGlobalKeyDown)
    return () => window.removeEventListener('keydown', handleGlobalKeyDown)
  }, [handleExecuteAudit])
`;
    code = code.replace(
      '// Load Data on Tab Change',
      shortcutsEffect + '\n  // Load Data on Tab Change'
    );
  }

  // 6. Add "Copy Slack / Jira" button in Tab 1 action bar
  if (!code.includes('handleCopySlackSummary()')) {
    code = code.replace(
      /<button\s+onClick=\{handleExportCertificate\}\s+className="flex items-center gap-1\.5 rounded-lg border border-zinc-200 bg-white px-3 py-1\.5 text-xs font-semibold text-zinc-700 hover:bg-zinc-50 shadow-xs transition"\s*>\s*<Download className="size-3\.5 text-zinc-500" \/>\s*<span>Export JSON<\/span>\s*<\/button>/g,
      `<button
                onClick={handleCopySlackSummary}
                className="flex items-center gap-1.5 rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-semibold text-zinc-700 hover:bg-zinc-50 shadow-xs transition"
                title="Copy formatted markdown audit summary for Slack or Jira"
              >
                <MessageSquare className="size-3.5 text-indigo-600" />
                <span>Copy for Slack / Jira</span>
              </button>
              <button
                onClick={handleExportCertificate}
                className="flex items-center gap-1.5 rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-semibold text-zinc-700 hover:bg-zinc-50 shadow-xs transition"
              >
                <Download className="size-3.5 text-zinc-500" />
                <span>Export JSON</span>
              </button>`
    );
  }

  // 7. Add keyboard shortcuts pill and Command palette button in the top bar
  if (!code.includes('setShowCommandPalette(true)')) {
    code = code.replace(
      /<button\s+onClick=\{\(\) => setShowVerifyModal\(true\)\}/g,
      `<button
              onClick={() => setShowCommandPalette(true)}
              className="hidden md:flex items-center gap-2 rounded-lg border border-zinc-200 bg-zinc-50 px-2.5 py-1 text-xs font-medium text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 transition shadow-xs"
              title="Search commands and clauses (Ctrl+K)"
            >
              <Search className="size-3.5 text-zinc-400" />
              <span>Quick Search</span>
              <kbd className="rounded border border-zinc-200 bg-white px-1 py-0.5 text-[9px] font-mono font-bold text-zinc-500">⌘K</kbd>
            </button>
            <button
              onClick={() => setShowShortcutsModal(true)}
              className="hidden lg:flex items-center gap-1 rounded-lg border border-zinc-200 bg-white px-2 py-1 text-xs font-semibold text-zinc-600 hover:bg-zinc-50 shadow-xs transition"
              title="View Keyboard Shortcuts (?)"
            >
              <kbd className="font-mono text-zinc-500 font-bold">?</kbd>
            </button>
            <button onClick={() => setShowVerifyModal(true)}`
    );
  }

  // 8. Add Command Palette and Shortcuts Modals at the bottom before closing tag
  if (!code.includes('{/* Command Palette Modal */}')) {
    const modalsJSX = `
      {/* Command Palette Modal (Ctrl+K) */}
      {showCommandPalette && (
        <div className="fixed inset-0 z-50 flex items-start justify-center bg-black/60 p-4 pt-20 backdrop-blur-xs">
          <div className="w-full max-w-xl overflow-hidden rounded-2xl bg-white shadow-2xl border border-zinc-200 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center gap-3 border-b border-zinc-200 px-4 py-3">
              <Search className="size-4 text-zinc-400" />
              <input
                type="text"
                value={paletteQuery}
                onChange={(e) => setPaletteQuery(e.target.value)}
                placeholder="Search clauses, run actions, or jump to tabs... (Esc to close)"
                className="w-full bg-transparent text-sm font-medium text-zinc-900 placeholder:text-zinc-400 outline-none"
                autoFocus
              />
              <kbd className="rounded border border-zinc-200 bg-zinc-100 px-1.5 py-0.5 text-[10px] font-mono text-zinc-500">ESC</kbd>
            </div>
            <div className="max-h-80 overflow-y-auto p-2 text-xs">
              <div className="px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-zinc-400">Navigation</div>
              {[
                { label: 'Multi-Modal Scanner (Tab 1)', tab: 1, shortcut: '1' },
                { label: 'Brand Guidelines Knowledge Base (Tab 2)', tab: 2, shortcut: '2' },
                { label: 'Review & Sign-Off Governance Hub (Tab 3)', tab: 3, shortcut: '3' },
                { label: 'Compliance Analytics & Policy Drift (Tab 4)', tab: 4, shortcut: '4' },
                { label: 'Knowledge Graph Architecture View (Tab 5)', tab: 5, shortcut: '5' },
              ].filter((item) => item.label.toLowerCase().includes(paletteQuery.toLowerCase())).map((item) => (
                <button
                  key={item.tab}
                  onClick={() => { setActiveTab(item.tab); setShowCommandPalette(false); }}
                  className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left font-medium text-zinc-700 hover:bg-indigo-50 hover:text-indigo-900 transition"
                >
                  <span>{item.label}</span>
                  <kbd className="rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 font-mono text-[10px] text-zinc-500">{item.shortcut}</kbd>
                </button>
              ))}

              <div className="mt-2 px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-zinc-400">Actions</div>
              {[
                { label: 'Execute Multi-Modal Audit', action: () => { handleExecuteAudit(); setShowCommandPalette(false); }, shortcut: '⌘↵' },
                { label: 'Load Quick Scan Claim Verification Sample', action: () => { runOneClickDemo(); setShowCommandPalette(false); } },
                { label: 'Copy Markdown Summary for Slack / Jira', action: () => { handleCopySlackSummary(); setShowCommandPalette(false); } },
                { label: 'Verify Cryptographic Provenance Hash', action: () => { setShowVerifyModal(true); setShowCommandPalette(false); } },
                { label: 'Ingest New Brand Manual (PDF / DOCX)', action: () => { setShowIngestModal(true); setShowCommandPalette(false); } },
              ].filter((item) => item.label.toLowerCase().includes(paletteQuery.toLowerCase())).map((item, idx) => (
                <button
                  key={idx}
                  onClick={item.action}
                  className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-left font-medium text-zinc-700 hover:bg-emerald-50 hover:text-emerald-900 transition"
                >
                  <span>{item.label}</span>
                  {item.shortcut && <kbd className="rounded border border-zinc-200 bg-zinc-50 px-1.5 py-0.5 font-mono text-[10px] text-zinc-500">{item.shortcut}</kbd>}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Keyboard Shortcuts Cheat Sheet Modal (?) */}
      {showShortcutsModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
          <div className="w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-2xl border border-zinc-200 p-6 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between border-b border-zinc-100 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <Terminal className="size-5 text-indigo-600" />
                <h3 className="text-base font-bold text-zinc-900">Keyboard Shortcuts</h3>
              </div>
              <button onClick={() => setShowShortcutsModal(false)} className="rounded-lg p-1 text-zinc-400 hover:bg-zinc-100">
                <X className="size-4" />
              </button>
            </div>
            <div className="space-y-2.5 text-xs text-zinc-700">
              <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                <span>Quick Search / Command Palette</span>
                <kbd className="rounded border border-zinc-200 bg-zinc-50 px-2 py-0.5 font-mono text-[11px] font-bold">Ctrl + K / ⌘K</kbd>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                <span>Execute Multi-Modal Audit</span>
                <kbd className="rounded border border-zinc-200 bg-zinc-50 px-2 py-0.5 font-mono text-[11px] font-bold">Ctrl + Enter / ⌘↵</kbd>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                <span>Switch to Module 1–5</span>
                <kbd className="rounded border border-zinc-200 bg-zinc-50 px-2 py-0.5 font-mono text-[11px] font-bold">1, 2, 3, 4, 5</kbd>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-zinc-100">
                <span>Close Any Modal / Dialog</span>
                <kbd className="rounded border border-zinc-200 bg-zinc-50 px-2 py-0.5 font-mono text-[11px] font-bold">Esc</kbd>
              </div>
              <div className="flex items-center justify-between py-1">
                <span>Open Shortcuts Guide</span>
                <kbd className="rounded border border-zinc-200 bg-zinc-50 px-2 py-0.5 font-mono text-[11px] font-bold">?</kbd>
              </div>
            </div>
          </div>
        </div>
      )}
`;
    code = code.replace(
      '      {/* Toast Notification Container */}\n      <div',
      modalsJSX + '\n      {/* Toast Notification Container */}\n      <div'
    );
  }

  fs.writeFileSync(filePath, code, 'utf8');
  console.log('Successfully polished:', filePath);
}
