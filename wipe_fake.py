import sqlite3

conn = sqlite3.connect('data/reviews.db')
c = conn.cursor()
c.execute("DELETE FROM reviews WHERE summary LIKE 'User feedback regarding %' OR summary LIKE 'User complained about issue on %'")
print(f"Deleted {c.rowcount} fake rows.")
conn.commit()
conn.close()
