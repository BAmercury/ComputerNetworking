#!/usr/bin/env python

import socket


TCP_IP = '192.168.1.126'
TCP_PORT = 5005
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

keep_alive = True

def generate_cda():
    words = []
    number_of_words = raw_input("Please enter how many words you would like to check: ")
    for i in xrange(0, int(number_of_words)):
        words.append(raw_input("Enter a word: "))

    words = ["2"] + words
    word_string = ",".join(words)
    return word_string



while keep_alive:
    print("---Commands---")
    print("1: Send single word")
    print("2: Send multiple words")
    print("3: Exit and close connection")
    print("4: Total number of palindromes found")
    print("5: Return list of palindromes found")
    command = raw_input("Please enter a command: ")

    if (command == "1"):
        payload = []
        word = raw_input("Please give me a word: ")
        payload.append("1")
        payload.append(word)
        payload_string = ",".join(payload)
        s.send(payload_string)
        data = s.recv(BUFFER_SIZE)
        print(data)
    elif (command == "2"):
        payload = generate_cda()
        s.send(payload)
        data = s.recv(BUFFER_SIZE)
        print(data)
    elif (command == "4"):
        # Return result from server, the amount of palindromes found thus far:
        s.send("4") # Send the command to the server
        data = s.recv(BUFFER_SIZE) # Show server result
        print(data)
    elif (command == "5"):
        # Ask server to return list of all palindromes found
        s.send("5")
        data = s.recv(BUFFER_SIZE)
        print(data)
    elif (command == "3"):
        s.send("3")
        data = s.recv(BUFFER_SIZE)
        print(data)
        keep_alive = False
        break
    else:
        print("Please insert a command listed on the table")
s.close()