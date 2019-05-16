import unittest
import configparser

from lib.data_engine import DataEngine
from tests.id_gen import id_generator
from tests.sender import sender


class test_DataEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conf = configparser.ConfigParser()
        cls.conf['host'] = ''
        cls.conf['port'] = 30110
        cls.conf['db_update_period'] = 60



