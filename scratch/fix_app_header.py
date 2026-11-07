import os

target_files = [
    r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx",
    r"C:\Users\swast\OneDrive\Desktop\vercel\frontend\app\page.tsx",
]

for fpath in target_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read().replace("\r\n", "\n")

    if "import { motion, AnimatePresence } from 'framer-motion'" not in code:
        code = code.replace(
            "import React, { useState, useEffect, useCallback, useMemo } from 'react'",
            "import React, { useState, useEffect, useCallback, useMemo } from 'react'\nimport { motion, AnimatePresence } from 'framer-motion'"
        )

    old_fn = "export default function OmniGuardEnterpriseApp() {\n  // Navigation: 1=Live Scanner, 2=Knowledge Base, 3=Review Hub, 4=Drift Analytics, 5=Graph Inspector, 6=Hackathon Dossier\n  const [activeTab, setActiveTab] = useState<number>(1)"
    new_fn = """export default function OmniGuardEnterpriseApp({ initialTab = 1 }: { initialTab?: number } = {}) {
  // Navigation: 1=Live Scanner, 2=Knowledge Base, 3=Review Hub, 4=Compliance Analytics, 5=Knowledge Graph
  const [activeTab, setActiveTab] = useState<number>(initialTab)
  const [direction, setDirection] = useState<number>(0)
  const [mounted, setMounted] = useState(false)

  const navigateTab = useCallback((tabId: number) => {
    setDirection(tabId > activeTab ? 1 : -1)
    setActiveTab(tabId)
    const routes: Record<number, string> = {
      1: '/scanner',
      2: '/guidelines',
      3: '/governance',
      4: '/analytics',
      5: '/graph',
    }
    const targetRoute = routes[tabId] || '/scanner'
    if (typeof window !== 'undefined') {
      if (window.location.pathname !== targetRoute) {
        window.history.pushState(null, '', targetRoute)
      }
      const titles: Record<number, string> = {
        1: 'Multi-Modal Scanner | OmniGuard AI',
        2: 'Brand Guidelines Knowledge Base | OmniGuard AI',
        3: 'Review & Sign-Off Hub | OmniGuard AI',
        4: 'Compliance Analytics & Policy Drift | OmniGuard AI',
        5: 'Deterministic Knowledge Graph | OmniGuard AI',
      }
      document.title = titles[tabId] || 'OmniGuard AI | Enterprise Brand Governance'
    }
  }, [activeTab])

  useEffect(() => {
    setMounted(true)
    if (typeof window !== 'undefined') {
      const path = window.location.pathname.toLowerCase()
      if (path.includes('/guidelines')) {
        setActiveTab(2)
        document.title = 'Brand Guidelines Knowledge Base | OmniGuard AI'
      } else if (path.includes('/governance') || path.includes('/review')) {
        setActiveTab(3)
        document.title = 'Review & Sign-Off Hub | OmniGuard AI'
      } else if (path.includes('/analytics')) {
        setActiveTab(4)
        document.title = 'Compliance Analytics & Policy Drift | OmniGuard AI'
      } else if (path.includes('/graph')) {
        setActiveTab(5)
        document.title = 'Deterministic Knowledge Graph | OmniGuard AI'
      } else if (path.includes('/scanner')) {
        setActiveTab(1)
        document.title = 'Multi-Modal Scanner | OmniGuard AI'
      } else {
        const params = new URLSearchParams(window.location.search)
        const t = params.get('tab')
        if (t) {
          const num = parseInt(t, 10)
          if (num >= 1 && num <= 5) setActiveTab(num)
        } else if (initialTab) {
          setActiveTab(initialTab)
        }
      }

      const handlePopState = () => {
        const p = window.location.pathname.toLowerCase()
        let newTab = 1
        if (p.includes('/guidelines')) newTab = 2
        else if (p.includes('/governance') || p.includes('/review')) newTab = 3
        else if (p.includes('/analytics')) newTab = 4
        else if (p.includes('/graph')) newTab = 5
        setDirection(newTab > activeTab ? 1 : -1)
        setActiveTab(newTab)
      }
      window.addEventListener('popstate', handlePopState)
      return () => window.removeEventListener('popstate', handlePopState)
    }
  }, [initialTab, activeTab])"""

    if old_fn in code:
        code = code.replace(old_fn, new_fn, 1)
        print("Updated function header in", fpath)
    else:
        print("Could not match old_fn in", fpath)

    # Replace setActiveTab calls
    code = code.replace("onClick={() => setActiveTab(tab.id)}", "onClick={() => navigateTab(tab.id)}")
    code = code.replace("setActiveTab(1)", "navigateTab(1)")
    code = code.replace("setActiveTab(3)", "navigateTab(3)")
    code = code.replace("setActiveTab(5)", "navigateTab(5)")
    code = code.replace("setActiveTab(parseInt(e.key, 10))", "navigateTab(parseInt(e.key, 10))")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)

print("Finished header and navigation fixes.")
