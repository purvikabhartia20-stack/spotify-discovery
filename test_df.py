import sqlite3
import pandas as pd
conn = sqlite3.connect('data/reviews.db')
df = pd.read_sql_query("SELECT strftime('%Y-%m-%d', date) as day, sentiment, COUNT(*) as count FROM reviews WHERE tagged_at IS NOT NULL AND date IS NOT NULL AND sentiment != 'unclear' GROUP BY day, sentiment ORDER BY day", conn)
print(df)
