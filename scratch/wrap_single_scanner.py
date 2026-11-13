page_path = r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx"

with open(page_path, "r", encoding="utf-8") as f:
    content = f.read()

target_banner = "{/* Celebratory Banner when patches applied */}"
if target_banner in content and "{scannerMode === 'single' && (" not in content:
    content = content.replace(target_banner, "{scannerMode === 'single' && (\n              <>\n            " + target_banner)
    print("Wrapped start of Single Asset Inspector!")

target_end = """                  )}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* ─────────────────────────────────────────────────────────────────────────────
            TAB 2: STAGE 1: INGEST (KNOWLEDGE BASE MANAGER)"""

replacement_end = """                  )}
                </div>
              </div>
            </div>
            </>
            )}
          </section>
        )}

        {/* ─────────────────────────────────────────────────────────────────────────────
            TAB 2: STAGE 1: INGEST (KNOWLEDGE BASE MANAGER)"""

if target_end in content:
    content = content.replace(target_end, replacement_end)
    print("Wrapped end of Single Asset Inspector!")

with open(page_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Single scanner wrap done!")
