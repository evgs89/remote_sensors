import unittest
from lib.listener import Listener
from tests.sender import Sender
from time import sleep
import datetime


class test_Listener(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = ''
        cls.port = 30112

    def test_start_stop(self):
        L = Listener(self.host, self.port)
        self.assertTrue(L.start())
        self.assertTrue(L.is_active())
        self.assertTrue(L.stop())

    def test_get_data(self):
        def get_data_now(listener):
            for i in range(3):
                data = listener.get_data()
                if len(data) > 0: return data
                else: sleep(.1)
        L = Listener(self.host, self.port)
        self.assertTrue(L.start())
        sleep(1)
        for id_ in range(5):
            for balance in [None, 1, 2, 3]:
                s = Sender(id_, self.host, self.port)
                text, reply = s.send(balance = balance)
                self.assertEqual(b'\x06', reply)
                listened = get_data_now(L)[0]
                if balance:
                    self.assertEqual(text, "{id}%%{data}%%{balance}".format(id = listened.id,
                                                                            data = listened.data,
                                                                            balance = balance))
                else:
                    self.assertEqual(text, "{id}%%{data}".format(id = listened.id, data = listened.data))
                self.assertIsInstance(listened.timestamp, datetime.datetime)
                sleep(.1)
        self.assertTrue(L.is_active())
        self.assertTrue(L.stop())




