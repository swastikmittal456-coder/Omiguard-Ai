path = r"C:\Users\swast\OneDrive\Desktop\vercel\scratch\run_full_system_test.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace('"user_name": "Aprajita"', '"user_name": "Office of General Counsel"')
c = c.replace('Legal Counsel (Aprajita)', 'Office of General Counsel')
c = c.replace('forbidden = ["judge presets", "judge guide", "100-pt rubric", "100-point rubric", "team layer 7"]', 'forbidden = ["judge presets", "judge guide", "100-pt rubric", "100-point rubric", "team layer 7", "swastik", "aprajita", "baliyan", "nikita"]')

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Updated run_full_system_test.py successfully!")
