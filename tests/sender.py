import socket

from tests.id_gen import id_generator


class Sender(object):
    def __init__(self, id_, host, port):
        self.id = id_
        self.host = host
        self.port = port

    def send(self, text = None):
        if not text or type(text) not in [str, int, bytes]:
            text = str(self.id) + '%%' + id_generator()
        try:
            if type(text) == int:
                text = str(text)
            if type(text) == str:
                text = text.encode('ascii')
            sock = socket.socket()
            sock.connect((self.host, self.port))
            sock.send(text)
            reply = sock.recv(1024)
            assert (reply == b'06' or reply == b'15')
            sock.close()
            return text.decode('ascii'), reply
        except ConnectionRefusedError:
            print('Socket {host}:{port} is inactive or busy'.format(host = self.host, port = self.port))
            return text, None
