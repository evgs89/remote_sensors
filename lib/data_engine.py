import sqlite3
import os
import threading
from lib.listener import Listener
from time import sleep


class DataEngine(object):
    def __init__(self, host, port, db_file = 'db.sqlite'):
        self._db_file = db_file
        self.L = Listener(host, int(port))
        self._db_init()
        self._t = None
        self._sync_loop_enabled = True

    def _db_init(self):
        if not os.path.isfile(self._db_file):
            conn, cur = self._connect_db()
            cur.execute("CREATE TABLE last_messages (dev_id TEXT NOT NULL PRIMARY KEY, data TEXT, received_at TEXT)")
            cur.execute("CREATE TABLE messages (dev_id TEXT NOT NULL, data TEXT, received_at TEXT)")
            conn.commit()
        return True

    def _connect_db(self):
        conn = sqlite3.connect(self._db_file)
        cur = conn.cursor()
        return [conn, cur]

    def _sync_messages(self):
        conn, cur = self._connect_db()
        if not self.L.is_active(): self.L.start()
        data = self.L.get_data()
        for message in data:
            try:
                cur.execute("""INSERT OR REPLACE INTO last_messages(dev_id, data, received_at) 
                               VALUES (?, ?, ?)""",
                            (message.id, message.data, message.timestamp.strftime("%d-%m-%Y %H:%M:%S.%f")))
                cur.execute("INSERT INTO messages(dev_id, data, received_at) VALUES (?, ?, ?)",
                            (message.id, message.data, message.timestamp.strftime("%d-%m-%Y %H:%M:%S.%f")))
                conn.commit()
            except Exception as e:
                print(e)
                return False
        return True

    def _sync_loop(self, period):
        counter = period
        while self._sync_loop_enabled:
            if counter < period:
                counter += 1
                sleep(1)
            else:
                counter = 0
                self._sync_messages()

    def start_sync_loop(self, period = 1):
        self._sync_loop_enabled = True
        self._t = threading.Thread(target = self._sync_loop, args = (int(period) ,))
        self._t.start()
        return self._t.is_alive()

    def stop_sync_loop(self):
        self.L.stop()
        self._sync_loop_enabled = False
        while self._t.is_alive():
            sleep(.1)
        return True

    def sync_loop_is_alive(self):
        if self._t:
            return self._t.is_alive()

    def get_last_messages(self):
        conn, cur = self._db_init()
        try:
            cur.execute("SELECT dev_id, data, received_at FROM last_messages")
        except Exception as e:
            print('DB seems to be corrupted, error is: ', str(e))
        data = []
        rows = cur.fetchall()
        for row in rows:
            data.append(tuple(row))
        return data

    def get_messages_by_id(self, id_):
        conn, cur = self._db_init()
        try:
            cur.execute("SELECT dev_id, data, received_at FROM messages WHERE dev_id = ?", (str(id_), ))
        except Exception as e:
            print('DB seems to be corrupted, error is: ', str(e))
        data = []
        rows = cur.fetchall()
        for row in rows:
            data.append(tuple(row))
        return data








