import re

path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Add Link import
if "import Link from 'next/link'" not in c:
    c = c.replace("import React, { useState, useEffect, useCallback, useMemo } from 'react'", "import React, { useState, useEffect, useCallback, useMemo } from 'react'\nimport Link from 'next/link'")

# 2. Refine useEffect for initialTab and popstate
old_use_effect = """  useEffect(() => {
    setMounted(true)
    if (typeof window !== 'undefined') {
      const path = window.location.pathname.toLowerCase()
      if (path.includes('/guidelines')) {
        setActiveTab(2)
        document.title = 'Brand Guidelines Knowledge Base | OmniGuard AI'
      } else if (path.includes('/governance') || path.includes('/review')) {
        navigateTab(3)
        document.title = 'Review & Sign-Off Hub | OmniGuard AI'
      } else if (path.includes('/analytics')) {
        setActiveTab(4)
        document.title = 'Compliance Analytics & Policy Drift | OmniGuard AI'
      } else if (path.includes('/graph')) {
        navigateTab(5)
        document.title = 'Deterministic Knowledge Graph | OmniGuard AI'
      } else if (path.includes('/scanner')) {
        navigateTab(1)
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

new_use_effect = """  useEffect(() => {
    setMounted(true)
    if (typeof window !== 'undefined') {
      const p = window.location.pathname.toLowerCase()
      let initialTabNum = initialTab || 1
      if (p.includes('/guidelines')) initialTabNum = 2
      else if (p.includes('/governance') || p.includes('/review')) initialTabNum = 3
      else if (p.includes('/analytics')) initialTabNum = 4
      else if (p.includes('/graph')) initialTabNum = 5
      else if (p.includes('/scanner')) initialTabNum = 1
      else {
        const params = new URLSearchParams(window.location.search)
        const t = params.get('tab')
        if (t) {
          const num = parseInt(t, 10)
          if (num >= 1 && num <= 5) initialTabNum = num
        }
      }
      setActiveTab(initialTabNum)

      const titles: Record<number, string> = {
        1: 'Multi-Modal Scanner | OmniGuard AI',
        2: 'Brand Guidelines Knowledge Base | OmniGuard AI',
        3: 'Review & Sign-Off Hub | OmniGuard AI',
        4: 'Compliance Analytics & Policy Drift | OmniGuard AI',
        5: 'Deterministic Knowledge Graph | OmniGuard AI',
      }
      document.title = titles[initialTabNum] || 'OmniGuard AI | Enterprise Brand Governance'

      const handlePopState = () => {
        const curPath = window.location.pathname.toLowerCase()
        let target = 1
        if (curPath.includes('/guidelines')) target = 2
        else if (curPath.includes('/governance') || curPath.includes('/review')) target = 3
        else if (curPath.includes('/analytics')) target = 4
        else if (curPath.includes('/graph')) target = 5
        setActiveTab(target)
      }
      window.addEventListener('popstate', handlePopState)
      return () => window.removeEventListener('popstate', handlePopState)
    }
  }, [initialTab])"""

if old_use_effect in c:
    c = c.replace(old_use_effect, new_use_effect)
    print("Replaced useEffect cleanly")
else:
    print("Warning: old_use_effect not found by exact string, checking...")

# 3. Enhance nav tabs with Link, path, and bubble-tab
old_nav_block = """          {[
            {
              id: 1,
              stage: 'Real-Time Inspector',
              label: 'Multi-Modal Scanner',
              detail: 'Tone, Claims & Smart Patches',
              icon: Search,
            },
            {
              id: 2,
              stage: 'Knowledge Base',
              label: 'Brand Guidelines',
              detail: 'Qdrant Vectors & Policy Rules',
              icon: Database,
            },
            {
              id: 3,
              stage: 'Governance Hub',
              label: 'Review & Sign-Off',
              detail: 'Multi-Role RBAC Workflow',
              icon: UserCheck,
            },
            {
              id: 4,
              stage: 'Enterprise Insights',
              label: 'Compliance Analytics',
              detail: 'Drift & Ambiguity Detection',
              icon: BarChart3,
            },
            {
              id: 5,
              stage: 'Architecture View',
              label: 'Knowledge Graph',
              detail: 'Deterministic Clause Explorer',
              icon: Network,
            },
          ].map((tab) => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            return (
              <button
                key={tab.id}
                onClick={() => navigateTab(tab.id)}
                className="relative group flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-left transition select-none outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 overflow-hidden"
              >"""

new_nav_block = """          {[
            {
              id: 1,
              stage: 'Real-Time Inspector',
              label: 'Multi-Modal Scanner',
              detail: 'Tone, Claims & Smart Patches',
              icon: Search,
              path: '/scanner',
            },
            {
              id: 2,
              stage: 'Knowledge Base',
              label: 'Brand Guidelines',
              detail: 'Qdrant Vectors & Policy Rules',
              icon: Database,
              path: '/guidelines',
            },
            {
              id: 3,
              stage: 'Governance Hub',
              label: 'Review & Sign-Off',
              detail: 'Multi-Role RBAC Workflow',
              icon: UserCheck,
              path: '/governance',
            },
            {
              id: 4,
              stage: 'Enterprise Insights',
              label: 'Compliance Analytics',
              detail: 'Drift & Ambiguity Detection',
              icon: BarChart3,
              path: '/analytics',
            },
            {
              id: 5,
              stage: 'Architecture View',
              label: 'Knowledge Graph',
              detail: 'Deterministic Clause Explorer',
              icon: Network,
              path: '/graph',
            },
          ].map((tab) => {
            const Icon = tab.icon
            const isActive = activeTab === tab.id
            return (
              <Link
                key={tab.id}
                href={tab.path}
                onClick={(e) => {
                  e.preventDefault()
                  navigateTab(tab.id)
                }}
                className="bubble-tab relative group flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-left transition select-none outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 overflow-hidden cursor-pointer"
              >"""

if old_nav_block in c:
    c = c.replace(old_nav_block, new_nav_block)
    print("Replaced nav block with Link and bubble-tab")
    # Also replace closing button tag with Link
    c = c.replace("                  <span className=\"mt-0.5 block truncate text-[10px] text-zinc-500\">{tab.detail}</span>\n                </span>\n              </button>", "                  <span className=\"mt-0.5 block truncate text-[10px] text-zinc-500\">{tab.detail}</span>\n                </span>\n              </Link>")
else:
    print("Warning: old_nav_block not found by exact string")

# 4. Add bubble-btn to header action buttons
c = c.replace('className="flex items-center gap-1.5 rounded-lg border border-purple-300 bg-purple-50 px-2.5 py-1 text-xs font-bold text-purple-900 hover:bg-purple-100 transition shadow-xs"', 'className="bubble-btn flex items-center gap-1.5 rounded-lg border border-purple-300 bg-purple-50 px-2.5 py-1 text-xs font-bold text-purple-900 hover:bg-purple-100 transition shadow-xs cursor-pointer"')
c = c.replace('className="flex items-center gap-1.5 rounded-lg border border-indigo-300 bg-indigo-50 px-2.5 py-1 text-xs font-bold text-indigo-900 hover:bg-indigo-100 transition shadow-xs"', 'className="bubble-btn flex items-center gap-1.5 rounded-lg border border-indigo-300 bg-indigo-50 px-2.5 py-1 text-xs font-bold text-indigo-900 hover:bg-indigo-100 transition shadow-xs cursor-pointer"')

# 5. Add bubble-btn to primary scan buttons
c = c.replace('className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-indigo-700 disabled:opacity-60 transition"', 'className="bubble-btn flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-sm hover:bg-indigo-700 disabled:opacity-60 transition cursor-pointer"')
c = c.replace('className="flex items-center gap-2 rounded-lg border border-emerald-300 bg-emerald-50 px-3 py-2 text-xs font-bold text-emerald-800 hover:bg-emerald-100 transition shadow-xs"', 'className="bubble-btn flex items-center gap-2 rounded-lg border border-emerald-300 bg-emerald-50 px-3 py-2 text-xs font-bold text-emerald-800 hover:bg-emerald-100 transition shadow-xs cursor-pointer"')
c = c.replace('className="flex items-center gap-1.5 rounded-lg border border-purple-300 bg-purple-50 px-3 py-2 text-xs font-bold text-purple-900 hover:bg-purple-100 transition shadow-xs"', 'className="bubble-btn flex items-center gap-1.5 rounded-lg border border-purple-300 bg-purple-50 px-3 py-2 text-xs font-bold text-purple-900 hover:bg-purple-100 transition shadow-xs cursor-pointer"')
c = c.replace('className="flex items-center gap-2 rounded-lg border border-indigo-200 bg-indigo-50/50 px-3 py-2 text-xs font-semibold text-indigo-950 hover:bg-indigo-100/60 transition shadow-xs"', 'className="bubble-btn flex items-center gap-2 rounded-lg border border-indigo-200 bg-indigo-50/50 px-3 py-2 text-xs font-semibold text-indigo-950 hover:bg-indigo-100/60 transition shadow-xs cursor-pointer"')
c = c.replace('className="flex items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 py-2 text-xs font-semibold text-zinc-700 hover:bg-zinc-50 transition shadow-xs"', 'className="bubble-btn-secondary flex items-center gap-2 rounded-lg border border-zinc-200 bg-white px-3 py-2 text-xs font-semibold text-zinc-700 hover:bg-zinc-50 transition shadow-xs cursor-pointer"')

# 6. Add bubble-btn to sign-off buttons
c = c.replace('className={`flex items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-bold transition shadow-xs ${', 'className={`bubble-btn flex items-center gap-1.5 rounded-lg px-3 py-2 text-xs font-bold transition shadow-xs cursor-pointer ${')

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Page enhancements applied successfully to share/v0-project/app/page.tsx")
