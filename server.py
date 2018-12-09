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

def isPalindrome(data):
    if len(data) < 2:
        #If the string has 0 or 1 characters, the string conforms to the palindrome definition
        return True
    if data[0] != data[-1]:
        #If the string has more than one character, check that the first and last item of the string are equivalent
        return False
    return isPalindrome(data[1:-1])
    #The first and last items of the string are equivalent, so remove the first and last items of the string and continue checking



class ClientCallBack(threading.Thread):

    def __init__(self,ip,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
    def run(self):
        while True:
            data = conn.recv(BUFFER_SIZE)
            data_list = data.split(",")
            if (data_list[0] == "1"):
                result = isPalindrome(data[1])
                if (result == True):
                    conn.send("Your word is a palindrome")
                else:
                    conn.send("Your word is not a palindrome")
            elif (data_list[0] == "2"):
                data_list.remove("2")
                results = []
                for word in data_list:
                    results.append(str(isPalindrome(word)))
                results_string = ",".join(results)
                conn.send(results_string)
            elif (data_list[0] == "3"):
                conn.send("Bye")
                break
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
        for t in threads:
            t.join()
        server_socket.close()
    except KeyboardInterrupt:
        for t in threads:
            t.join()
        server_socket.close()
        pass



