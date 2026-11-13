for p in [r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx", r"C:\Users\swast\OneDrive\Desktop\vercel\frontend\app\page.tsx"]:
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. Update navigateTab to use functional setState and empty dependency array
    old_nav = """  const navigateTab = useCallback((tabId: number) => {
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
  }, [activeTab])"""

    new_nav = """  const navigateTab = useCallback((tabId: number) => {
    setActiveTab((prev) => {
      setDirection(tabId > prev ? 1 : -1)
      return tabId
    })
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
  }, [])"""

    c = c.replace(old_nav, new_nav)

    # 2. Update popstate handler in useEffect
    old_pop = """      const handlePopState = () => {
        const curPath = window.location.pathname.toLowerCase()
        let target = 1
        if (curPath.includes('/guidelines')) target = 2
        else if (curPath.includes('/governance') || curPath.includes('/review')) target = 3
        else if (curPath.includes('/analytics')) target = 4
        else if (curPath.includes('/graph')) target = 5
        setActiveTab(target)
      }"""

    new_pop = """      const handlePopState = () => {
        const curPath = window.location.pathname.toLowerCase()
        let target = 1
        if (curPath.includes('/guidelines')) target = 2
        else if (curPath.includes('/governance') || curPath.includes('/review')) target = 3
        else if (curPath.includes('/analytics')) target = 4
        else if (curPath.includes('/graph')) target = 5
        setActiveTab((prev) => {
          setDirection(target > prev ? 1 : -1)
          return target
        })
      }"""

    c = c.replace(old_pop, new_pop)

    with open(p, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Updated {p}")
