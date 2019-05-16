import unittest
import os
from time import sleep

from lib.data_engine import DataEngine
from tests.create_test_db import create_test_db
from tests.sender import Sender


class test_DataEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = ''
        cls.port = 30110
        cls.period = 1

    def test_start_stop_sync_loop(self):
        dbfile = 'test_start_stop.sqlite'
        data_engine = DataEngine(self.host, self.port, dbfile)
        self.assertTrue(os.path.isfile(dbfile))
        self.assertTrue(data_engine.start_sync_loop(1))
        sleep(1)
        for i in range(10):
            sender = Sender(i, self.host, self.port)
            self.assertIsNotNone(sender.send())
        self.assertTrue(data_engine.stop_sync_loop())
        os.remove(dbfile)

    def get_last_messages(self):
        dbfile = 'test_get_last_messages.sqlite'
        create_test_db(dbfile, 10, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        data = data_engine.get_last_messages()
        self.assertTrue(len(data) > 0)
        self.assertIsInstance(data[0], tuple)
        self.assertIsInstance(data[0][1], str)
        os.remove(dbfile)

    def get_all_messages_by_id(self):
        dbfile = 'test_get_last_messages.sqlite'
        create_test_db(dbfile, 1, 100)
        data_engine = DataEngine(self.host, self.port, dbfile)
        data = data_engine.get_messages_by_id(0)
        self.assertEqual(100, len(data))
        self.assertIsInstance(data[0], tuple)
        self.assertEqual('0', data[0][0])
        self.assertIsInstance(data[0][1], str)
        os.remove(dbfile)





