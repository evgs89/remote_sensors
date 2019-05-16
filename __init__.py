from lib.listener import Listener
import configparser


class WebServer(object):
    def __init__(self):
        self.config = configparser.ConfigParser(allow_no_value = True)
        with open('settings.ini', 'r') as conffile:
            self.config.read(conffile)
        self.listener = Listener(host = self.config['socket'].get('host', ''),
                                 port = int(self.config['socket']['port']))

