with open(r"C:\Users\swast\OneDrive\Desktop\vercel\scratch\run_full_system_test.py", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("Δ", "Delta")
c = c.replace("Î”", "Delta")

# Ensure UTF-8 on Windows
if "sys.stdout.reconfigure(encoding='utf-8')" not in c:
    c = "import sys\nif hasattr(sys.stdout, 'reconfigure'):\n    sys.stdout.reconfigure(encoding='utf-8')\n" + c

with open(r"C:\Users\swast\OneDrive\Desktop\vercel\scratch\run_full_system_test.py", "w", encoding="utf-8") as f:
    f.write(c)

print("Safely updated run_full_system_test.py")
