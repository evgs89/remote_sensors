import socket
import datetime
import threading, queue
from collections import namedtuple
from time import sleep


Message = namedtuple('Message', 'timestamp, id, data, balance')


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
                sock2.send(b'\x06')
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

    def _create_socket(self):
        print("CREATE SOCKET")
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((self.host, self.port))
            print("BIND OK")
        except OSError as msg:
            sock.close()
            print("OS ERROR: ", msg)
            return False
        sock.listen(1)
        conn, addr = sock.accept()
        print("CLIENT CONNECTED")
        return sock, conn, addr

    def _main_loop(self):
        while self._listener_active:
            try:
                sock, conn, addr = self._create_socket()
                data = conn.recv(self.data_block_size)
                if data == b'\x06':
                    conn.send(b'\x06')
                    print("EOT")
                    sock.close()
                elif data:
                    result, message = self._parse_message(data)
                    conn.send(b'\x06' if result else b'\x15')
                    self.queue.put_nowait(message)
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    print("RECEIVED: ", str(data))
            except Exception as e:
                print(str(e))

