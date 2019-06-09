import sqlite3
import os
import threading
from lib.listener import Listener
from time import sleep
from datetime import datetime, timedelta


class DataEngine(object):
    def __init__(self, host, port, db_file = 'db.sqlite'):
        self.datetime_format = "%Y-%m-%d %H:%M:%S.%f" # it's not familiar for Russia, but sorting would work correctly
        self._db_file = db_file
        self.L = Listener(host, int(port))
        self._db_init()
        self._t = None
        self._sync_loop_enabled = True

    def _db_init(self):
        if not os.path.isfile(self._db_file):
            conn, cur = self._connect_db()
            cur.execute("CREATE TABLE last_messages (dev_id TEXT NOT NULL PRIMARY KEY, data TEXT, balance REAL, received_at TEXT)")
            cur.execute("CREATE TABLE messages (dev_id TEXT NOT NULL, data TEXT, balance REAL, received_at TEXT)")
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
                cur.execute("""INSERT OR REPLACE INTO last_messages(dev_id, data, balance, received_at) 
                               VALUES (?, ?, ?, ?)""",
                            (message.id, message.data, message.balance, message.timestamp.strftime(self.datetime_format)))
                cur.execute("INSERT INTO messages(dev_id, data, balance, received_at) VALUES (?, ?, ?, ?)",
                            (message.id, message.data, message.balance, message.timestamp.strftime(self.datetime_format)))
            except Exception as e:
                print(e)
                return False
        conn.commit()
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

    def get_last_messages(self, sort_by = 'received_at', reverse = False, page = 0, page_size = 100):
        conn, cur = self._connect_db()
        try:
            cur.execute("SELECT COUNT(*) FROM last_messages")
            count = cur.fetchone()[0]
            pages = int(count / page_size) + int(count % page_size != 0)  # get num of pages to show
            args = (page_size, page_size * (page - 1))
            cur.execute("""
            SELECT dev_id, data, balance, received_at 
            FROM last_messages 
            ORDER BY {0} {1} 
            LIMIT ? 
            OFFSET ?;
                        """.format(sort_by, 'DESC' if reverse else 'ASC'), args)
        except Exception as e:
            print('DB seems to be corrupted, error is: ', str(e))
        data = []
        rows = cur.fetchall()
        for row in rows:
            data.append(tuple(row))
        return data, pages

    def get_messages_by_id(self, id_, sort_by = 'received_at', reverse = False, page = 0, page_size = 100):
        if sort_by not in ['dev_id', 'data', 'balance', 'received_at']: sort_by = 'received_at'
        conn, cur = self._connect_db()
        try:
            cur.execute("SELECT COUNT(*) FROM messages WHERE dev_id = ?", (str(id_), ))
            count = cur.fetchone()[0]
            pages = int(count/page_size) + int(count % page_size != 0) # get num of pages to show
            cur.execute("""
                        SELECT dev_id, data, balance, received_at 
                        FROM messages 
                        WHERE dev_id = ?
                        ORDER BY {key} {rev}
                        LIMIT ?
                        OFFSET ?; 
                        """.format(key = sort_by, rev = 'DESC' if reverse else 'ASC'),
                        (str(id_), page_size, page_size * (page - 1)))
            rows = cur.fetchall()
            data = [tuple(row) for row in rows]
            return data, pages
        except Exception as e:
            print('DB seems to be corrupted, error is: ', str(e))
            return [], 0


    def delete_messages(self,
                        id_ = None,
                        date_before: datetime = datetime.now() + timedelta(days = 1)):
        """
        delete all messages or only filtered
        :param id_: messages from this id would be deleted
        :param date_before: all messages received before this date would be deleted
        :return:
        """
        conn, cur = self._connect_db()
        try:
            cur.execute("SELECT dev_id, data, received_at FROM messages")
        except Exception as e:
            print('DB seems to be corrupted, error is: ', str(e))
        rows = cur.fetchall()
        counter_deleted = 0
        for row in rows:
            if datetime.strptime(row[2], self.datetime_format) < date_before:
                if not id_:
                    cur.execute("DELETE FROM messages WHERE received_at = ?", (row[2], ))
                    cur.execute("DELETE FROM last_messages WHERE received_at = ?", (row[2], ))
                    counter_deleted += 1
                else:
                    if str(row[0]) == id_:
                        cur.execute("DELETE FROM messages WHERE received_at = ? AND dev_id = ?", (row[2], str(id_)))
                        cur.execute("DELETE FROM last_messages WHERE dev_id = ?", (str(id_), ))
                        counter_deleted += 1
        conn.commit()
        return counter_deleted







