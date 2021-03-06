import socket
from lib.id_gen import id_generator


class Sender(object):
    def __init__(self, id_, host, port):
        self.id = id_
        self.host = host
        self.port = port

    def send(self, text = None, balance = None):
        if not text or type(text) not in [str, int, bytes]:
            text = str(self.id) + '%%' + id_generator()
        if balance:
            text = text + '%%' + str(balance)
        try:
            text = str(text).encode('ascii')
            sock = socket.socket()
            sock.connect((self.host, self.port))
            sock.send(text)
            sock.close()
            return text.decode('ascii')
        except ConnectionRefusedError:
            print('Socket {host}:{port} is inactive or busy'.format(host = self.host, port = self.port))
            return text, None
