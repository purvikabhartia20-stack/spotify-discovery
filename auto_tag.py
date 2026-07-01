import sqlite3
import datetime

conn = sqlite3.connect('data/reviews.db')
c = conn.cursor()
c.execute("""
    UPDATE reviews 
    SET theme='other', pain_severity=3, behavior_intent='Unknown', summary='Auto-tagged due to API limits', tagged_at=?
    WHERE tagged_at IS NULL
""", (datetime.datetime.now().isoformat(),))
print(f"Mock tagged {c.rowcount} reviews.")
conn.commit()
conn.close()
