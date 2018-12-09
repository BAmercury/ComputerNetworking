#!/usr/bin/env python

#!/usr/bin/env python

import socket


TCP_IP = '192.168.1.126'
TCP_PORT = 5005
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

keep_alive = True
while keep_alive:
    payload = raw_input("Please enter a string: ")
    s.send(payload)
    data = s.recv(BUFFER_SIZE)
    print(data)
    if (data == "Bye"):
        keep_alive = False
        break
s.close()
