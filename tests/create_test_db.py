import sqlite3
from tests.id_gen import id_generator
import random
from datetime import datetime, timedelta

def create_test_db(filename, ids, messages):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE last_messages (dev_id TEXT NOT NULL PRIMARY KEY, data TEXT, balance REAL, received_at TEXT)")
    cur.execute("CREATE TABLE messages (dev_id TEXT NOT NULL, data TEXT, balance REAL, received_at TEXT)")
    cur.execute("CREATE TABLE users (username TEXT NOT NULL PRIMARY KEY, password_secret NOT NULL, last_login TEXT)")
    cur.execute("INSERT INTO users(username, password_secret) VALUES ('admin', '25d55ad283aa400af464c76d713c07ad')")
    conn.commit()
    id_list = [str(i) for i in range(ids)]
    for i in range(messages):
        id_ = random.choice(id_list)
        text = id_generator(random.randint(12, 24))
        timestamp = ((datetime.now()) - timedelta(days = random.randint(1, 5))).strftime("%Y-%m-%d %H:%M:%S.%f")
        cur.execute("""INSERT OR REPLACE 
                       INTO last_messages(dev_id, data, balance, received_at) 
                       VALUES (?, ?, ?, ?)""",
                    (id_, text, 123, timestamp))
        cur.execute("INSERT INTO messages(dev_id, data, balance, received_at) VALUES (?, ?, ?, ?)",
                    (id_, text, 123, timestamp))
    conn.commit()
    return True

