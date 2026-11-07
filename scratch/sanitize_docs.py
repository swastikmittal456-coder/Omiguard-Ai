with open(r"C:\Users\swast\OneDrive\Desktop\vercel\README.md", "r", encoding="utf-8") as f:
    r = f.read()
r = r.replace("Team Layer 7", "OmniGuard Core Team")
r = r.replace("team layer 7", "OmniGuard Core Team")
r = r.replace("hackathon", "enterprise")
r = r.replace("Hackathon", "Enterprise")
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\README.md", "w", encoding="utf-8") as f:
    f.write(r)

with open(r"C:\Users\swast\OneDrive\Desktop\vercel\DEPLOYMENT.md", "r", encoding="utf-8") as f:
    d = f.read()
d = d.replace("Team Layer 7", "OmniGuard Core Team")
d = d.replace("team layer 7", "OmniGuard Core Team")
d = d.replace("hackathon", "enterprise")
d = d.replace("Hackathon", "Enterprise")
with open(r"C:\Users\swast\OneDrive\Desktop\vercel\DEPLOYMENT.md", "w", encoding="utf-8") as f:
    f.write(d)

print("Sanitized README.md and DEPLOYMENT.md")
