import unittest
import os
from time import sleep
from datetime import datetime, timedelta

from lib.data_engine import DataEngine
from tests.create_test_db import create_test_db
from tests.sender import Sender


class test_DataEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = ''
        cls.port = 30112
        cls.period = 1

    def test_start_stop_sync_loop(self):
        dbfile = 'test_start_stop.sqlite'
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(os.path.isfile(dbfile))
        self.assertTrue(data_engine.start_sync_loop(1))
        sleep(1)
        for i in range(10):
            sender = Sender(i, self.host, self.port)
            self.assertIsNotNone(sender.send(balance = 10))
        self.assertTrue(data_engine.stop_sync_loop())
        os.remove(dbfile)

    def test_get_last_messages(self):
        dbfile = 'test_get_last_messages.sqlite'
        create_test_db(dbfile, 10, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        data, pages = data_engine.get_last_messages()
        self.assertTrue(len(data) > 0)
        self.assertIsInstance(data[0], tuple)
        self.assertIsInstance(data[0][1], str)
        sleep(2)
        os.remove(dbfile)

    def test_get_all_messages_by_id(self):
        ## TODO: sorting not tested but implemented
        dbfile = 'test_get_messages_id.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        data, pages = data_engine.get_messages_by_id(0)
        self.assertEqual(100, len(data))
        self.assertIsInstance(data[0], tuple)
        self.assertEqual('0', data[0][0])
        self.assertIsInstance(data[0][1], str)
        os.remove(dbfile)

    def test_delete_messages(self):
        dbfile = 'test_delete_messages.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        data, pages = data_engine.get_messages_by_id(0)
        date_before = datetime.now() - timedelta(days = 2)
        self.assertEqual(100, len(data))
        counter = 0
        for row in data:
            if datetime.strptime(row[3], data_engine.datetime_format) < date_before: counter += 1
        deleted = data_engine.delete_messages(date_before = date_before)
        self.assertEqual(counter, deleted)
        dbfile2 = 'test_delete_old_messages.sqlite'
        create_test_db(dbfile2, 2, 100)
        data_engine = DataEngine(self.host, self.port, dbfile2)
        data, pages = data_engine.get_messages_by_id(0)
        counter = 0
        for row in data:
            if row[0] == '0': counter += 1
        deleted = data_engine.delete_messages(id_ = 0)
        self.assertEqual(counter, deleted)
        os.remove(dbfile)
        os.remove(dbfile2)

    def test_autoclean_old_messages(self):
        dbfile = 'test_auto_delete_old_messages.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile, 2)
        data, pages = data_engine.get_messages_by_id(0)
        date_before = datetime.now() - timedelta(days = 2)
        counter = 0
        for row in data:
            if datetime.strptime(row[3], data_engine.datetime_format) < date_before: counter += 1
        records = len(data)
        data_engine.get_last_messages()
        sleep(2)
        data, pages = data_engine.get_messages_by_id(0)
        fresh = len(data)
        self.assertTrue(records == fresh + counter)
        os.remove(dbfile)

    def test_validate_user(self):
        dbfile = 'test_users.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(data_engine.validate_user('admin', '12345678'))
        self.assertFalse(data_engine.validate_user('admin', '1234567890'))
        os.remove(dbfile)

    def test_validate_session(self):
        dbfile = 'test_users_session.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        session_id = data_engine.validate_user('admin', '12345678')
        self.assertTrue(data_engine.validate_session(session_id))
        os.remove(dbfile)

    def test_change_password(self):
        dbfile = 'test_users_chpwd.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(data_engine.validate_user('admin', '12345678'))
        self.assertTrue(data_engine.change_password('admin', '12345678', '87654321'))
        self.assertTrue(data_engine.validate_user('admin', '87654321'))
        self.assertFalse(data_engine.change_password('admin', '12345678', '87654321'))
        os.remove(dbfile)

    def test_create_user(self):
        dbfile = 'test_users_create.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(data_engine.add_user('testuser'))
        self.assertTrue(data_engine.validate_user('testuser', '12345678'))
        os.remove(dbfile)

    def test_get_user_list(self):
        dbfile = 'test_users_getlist.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(data_engine.add_user('testuser1'))
        self.assertTrue(data_engine.add_user('testuser2'))
        lst = data_engine.get_user_list()
        self.assertEqual(3, len(lst))
        self.assertTrue('testuser1' in lst)
        os.remove(dbfile)

    def test_delete_user(self):
        dbfile = 'test_users_delete.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(data_engine.add_user('testuser1'))
        self.assertTrue(data_engine.delete_user('admin', '12345678', 'testuser1'))
        self.assertEqual(1, len(data_engine.get_user_list()))
        os.remove(dbfile)


