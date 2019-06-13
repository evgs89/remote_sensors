import datetime
import threading
import queue
import socket
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from collections import namedtuple


Message = namedtuple('Message', 'timestamp, id, data, balance')


class MyTCPHandler(BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        data = bytearray()
        print("DEBUG: HANDLE")
        while True:
            try:
                chunk = self.request.recv(1024)
                data += chunk
            except socket.timeout:
                print("timeout")
                break
            if not chunk: break
        result, message = self._parse_message(data)
        self.server.queue.put_nowait(message)

    def _parse_message(self, data):
        data = data.decode(encoding = 'ascii')
        result = False
        try:
            data_list = data.split('%%')
            id_ = data_list[0]
            text = data_list[1]
            balance = data_list[2] if len(data_list) == 3 else 0
            try: balance = float(balance)
            except ValueError: balance = 0
            result = True
            print('RECEIVED MESSAGE:\nID={id}\nDATA={data}\nBALANCE={bal}'.format(id = id_,
                                                                                  data = text,
                                                                                  bal = balance, ))
        except IndexError as e:
            print("RECEIVED: ", str(data))
            id_ = 'ERROR'
            text = str(data)
            balance = 0
        message = Message(datetime.datetime.now(), id_, text, balance)
        return result, message


class ThreadedServer(ThreadingMixIn, TCPServer):
    pass


class Listener(object):
    def __init__(self, host = '', port = 30110):
        self.port = port
        self.host = host
        self.data_block_size = 1024
        self.t = None
        self.queue = queue.Queue()
        self.server = None

    def start(self):
        if self.is_active():
            self.stop()
        TCPServer.allow_reuse_address = True
        self.server = TCPServer((self.host, self.port), MyTCPHandler)
        self.server.queue = self.queue
        self.t = threading.Thread(target = self.server.serve_forever)
        self.t.daemon = True
        self.t.start()
        return self.is_active()

    def stop(self):
        self.server.shutdown()
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

    def _start_server(self):
        self.server.serve_forever()

