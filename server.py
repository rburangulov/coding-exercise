from multiprocessing.connection import Listener
import config

listener = Listener((config.server_address, config.server_port))

while True:
    conn = listener.accept()
    while True:
        msg = conn.recv()
        if msg == 'close connection':
            conn.close()
            break
        print(msg)
listener.close()
