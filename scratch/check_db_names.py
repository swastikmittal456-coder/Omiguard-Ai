import sqlite3

conn = sqlite3.connect(r'C:\Users\swast\OneDrive\Desktop\vercel\backend\omniguard.db')
cursor = conn.cursor()
tables = [r[0] for r in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
names = ['swastik', 'aprajita', 'baliyan', 'nikita', 'layer 7']
found = []
for t in tables:
    rows = cursor.execute(f"SELECT * FROM {t}").fetchall()
    for row in rows:
        r_str = str(row).lower()
        for n in names:
            if n in r_str:
                found.append((t, n, str(row)[:100]))
print(f"Database matches: {len(found)}")
for t, n, r in found:
    print(f"Table {t}: {n} -> {r}")
