import os

target_files = [
    "share/v0-project/app/page.tsx",
    "frontend/app/page.tsx",
]

old_header_pattern = """export default function OmniGuardEnterpriseApp() {
  // Navigation: 1=Live Scanner, 2=Knowledge Base, 3=Review Hub, 4=Compliance Analytics, 5=Knowledge Graph
  const [activeTab, setActiveTab] = useState<number>(1)
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search)
      const t = params.get('tab')
      if (t) {
        const num = parseInt(t, 10)
        if (num >= 1 && num <= 5) setActiveTab(num)
      }
    }
  }, [])"""

new_header = """export default function OmniGuardEnterpriseApp({ initialTab = 1 }: { initialTab?: number } = {}) {
  // Navigation: 1=Live Scanner, 2=Knowledge Base, 3=Review Hub, 4=Compliance Analytics, 5=Knowledge Graph
  const [activeTab, setActiveTab] = useState<number>(initialTab)
  const [mounted, setMounted] = useState(false)

  const navigateTab = useCallback((tabId: number) => {
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
  }, [])

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
        if (p.includes('/guidelines')) setActiveTab(2)
        else if (p.includes('/governance') || p.includes('/review')) setActiveTab(3)
        else if (p.includes('/analytics')) setActiveTab(4)
        else if (p.includes('/graph')) setActiveTab(5)
        else setActiveTab(1)
      }
      window.addEventListener('popstate', handlePopState)
      return () => window.removeEventListener('popstate', handlePopState)
    }
  }, [initialTab])"""

for fpath in target_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize CRLF for matching
    content_normalized = content.replace("\r\n", "\n")
    if old_header_pattern in content_normalized:
        content_normalized = content_normalized.replace(old_header_pattern, new_header, 1)
        print(f"Header replaced in {fpath}")
    else:
        print(f"WARNING: Header pattern not found in {fpath}")

    # Replace setActiveTab with navigateTab
    content_normalized = content_normalized.replace("onClick={() => setActiveTab(tab.id)}", "onClick={() => navigateTab(tab.id)}")
    content_normalized = content_normalized.replace("setActiveTab(1)", "navigateTab(1)")
    content_normalized = content_normalized.replace("setActiveTab(3)", "navigateTab(3)")
    content_normalized = content_normalized.replace("setActiveTab(5)", "navigateTab(5)")
    content_normalized = content_normalized.replace("setActiveTab(parseInt(e.key, 10))", "navigateTab(parseInt(e.key, 10))")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content_normalized)
    print(f"Updated {fpath} successfully.")
