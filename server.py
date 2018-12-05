# using Python 2.7

from socket import *
import threading
 
BUFFER_SIZE = 1024
TCP_IP = '192.168.1.126'
TCP_PORT = 5005



server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

keep_alive = True

def client_callback(conn, addr):
    keep_alive = True
    while keep_alive:
        data = conn.recv(BUFFER_SIZE)
        print("received some data: ", data)
        if (data == "Exit"):
            keep_alive = False
            break
        else:
            conn.send("Got it")
    reply = "Bye"
    conn.send(reply)
    conn.close()

if __name__ == '__main__':
    try:
        while keep_alive:
            print("Waiting for clients to connect...")
            conn, address = server_socket.accept()
            print("Client connected. Address: ", address)
            callback_thread = threading.Thread(target=client_callback(conn, address))
            callback_thread.start()
    except KeyboardInterrupt:
        pass



