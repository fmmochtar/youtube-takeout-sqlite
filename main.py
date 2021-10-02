import json
import sqlite3
from datetime import datetime

import generate_sqlite
import logging as log

# write your file path here
file_input = "watch-history.json"
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
file_sqlitedb = f"history_{date}.db"

file_data = open(file_input, 'r', encoding="UTF8").read()
history = json.loads(file_data, encoding="UTF8")

log.info(f'Loaded history data from {file_input}')
log.info(f'Found a total of {len(history)} videos watched')

x = len(history)
totalcount = len(history)
count = 1

conn = sqlite3.connect(file_sqlitedb)
c = conn.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='videos' ''')
if c.fetchone()[0]==1 :
    log.warning('Table exists in the SQLite database. Delete it first.')
    conn.commit()
    conn.close()
else:
    log.warning("Table doesn't exist. Creating data ...")
    conn.commit()
    conn.close()
    generate_sqlite.generate(file_input, file_sqlitedb)


    
