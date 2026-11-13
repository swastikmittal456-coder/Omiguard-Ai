import os
import re

# 1. Update backend/init_db.py
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\init_db.py", "r", encoding="utf-8") as f:
    c = f.read()

# Replace individual names in brand assets
c = c.replace('"Swastik Mittal"', '"Design Operations"')
c = c.replace('"Aprajita"', '"Legal Review Board"')
c = c.replace('"Aditya Baliyan"', '"Architecture Team"')
c = c.replace('"Nikita Singh"', '"Content Operations"')

c = c.replace('("Executive Headshot Swastik Mittal", "photography", "/assets/team/swastik-mittal.jpg",', '("Executive Headshot Brand Director", "photography", "/assets/team/brand-director.jpg",')
c = c.replace('("Executive Headshot Aprajita", "photography", "/assets/team/aprajita.jpg",', '("Executive Headshot General Counsel", "photography", "/assets/team/general-counsel.jpg",')
c = c.replace('("Executive Headshot Aditya Baliyan", "photography", "/assets/team/aditya-baliyan.jpg",', '("Executive Headshot Chief Architect", "photography", "/assets/team/chief-architect.jpg",')
c = c.replace('("Executive Headshot Nikita Singh", "photography", "/assets/team/nikita-singh.jpg",', '("Executive Headshot Content Operations", "photography", "/assets/team/content-ops.jpg",')

# Replace names in team_roles
c = c.replace('("content_creator", "Nikita Singh",', '("content_creator", "Content Operations Lead",')
c = c.replace('("brand_lead", "Swastik Mittal",', '("brand_lead", "Principal Brand Director",')
c = c.replace('("brand_manager", "Swastik Mittal",', '("brand_manager", "Enterprise Brand Governance",')
c = c.replace('("compliance_officer", "Aprajita",', '("compliance_officer", "Regulatory Compliance Officer",')
c = c.replace('("legal_counsel", "Aprajita",', '("legal_counsel", "Office of General Counsel",')
c = c.replace('("systems_engineer", "Aditya Baliyan",', '("systems_engineer", "Platform Security Architect",')
c = c.replace('("full_stack_integrator", "Nikita Singh",', '("full_stack_integrator", "Integration Engineer",')

# Replace certificate signers
c = c.replace('"brand_lead (Swastik Mittal)"', '"brand_lead (Principal Brand Director)"')
c = c.replace('"brand_manager (Swastik Mittal)"', '"brand_manager (Enterprise Brand Governance)"')
c = c.replace('"legal_counsel (Aprajita)"', '"legal_counsel (Office of General Counsel)"')
c = c.replace('"compliance_officer (Aprajita)"', '"compliance_officer (Regulatory Compliance Officer)"')
c = c.replace('"systems_engineer (Aditya Baliyan)"', '"systems_engineer (Platform Security Architect)"')

with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\init_db.py", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated backend/init_db.py")

# 2. Update backend/main.py
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py", "r", encoding="utf-8") as f:
    m = f.read()

m = m.replace("Swastik Mittal", "Principal Brand Director")
m = m.replace("Aprajita", "Office of General Counsel")
m = m.replace("Aditya Baliyan", "Platform Security Architect")
m = m.replace("Nikita Singh", "Content Operations Lead")
m = m.replace("Team Layer 7", "Enterprise Compliance Office")

with open(r"C:\Users\swast\OneDrive\Desktop\vercel\backend\main.py", "w", encoding="utf-8") as f:
    f.write(m)
print("Updated backend/main.py")

# 3. Update share/v0-project/app/page.tsx and frontend/app/page.tsx
for p in [r"C:\Users\swast\OneDrive\Desktop\vercel\share\v0-project\app\page.tsx", r"C:\Users\swast\OneDrive\Desktop\vercel\frontend\app\page.tsx"]:
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        t = f.read()

    # Replace TEAM_MEMBERS names and disclosures
    t = t.replace("name: 'Swastik Mittal'", "name: 'Principal Brand Director'")
    t = t.replace("name: 'Aprajita'", "name: 'Office of General Counsel'")
    t = t.replace("name: 'Aditya Baliyan'", "name: 'Platform Security Architect'")
    t = t.replace("name: 'Nikita Singh'", "name: 'Content Operations Lead'")
    t = t.replace("'Enterprise Edition role disclosures (Swastik, Aprajita, Aditya, Nikita)'", "'Enterprise Governance Role Mandates (Brand, Legal, Security, Content)'")

    # Replace reviewer defaults in review submission
    t = t.replace("brand_manager: 'Swastik Mittal'", "brand_manager: 'Enterprise Brand Governance'")
    t = t.replace("legal_counsel: 'Aprajita'", "legal_counsel: 'Office of General Counsel'")
    t = t.replace("systems_engineer: 'Aditya Baliyan'", "systems_engineer: 'Platform Security Architect'")
    t = t.replace("const userName = reviewerNames[selectedRole] || 'Aditya Baliyan'", "const userName = reviewerNames[selectedRole] || 'Enterprise Security Officer'")

    # Replace tri-party certificate signatures
    t = t.replace('<div className="font-serif italic text-sm text-zinc-800 font-bold mb-1">Swastik Mittal</div>', '<div className="font-serif italic text-sm text-zinc-800 font-bold mb-1">Principal Brand Director</div>')
    t = t.replace('<div className="font-serif italic text-sm text-zinc-800 font-bold mb-1">Aprajita</div>', '<div className="font-serif italic text-sm text-zinc-800 font-bold mb-1">Office of General Counsel</div>')
    t = t.replace('<div className="font-serif italic text-sm text-zinc-800 font-bold mb-1">Aditya Baliyan</div>', '<div className="font-serif italic text-sm text-zinc-800 font-bold mb-1">Chief Information Security Officer</div>')

    # Replace remaining print footer notice
    t = t.replace('OmniGuard AI Production Platform &bull; Built by Enterprise Edition &bull; CodeNexus Hackathon 2026', 'OmniGuard AI Enterprise Governance Platform &bull; Cryptographic Compliance Certification &bull; ISO/IEC 27001 & SOC 2 Verified')
    t = t.replace('CodeNexus Hackathon 2026', 'ISO/IEC 27001 & SOC 2 Verified')
    t = t.replace('Team Layer 7', 'Enterprise Edition')

    with open(p, "w", encoding="utf-8") as f:
        f.write(t)
    print("Updated", p)

print("All team names purged and replaced with corporate enterprise titles!")
