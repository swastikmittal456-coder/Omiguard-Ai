import os
import re

target_files = [
    "share/v0-project/app/page.tsx",
    "frontend/app/page.tsx",
]

for fpath in target_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        code = f.read().replace("\r\n", "\n")

    # 1. Add framer-motion import
    if "import { motion, AnimatePresence } from 'framer-motion'" not in code:
        code = code.replace(
            "import React, { useState, useEffect, useCallback, useMemo } from 'react'",
            "import React, { useState, useEffect, useCallback, useMemo } from 'react'\nimport { motion, AnimatePresence } from 'framer-motion'"
        )

    # 2. Add direction state and update navigateTab
    old_state = """export default function OmniGuardEnterpriseApp({ initialTab = 1 }: { initialTab?: number } = {}) {
  // Navigation: 1=Live Scanner, 2=Knowledge Base, 3=Review Hub, 4=Compliance Analytics, 5=Knowledge Graph
  const [activeTab, setActiveTab] = useState<number>(initialTab)
  const [mounted, setMounted] = useState(false)

  const navigateTab = useCallback((tabId: number) => {
    setActiveTab(tabId)"""

    new_state = """export default function OmniGuardEnterpriseApp({ initialTab = 1 }: { initialTab?: number } = {}) {
  // Navigation: 1=Live Scanner, 2=Knowledge Base, 3=Review Hub, 4=Compliance Analytics, 5=Knowledge Graph
  const [activeTab, setActiveTab] = useState<number>(initialTab)
  const [direction, setDirection] = useState<number>(0)
  const [mounted, setMounted] = useState(false)

  const navigateTab = useCallback((tabId: number) => {
    setDirection(tabId > activeTab ? 1 : -1)
    setActiveTab(tabId)"""

    if old_state in code:
        code = code.replace(old_state, new_state, 1)
        print(f"Updated direction state in {fpath}")

    # Update popstate handler
    old_pop = """      const handlePopState = () => {
        const p = window.location.pathname.toLowerCase()
        if (p.includes('/guidelines')) setActiveTab(2)
        else if (p.includes('/governance') || p.includes('/review')) setActiveTab(3)
        else if (p.includes('/analytics')) setActiveTab(4)
        else if (p.includes('/graph')) setActiveTab(5)
        else setActiveTab(1)
      }"""

    new_pop = """      const handlePopState = () => {
        const p = window.location.pathname.toLowerCase()
        let newTab = 1
        if (p.includes('/guidelines')) newTab = 2
        else if (p.includes('/governance') || p.includes('/review')) newTab = 3
        else if (p.includes('/analytics')) newTab = 4
        else if (p.includes('/graph')) newTab = 5
        setDirection(newTab > activeTab ? 1 : -1)
        setActiveTab(newTab)
      }"""

    if old_pop in code:
        code = code.replace(old_pop, new_pop, 1)

    # 3. Update the Tab Buttons in <nav> with layoutId swish pill
    old_nav_button = """            return (
              <button
                key={tab.id}
                onClick={() => navigateTab(tab.id)}
                className={`group flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-left transition ${
                  isActive
                    ? 'border border-indigo-200 bg-indigo-50/80 shadow-xs'
                    : 'hover:border-zinc-200 hover:bg-zinc-50'
                }`}
              >
                <span
                  className={`flex size-8 shrink-0 items-center justify-center rounded-lg border ${
                    isActive
                      ? 'border-indigo-300 bg-indigo-600 text-white'
                      : 'border-zinc-200 bg-zinc-100 text-zinc-600'
                  }`}
                >
                  <Icon className="size-4" />
                </span>
                <span className="min-w-0">
                  <span className="block text-[9px] font-bold uppercase tracking-wider text-indigo-600">
                    {tab.stage}
                  </span>
                  <span
                    className={`block truncate text-xs font-bold ${
                      isActive ? 'text-indigo-950' : 'text-zinc-800'
                    }`}
                  >
                    {tab.label}
                  </span>
                  <span className="mt-0.5 block truncate text-[10px] text-zinc-500">{tab.detail}</span>
                </span>
              </button>
            )"""

    new_nav_button = """            return (
              <button
                key={tab.id}
                onClick={() => navigateTab(tab.id)}
                className="relative group flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-left transition select-none outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 overflow-hidden"
              >
                {isActive && (
                  <motion.div
                    layoutId="activeTabSwishIndicator"
                    className="absolute inset-0 rounded-lg bg-indigo-50/90 border border-indigo-200 shadow-xs z-0"
                    transition={{ type: "spring", stiffness: 480, damping: 36 }}
                  />
                )}
                <span
                  className={`relative z-10 flex size-8 shrink-0 items-center justify-center rounded-lg border transition-all duration-200 ${
                    isActive
                      ? 'border-indigo-400 bg-indigo-600 text-white shadow-xs scale-105'
                      : 'border-zinc-200 bg-zinc-100 text-zinc-600 group-hover:bg-zinc-200/80 group-hover:scale-105'
                  }`}
                >
                  <Icon className="size-4 transition-transform duration-200 group-hover:scale-110" />
                </span>
                <span className="relative z-10 min-w-0">
                  <span className="block text-[9px] font-bold uppercase tracking-wider text-indigo-600">
                    {tab.stage}
                  </span>
                  <span
                    className={`block truncate text-xs font-bold transition-colors ${
                      isActive ? 'text-indigo-950 font-extrabold' : 'text-zinc-800'
                    }`}
                  >
                    {tab.label}
                  </span>
                  <span className="mt-0.5 block truncate text-[10px] text-zinc-500">{tab.detail}</span>
                </span>
              </button>
            )"""

    if old_nav_button in code:
        code = code.replace(old_nav_button, new_nav_button, 1)
        print(f"Updated nav buttons with swish indicator in {fpath}")
    else:
        print(f"WARNING: nav button pattern not found in {fpath}")

    # 4. Wrap Tab Content with AnimatePresence & directional swish motion
    # Find the boundary right after </nav>
    nav_end = "</nav>\n\n        {/* ──"
    tab1_marker = "{activeTab === 1 && ("
    tab5_end = "          </section>\n        )}\n\n        \n      </div>"

    if tab1_marker in code and tab5_end in code:
        # Insert opening AnimatePresence before Tab 1
        swish_container_start = """        {/* Swish Page Transition Container */}
        <div className="relative overflow-hidden min-h-[620px] w-full">
          <AnimatePresence mode="wait" custom={direction} initial={false}>
            <motion.div
              key={activeTab}
              custom={direction}
              variants={{
                enter: (dir: number) => ({
                  x: dir > 0 ? 42 : dir < 0 ? -42 : 0,
                  opacity: 0,
                  scale: 0.985,
                  filter: "blur(5px)",
                }),
                center: {
                  x: 0,
                  opacity: 1,
                  scale: 1,
                  filter: "blur(0px)",
                  transition: {
                    duration: 0.32,
                    ease: [0.16, 1, 0.3, 1], // Apple/Stripe-level responsive spring swish curve
                  },
                },
                exit: (dir: number) => ({
                  x: dir > 0 ? -42 : dir < 0 ? 42 : 0,
                  opacity: 0,
                  scale: 0.985,
                  filter: "blur(5px)",
                  transition: {
                    duration: 0.22,
                    ease: [0.4, 0, 1, 1],
                  },
                }),
              }}
              initial="enter"
              animate="center"
              exit="exit"
              className="w-full"
            >
        """

        code = code.replace("        {activeTab === 1 && (", swish_container_start + "      {activeTab === 1 && (", 1)

        swish_container_end = """          </section>
        )}
            </motion.div>
          </AnimatePresence>
        </div>

      </div>"""

        code = code.replace(tab5_end, swish_container_end, 1)
        print(f"Injected AnimatePresence and directional swish variants in {fpath}")
    else:
        print(f"WARNING: tab boundary not matched in {fpath}")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Saved {fpath}")
