import sqlite3

conn = sqlite3.connect('data/reviews.db')
c = conn.cursor()
c.execute("DELETE FROM reviews WHERE source IN ('twitter', 'instagram', 'tiktok')")
print(f"Deleted {c.rowcount} rows.")
conn.commit()
conn.close()
