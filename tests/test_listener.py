import unittest
from lib.listener import Listener
from tests.sender import Sender
from time import sleep
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
        sleep(1)
        for id_ in range(5):
            for i in range(10):
                s = Sender(id_, self.host, self.port)
                text, reply = s.send()
                self.assertEqual(b'06', reply)
                listened = L.get_data()[0]
                self.assertEqual(text, f"{listened.id}%%{listened.data}")
                self.assertIsInstance(listened.timestamp, datetime.datetime)
        self.assertTrue(L.is_active())
        self.assertTrue(L.stop())




