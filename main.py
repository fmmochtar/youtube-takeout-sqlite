import json
import os
import sys
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

import generate_sqlite
import generate_sqlalchemy
import logging as log

# SQL backend (sqlalchemy/sqlite3)
#sql_backend_env = os.getenv('SQL_BACKEND')
#print(sql_backend_env)
sql_backend_env = 'sqlalchemy'

def start(input):
    #file_input = "watch-history.json"
    file_input = input
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_sqlitedb = f"yt_history_{date}.db"

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
        # conn.commit()
        # conn.close()
        if sql_backend_env == "sqlalchemy":
            print("Information: \nSQL backend: SQLAlchemy")
            generate_sqlalchemy.generate(file_input, file_sqlitedb)
        elif sql_backend_env == "sqlite3" or "sqlite":
            print("Information: \nSQL backend: SQLite3")
            generate_sqlite.generate(file_input, file_sqlitedb)
        else:
            print("Information: \nSQL backend: SQLAlchemy")
            generate_sqlalchemy.generate(file_input, file_sqlitedb)


# write your file path here
if len(sys.argv) < 2:
    input = "watch-history.json"
    start(input)
elif len(sys.argv[1]) >= 1:
    input = sys.argv[1]
    start(input)
else:
    input = "watch-history.json"
    start(input)  

