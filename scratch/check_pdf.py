from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
pdf_path = ROOT / "OmniGuard_AI_Round_3_Submission.pdf"
with open(pdf_path, "rb") as f:
    data = f.read()

pages = len(re.findall(rb"/Type\s*/Page\b", data))
print(f"Total pages in PDF: {pages}")

html_path = ROOT / "scratch" / "round3_proposal.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read().lower()

forbidden_terms = ["codenexus", "hackathon", "72-hour", "round 3", "rubric", "points", "100 points"]
for term in forbidden_terms:
    count = html.count(term)
    print(f"Term '{term}': {count} occurrences in HTML")

