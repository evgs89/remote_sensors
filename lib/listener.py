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
            balance = data_list[2] if len(data_list) == 3 else None
            result = True
            print('RECEIVED MESSAGE:\nID={id}\nDATA={data}\nBALANCE={bal}'.format(id = id_,
                                                                                  data = text,
                                                                                  bal = balance, ))
        except IndexError as e:
            print("RECEIVED: ", str(data))
            id_ = 'ERROR'
            text = str(data)
            balance = None
        message = Message(datetime.datetime.now(), id_, text, balance)
        return result, message


    def _main_loop(self):
        while self._listener_active:
            try:
                sock = socket.socket()
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    sock.bind((self.host, self.port))
                    sock.listen(1)
                except OSError as msg:
                    print("OSError: ", str(msg))
                    sock.close()
                    sleep(1)
                    # return False
                while self._listener_active:
                    try:
                        conn, addr = sock.accept()
                        data = conn.recv(self.data_block_size)
                        if data:
                            result, message = self._parse_message(data)
                            conn.send(b'\x06' if result else b'\x15')
                            self.queue.put_nowait(message)
                            """
                            this looks a bit complicated, but we've a problem. Sender can't close socket,
                            so I close it manually right after receiving data
                            """
                            sock.shutdown(socket.SHUT_RDWR)
                            sock.close()
                            sock = socket.socket()
                    except OSError:
                        break
                    except Exception as e:
                        print("PROCESSING MESSAGE ERROR: ", str(e))
                        sock.close()
            except OSError as e:
                print('SOCKET BUSY', str(e))
                sleep(1)
            except Exception as e:
                print(str(e))
