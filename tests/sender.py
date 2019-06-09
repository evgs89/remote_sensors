import socket
from tests.id_gen import id_generator
from time import sleep


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
            try:
                reply = sock.recv(1024)
                assert (reply == b'\x06' or reply == b'\x15')
            except:
                reply = None
            sock.close()
            return text.decode('ascii'), reply
        except ConnectionRefusedError:
            print('Socket {host}:{port} is inactive or busy'.format(host = self.host, port = self.port))
            return text, None
