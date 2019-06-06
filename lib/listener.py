import socket
import datetime
import threading, queue
from collections import namedtuple
from time import sleep


Message = namedtuple('Message', 'timestamp, id, data')


class Listener(object):
    def __init__(self, host = '', port = 30110):
        self.port = port
        self.host = host
        self.data_block_size = 1024
        self._listener_active = False
        self.t = None
        self.queue = queue.Queue()

    def start(self):
        if self.is_active(): self.stop()
        self._listener_active = True
        self.t = threading.Thread(target = self._main_loop, args = ())
        self.t.start()
        return self.is_active()

    def stop(self):
        self._listener_active = False
        while self.t.is_alive():
            # Loop hangs on sock.accept while there is no connection, so we'll create connection manually
            sock2 = socket.socket()
            try:
                sock2.connect((self.host, self.port))
                sock2.send(b'06')
            except ConnectionRefusedError:
                pass
            sock2.close()
            sleep(.1)
        return True

    def get_data(self):
        """
        Get all received data
        """
        data = []
        try:
            while not self.queue.empty():
                data.append(self.queue.get_nowait())
        except queue.Empty:
            pass
        return data

    def is_active(self):
        try:
            return self.t.is_alive()
        except AttributeError:
            return False

    def _main_loop(self):
        sock = socket.socket()
        try:
            sock.bind((self.host, self.port))
        except OSError as msg:
            print("OSError: ", str(msg))
            sock.close()
            return False
        sock.settimeout(1)
        sock.listen(1)
        conn, addr = sock.accept()
        while self._listener_active:
            data = conn.recv(self.data_block_size)
            if not data:
                conn, addr = sock.accept()
            else:
                data = data.decode(encoding = 'ascii')
                try:
                    id_, text = data.split('%%')
                    conn.send(b'06')
                except ValueError as e:
                    print(str(e))
                    id_ = 'ERROR'
                    text = str(data)
                    conn.send(b'15')
                self.queue.put_nowait(Message(datetime.datetime.now(), id_, text))
        sock.close()
