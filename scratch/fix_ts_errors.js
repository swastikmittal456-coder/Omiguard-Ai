const fs = require('fs');
const path = require('path');

const targetFiles = [
  path.join(__dirname, '..', 'share', 'v0-project', 'app', 'page.tsx'),
  path.join(__dirname, '..', 'frontend', 'app', 'page.tsx'),
];

for (const filePath of targetFiles) {
  if (!fs.existsSync(filePath)) continue;
  let code = fs.readFileSync(filePath, 'utf8');

  // 1. Update Toast interface & addToast signature
  code = code.replace(
    /interface Toast \{\s*id: string\s*type: 'success' \| 'error' \| 'info'/g,
    `interface Toast {\n  id: string\n  type: 'success' | 'error' | 'info' | 'warning'`
  );

  code = code.replace(
    /const addToast = useCallback\(\(type: 'success' \| 'error' \| 'info',/g,
    `const addToast = useCallback((type: 'success' | 'error' | 'info' | 'warning',`
  );

  // 2. Update computeClientAuditFallback to return both audit and audit_log
  code = code.replace(
    /return \{\s*audit: \{\s*id: Math\.floor\(Math\.random\(\) \* 9000\) \+ 1000,\s*channel,\s*draft_text: draftText,\s*compliance_score: score,\s*tone_status: issues\.some\(\(i: any\) => i\.guideline_clause === 'Clause 4\.1'\) \? 'warning' : 'passed',\s*claim_status: issues\.some\(\(i: any\) => i\.guideline_clause === 'Clause 3\.2'\) \? 'failed' : 'passed',\s*color_status: deltaE > 3\.0 \? 'warning' : 'passed',\s*contrast_status: apca < 75\.0 \? 'failed' : 'passed',\s*created_at: new Date\(\)\.toISOString\(\),\s*\},\s*compliance_score: score,\s*micro_patches: issues\s*\};/g,
    `const auditObj = {
      id: Math.floor(Math.random() * 9000) + 1000,
      channel,
      draft_text: draftText,
      compliance_score: score,
      tone_status: issues.some((i: any) => i.guideline_clause === 'Clause 4.1') ? 'warning' : 'passed',
      claim_status: issues.some((i: any) => i.guideline_clause === 'Clause 3.2') ? 'failed' : 'passed',
      color_status: deltaE > 3.0 ? 'warning' : 'passed',
      contrast_status: apca < 75.0 ? 'failed' : 'passed',
      created_at: new Date().toISOString(),
    };
    return {
      audit: auditObj,
      audit_log: auditObj,
      compliance_score: score,
      micro_patches: issues
    };`
  );

  // 3. Fix setExtractedPalette in fallbackResult
  code = code.replace(
    /setExtractedPalette\(fallbackResult\.palette\)/g,
    `const paletteItems: ColorPaletteItem[] = fallbackResult.palette.map((hex, idx) => ({
        hex,
        rgb: [79, 70, 229],
        percentage: idx === 0 ? 55 : (idx === 1 ? 25 : 10)
      }));
      setExtractedPalette(paletteItems)`
  );

  fs.writeFileSync(filePath, code, 'utf8');
  console.log('Fixed TS items in:', filePath);
}
