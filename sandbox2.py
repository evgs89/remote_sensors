import socket
from socketserver import BaseRequestHandler, TCPServer
import threading, queue
from time import sleep

Q = queue.Queue()


class MyTCPHandler(BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        data = bytearray()
        while True:
            try:
                chunk = self.request.recv(1024)
                data += chunk
                print(data)
            except socket.timeout:
                break
            if not chunk: break
        self.server.queue.put_nowait(data)


def start_server(host, port, q):
    TCPServer.allow_reuse_address = True
    server = TCPServer((host, port), MyTCPHandler)
    server.queue = q
    server.serve_forever()


if __name__ == '__main__':
    try:
        TCPServer.allow_reuse_address = True
        server = TCPServer(('', 9090), MyTCPHandler)
        server.queue = Q
        t = threading.Thread(target = server.serve_forever)
        t.daemon = True
        t.start()
        while True:
            try:
                data = Q.get_nowait()
                if data:
                    print("RECEIVED: ", data.decode('ascii'))
            except queue.Empty:
                sleep(.1)
    except KeyboardInterrupt:
        print('exititng')
        server.shutdown()
        print('ok')

