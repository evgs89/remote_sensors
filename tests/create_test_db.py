import sqlite3
from tests.id_gen import id_generator
import random
import datetime


def create_test_db(filename, ids, messages):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS last_messages (dev_id TEXT NOT NULL PRIMARY KEY, data TEXT, received_at TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS messages (dev_id TEXT NOT NULL, data TEXT, received_at TEXT)")
    conn.commit()
    id_list = [str(i) for i in range(ids)]
    for i in range(messages):
        id_ = random.choice(id_list)
        text = id_generator(random.randint(12, 24))
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
        cur.execute("""INSERT OR REPLACE INTO last_messages(dev_id, data, received_at) 
                                       VALUES (?, ?, ?)""",
                    (id_, text, timestamp))
        cur.execute("INSERT INTO messages(dev_id, data, received_at) VALUES (?, ?, ?)",
                    (id_, text, timestamp))
    conn.commit()
    return True

