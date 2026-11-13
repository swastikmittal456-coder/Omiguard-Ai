import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

page_path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add KeyRound to imports
if "KeyRound," not in c:
    c = c.replace("Lock,", "Lock,\n  KeyRound,")
    print("Added KeyRound to imports!")

# 2. Add state hooks for Demo Login Modal
login_states = """  // Demo Account Modal State
  const [showLoginModal, setShowLoginModal] = useState(false)
  const [loginEmailInput, setLoginEmailInput] = useState('brand.director@enterprise.omniguard.ai')
  const [loginPasswordInput, setLoginPasswordInput] = useState('OmniGuard#2026!Brand')
  const [loginError, setLoginError] = useState<string | null>(null)
"""

if "const [showLoginModal, setShowLoginModal]" not in c:
    target_demo_state = "const [copiedAccountEmail, setCopiedAccountEmail] = useState<string | null>(null)"
    c = c.replace(target_demo_state, target_demo_state + "\n" + login_states)
    print("Added showLoginModal state hooks!")

# 3. Add manual login handler method
login_methods = """  // ─── Manual Demo Login Handler ───────────────────────────────────────────
  const handleManualLogin = (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    setLoginError(null)
    const matched = DEMO_ACCOUNTS.find(
      (a) => a.email.toLowerCase() === loginEmailInput.trim().toLowerCase()
    )
    if (!matched) {
      setLoginError('Unknown demo account. Please choose one of the 4 evaluator accounts below.')
      return
    }
    if (loginPasswordInput !== matched.password) {
      setLoginError('Password does not match. Expected: ' + matched.password)
      return
    }
    setActiveDemoEmail(matched.email)
    setSelectedRole(matched.roleKey)
    setShowLoginModal(false)
    addToast(
      'success',
      `Authenticated as ${matched.name}`,
      `Signed in as ${matched.email} with mandate: ${matched.badge}.`
    )
  }
"""

if "const handleManualLogin =" not in c:
    target_switch = "const switchDemoPersona = (account: (typeof DEMO_ACCOUNTS)[0]) => {"
    c = c.replace(target_switch, login_methods + "\n" + target_switch)
    print("Added handleManualLogin method!")

# 4. Add User Persona Badge Button in the Header (next to Quick Search)
header_persona_button = """            {/* Demo Account Active User Pill */}
            {(() => {
              const activeAcc = DEMO_ACCOUNTS.find((a) => a.email === activeDemoEmail) || DEMO_ACCOUNTS[0]
              return (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className="flex items-center gap-1.5 rounded-lg border border-indigo-200 bg-white px-2.5 py-1 text-xs font-bold text-indigo-950 hover:border-indigo-400 hover:bg-indigo-50/50 shadow-xs transition cursor-pointer"
                  title="Click to view all demo account credentials or switch persona"
                >
                  <span className="size-2 rounded-full bg-emerald-500 animate-pulse" />
                  <span>{activeAcc.icon}</span>
                  <span className="hidden sm:inline font-bold">{activeAcc.name}</span>
                  <span className="rounded bg-indigo-100 px-1 py-0.2 text-[9px] font-mono text-indigo-700 font-bold">
                    {activeAcc.badge}
                  </span>
                  <KeyRound className="size-3 text-indigo-500" />
                </button>
              )
            })()}
"""

target_header_search = '<button\n              onClick={() => setShowCommandPalette(true)}'
if target_header_search in c and "Demo Account Active User Pill" not in c:
    c = c.replace(target_header_search, header_persona_button + "\n            " + target_header_search)
    print("Added active user persona button to header!")

# 5. Add "View Credentials Guide" button in the Demo Banner
banner_guide_button = """            <button
              onClick={() => setShowLoginModal(true)}
              className="flex items-center gap-1 rounded-md bg-indigo-600 px-2 py-0.5 text-[11px] font-bold text-white hover:bg-indigo-700 transition cursor-pointer shadow-xs ml-1"
              title="Open Demo Accounts & Credentials Dialog"
            >
              <KeyRound className="size-3" />
              <span>Login &amp; Credentials Guide</span>
            </button>
"""

target_banner_text = '<span className="font-bold text-indigo-950">Evaluator Demo Accounts (1-Click Switch &amp; Login):</span>'
if target_banner_text in c and "Login &amp; Credentials Guide" not in c:
    target_banner_div = '<div className="flex flex-wrap items-center gap-2">\n            {DEMO_ACCOUNTS.map((acc) => {'
    c = c.replace(target_banner_div, '<div className="flex flex-wrap items-center gap-2">\n' + banner_guide_button + '            {DEMO_ACCOUNTS.map((acc) => {')
    print("Added Credentials Guide button to Demo banner!")

# 6. Add Demo Account Login Modal JSX
demo_login_modal = """      {/* ─────────────────────────────────────────────────────────────────────────────
          CODE NEXUS R3: DEMO ACCOUNT CREDENTIALS & LOGIN MODAL
      ───────────────────────────────────────────────────────────────────────────── */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4 backdrop-blur-xs">
          <div className="relative w-full max-w-3xl rounded-2xl border border-zinc-200 bg-white p-6 shadow-2xl animate-in fade-in zoom-in-95 duration-150 max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-start justify-between border-b border-zinc-100 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="flex size-6 items-center justify-center rounded-md bg-indigo-600 text-white font-bold text-xs shadow-xs">
                    R3
                  </span>
                  <Badge tone="purple">CodeNexus Evaluator Suite</Badge>
                  <Badge tone="emerald">1-Click Fast Login</Badge>
                </div>
                <h3 className="mt-1.5 text-lg font-bold text-zinc-950">
                  Evaluator Demo Accounts &amp; RBAC Authentication
                </h3>
                <p className="mt-0.5 text-xs text-zinc-500">
                  Select any pre-configured enterprise persona below to authenticate instantly, or test manual login credentials.
                </p>
              </div>
              <button
                onClick={() => setShowLoginModal(false)}
                className="rounded-lg p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 cursor-pointer"
              >
                <X className="size-5" />
              </button>
            </div>

            {/* 4 Demo Account Cards */}
            <div className="mt-5 space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-zinc-400 block mb-1">
                4 Pre-Configured Evaluator Personas (1-Click Switch):
              </span>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                {DEMO_ACCOUNTS.map((acc) => {
                  const isActive = activeDemoEmail === acc.email
                  return (
                    <div
                      key={acc.email}
                      className={`rounded-xl border p-3.5 transition flex flex-col justify-between ${
                        isActive
                          ? 'border-indigo-600 bg-indigo-50/50 shadow-xs ring-2 ring-indigo-500/20'
                          : 'border-zinc-200 bg-zinc-50/60 hover:border-zinc-300 hover:bg-white'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-1.5">
                          <div className="flex items-center gap-1.5">
                            <span className="text-base">{acc.icon}</span>
                            <span className="text-xs font-bold text-zinc-900">{acc.name}</span>
                          </div>
                          <span className="rounded bg-zinc-100 px-1.5 py-0.5 text-[9px] font-mono font-bold text-zinc-700">
                            {acc.badge}
                          </span>
                        </div>

                        <p className="text-[11px] text-zinc-600 mb-2 leading-relaxed">
                          {acc.description}
                        </p>

                        <div className="rounded-lg bg-white p-2 border border-zinc-200/80 text-[10px] font-mono space-y-0.5 mb-3">
                          <div className="flex justify-between items-center text-zinc-600">
                            <span>Email:</span>
                            <span className="font-bold text-zinc-900">{acc.email}</span>
                          </div>
                          <div className="flex justify-between items-center text-zinc-600">
                            <span>Password:</span>
                            <span className="font-bold text-indigo-600">{acc.password}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => {
                            setLoginEmailInput(acc.email)
                            setLoginPasswordInput(acc.password)
                            switchDemoPersona(acc)
                            setShowLoginModal(false)
                          }}
                          className={`flex-1 flex items-center justify-center gap-1.5 rounded-lg py-1.5 text-xs font-bold transition cursor-pointer shadow-xs ${
                            isActive
                              ? 'bg-emerald-600 text-white hover:bg-emerald-700'
                              : 'bg-indigo-600 text-white hover:bg-indigo-700'
                          }`}
                        >
                          <CheckCircle2 className="size-3.5" />
                          <span>{isActive ? 'Active Session' : `Login as ${acc.name.split(' ')[0]}`}</span>
                        </button>
                        <button
                          onClick={() => copyPersonaCredentials(acc)}
                          className="rounded-lg border border-zinc-200 bg-white p-1.5 text-zinc-500 hover:text-indigo-600 hover:border-indigo-300 transition cursor-pointer"
                          title="Copy email & password"
                        >
                          <Copy className="size-3.5" />
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Manual Credential Verification Form */}
            <div className="mt-5 rounded-xl border border-zinc-200 bg-zinc-50/70 p-4">
              <span className="text-[11px] font-bold text-zinc-800 block mb-2">
                Manual Credential Verification Form:
              </span>
              <form onSubmit={handleManualLogin} className="space-y-3">
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-zinc-500 mb-1">
                      Account Email
                    </label>
                    <input
                      type="email"
                      value={loginEmailInput}
                      onChange={(e) => setLoginEmailInput(e.target.value)}
                      placeholder="e.g. brand.director@enterprise.omniguard.ai"
                      className="w-full rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-mono text-zinc-900 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-zinc-500 mb-1">
                      Password
                    </label>
                    <input
                      type="text"
                      value={loginPasswordInput}
                      onChange={(e) => setLoginPasswordInput(e.target.value)}
                      placeholder="e.g. OmniGuard#2026!Brand"
                      className="w-full rounded-lg border border-zinc-200 bg-white px-3 py-1.5 text-xs font-mono text-zinc-900 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>
                </div>

                {loginError && (
                  <div className="rounded-lg bg-rose-50 border border-rose-200 p-2 text-xs text-rose-700 flex items-center gap-1.5">
                    <AlertTriangle className="size-3.5 shrink-0 text-rose-600" />
                    <span>{loginError}</span>
                  </div>
                )}

                <div className="flex items-center justify-between pt-1">
                  <span className="text-[10px] text-zinc-500">
                    Credentials are pre-validated against SQLite RBAC role registry.
                  </span>
                  <button
                    type="submit"
                    className="flex items-center gap-1.5 rounded-lg bg-indigo-600 px-4 py-1.5 text-xs font-bold text-white hover:bg-indigo-700 transition shadow-xs cursor-pointer"
                  >
                    <Lock className="size-3.5" />
                    <span>Sign In &amp; Set RBAC Role</span>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
"""

target_modal_place = "{/* ─────────────────────────────────────────────────────────────────────────────\n          IMPROVEMENT 3: CROSS-POLICY CONTRADICTION INTERACTIVE DIFF MERGER MODAL"
if target_modal_place in c and "CODE NEXUS R3: DEMO ACCOUNT CREDENTIALS & LOGIN MODAL" not in c:
    c = c.replace(target_modal_place, demo_login_modal + "\n" + target_modal_place)
    print("Added Demo Login Modal JSX!")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Demo login modal additions finished!")
"""
"""
