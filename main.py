import json
import sqlite3

import generate_sqlite

# write your file path here
file_input = "watch-history.json"
file_sqlitedb = "history.db"

file_data = open(file_input, 'r', encoding="UTF8").read()
history = json.loads(file_data, encoding="UTF8")

print(f'Loaded history data from {file_input}')
print(f'Found a total of {len(history)} videos watched')

x = len(history)
totalcount = len(history)
count = 1

conn = sqlite3.connect(file_sqlitedb)
c = conn.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='videos' ''')
if c.fetchone()[0]==1 :
    print('Table exists in the SQLite database. Delete it first.')
    conn.commit()
    conn.close()
else:
    print("Table doesn't exist. Creating data ...")
    conn.commit()
    conn.close()
    generate_sqlite.generate(file_input, file_sqlitedb)


    
