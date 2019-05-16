import unittest
from lib.listener import Listener
from tests.sender import sender
import datetime


class test_Listener(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = ''
        cls.port = 30110

    def test_start_stop(self):
        L = Listener(self.host, self.port)
        self.assertTrue(L.start())
        self.assertTrue(L.is_active())
        self.assertTrue(L.stop())

    def test_get_data(self):
        L = Listener(self.host, self.port)
        self.assertTrue(L.start())
        for id_ in range(5):
            for i in range(10):
                text, reply = sender(id_, self.host, self.port)
                self.assertEqual(reply, b'06')
                listened = L.get_data()[0]
                self.assertEqual(f"{listened.id}%%{listened.data}", text)
                self.assertIsInstance(listened.timestamp, datetime.datetime)
        self.assertTrue(L.is_active())
        self.assertTrue(L.stop())




