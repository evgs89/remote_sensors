import socket
from time import sleep


while True:
    try:
        print("START")
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 9090))
        sock.listen(1)
        while True:
            try:
                conn, addr = sock.accept()
                print("LISTENING")
                data = conn.recv(1024)
                if data:
                    print("RECEIVED: ", data.decode('ascii'))
                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()
                    print("SOCKET CLOSED")
                    sock = socket.socket()
            except socket.timeout:
                pass
            except OSError:
                print("RESET")
                break
            except Exception as e:
                print(str(e))
                sock.close()
    except OSError as e:
        print('SOCKET BUSY', str(e))
        sleep(1)
    except Exception as e: print(str(e))

