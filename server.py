# using Python 2.7

from socket import *
import threading
from SocketServer import ThreadingMixIn
 
BUFFER_SIZE = 1024
TCP_IP = '192.168.1.126'
TCP_PORT = 5005



server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

threads = []

keep_alive = True

class ClientCallBack(threading.Thread):

    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
    def run(self):
        while True:
            data = conn.recv(BUFFER_SIZE)
            if (data == "Exit"):
                break
            conn.send("Got It")
        conn.send("Bye")
        conn.close()

if __name__ == '__main__':
    try:
        while keep_alive:
            server_socket.listen(4)
            print("Waiting for clients to connect...")
            (conn, (ip,address)) = server_socket.accept()
            print("Client connected. Address: ", address)
            newThread = ClientCallBack(ip,address)
            newThread.start()
            threads.append(newThread)
            #callback_thread = threading.Thread(target=client_callback(conn, address))
            #callback_thread.start()
            #threads.append(callback_thread)
        for t in threads:
            t.join()
        server_socket.close()
    except KeyboardInterrupt:
        for t in threads:
            t.join()
        server_socket.close()
        pass



