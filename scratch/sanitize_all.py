import os

# 1. Clean backend/init_db.py
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\init_db.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("CodeNexus Hackathon Selects OmniGuard AI (Team Layer 7) for Round 2 Enterprise Brand Safety", "Enterprise Consortium Selects OmniGuard AI for Global Enterprise Brand Safety")
c = c.replace("Team Layer 7", "Enterprise Compliance Office")
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\init_db.py", "w", encoding="utf-8") as f:
    f.write(c)

# 2. Clean backend/main.py
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("Enterprise Compliance Office role disclosures (Swastik, Office of General Counsel, Aditya, Nikita)", "Enterprise Governance Role Mandates (Brand Director, Legal Counsel, Security Architect, Content Ops)")
c = c.replace("Swastik Mittal", "Principal Brand Director")
c = c.replace("Swastik", "Brand Director")
c = c.replace("Nikita Singh", "Content Operations Lead")
c = c.replace("Nikita", "Content Ops")
c = c.replace("Aditya Baliyan", "Platform Security Architect")
c = c.replace("Aditya", "Security Architect")
c = c.replace("Aprajita", "Office of General Counsel")
c = c.replace("Team Layer 7", "Enterprise Compliance Office")
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py", "w", encoding="utf-8") as f:
    f.write(c)

# 3. Clean frontend/app/page.tsx and share/v0-project/app/page.tsx
for p in [r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx", r"C:\Users\swast\OneDrive\Desktop\vercel\frontend\app\page.tsx"]:
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("content_creator: 'Nikita Singh'", "content_creator: 'Content Operations Lead'")
    c = c.replace("Legal Counsel (Aprajita)", "Office of General Counsel")
    c = c.replace("Aprajita", "Office of General Counsel")
    c = c.replace("Nikita Singh", "Content Operations Lead")
    c = c.replace("Nikita", "Content Operations Lead")
    c = c.replace("Swastik Mittal", "Principal Brand Director")
    c = c.replace("Swastik", "Principal Brand Director")
    c = c.replace("Aditya Baliyan", "Chief Information Security Officer")
    c = c.replace("Aditya", "Chief Information Security Officer")
    c = c.replace("Team Layer 7", "Enterprise Edition")
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)

# 4. Clean README.md and DEPLOYMENT.md
for doc in [r"C:\Users\swast\OneDrive\Desktop\vercel\README.md", r"C:\Users\swast\OneDrive\Desktop\vercel\DEPLOYMENT.md"]:
    if not os.path.exists(doc):
        continue
    with open(doc, "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("Nikita Singh (Creator)", "Content Operations Lead (Creator)")
    c = c.replace("Nikita Singh", "Content Operations Lead")
    c = c.replace("Swastik Mittal", "Principal Brand Director")
    c = c.replace("Aprajita", "Office of General Counsel")
    c = c.replace("Aditya Baliyan", "Platform Security Architect")
    c = c.replace("Team Layer 7", "Enterprise Consortium")
    with open(doc, "w", encoding="utf-8") as f:
        f.write(c)

print("Sanitization script executed successfully!")
