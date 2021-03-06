#!/usr/bin/env python
# Using Python 2.7
import socket
import os
import sys

# Server Host IP address and port information
TCP_IP = '192.168.1.126'
TCP_PORT = 5005
# TCP message buffer size
BUFFER_SIZE = 1024


# Create TCP socket, use AF_INET family of addresses
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the TCP Server
s.connect((TCP_IP, TCP_PORT))

# Boolean to control the main application loop
keep_alive = True

# Boolean to see if user requests a non persistent connection
nonpersis = False

# Generate a large comma delimited string message
def generate_cda():
    words = []
    number_of_words = raw_input("Please enter how many words you would like to check: ")
    for i in xrange(0, int(number_of_words)):
        words.append(raw_input("Enter a word: "))

    words = ["2"] + words
    word_string = ",".join(words)
    return word_string




# Main application loop
while keep_alive:
    # Show list of available commands to the user
    print("----Commands----")
    print("1: Send single word")
    print("2: Send multiple words")
    print("3: Exit and close connection")
    print("4: Total number of palindromes found")
    print("5: Return list of palindromes found")
    print("6: Return latest palindrome found")
    print("7: Delete all found palindromes")
    print("8: Delete palindromes at specfic positions")
    print("9: Request non-persistent connection")
    command = raw_input("Please enter a command: ")
	# Parse the user input command. Evaluated as a string
    if (command == "1"):
		# Send a single word to the server for evaluation
        payload = []
        word = raw_input("Please give me a word: ")
		# Append the command to the payload
        payload.append("1")
        payload.append(word)
        payload_string = ",".join(payload) # Convert Python list to a comma delimited string
        s.send(payload_string)
		# Recieve server response and display
        data = s.recv(BUFFER_SIZE)
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "2"):
		# Prompt user to input a list of words
        payload = generate_cda()
		# Send the comma delimited string payload
        s.send(payload)
        data = s.recv(BUFFER_SIZE)
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "4"):
        # Return result from server, the amount of palindromes found thus far:
        s.send("4") # Send the command to the server
        data = s.recv(BUFFER_SIZE) # Show server result
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "5"):
        # Ask server to return list of all palindromes found
        s.send("5")
        data = s.recv(BUFFER_SIZE)
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "6"):
        # Ask server to return the lastest palindrome found
        s.send("6")
        data = s.recv(BUFFER_SIZE)
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "7"):
        # Ask server to delete all the palindromes found
        # Server should send a status reply saying if it was successful
        s.send("7")
        data = s.recv(BUFFER_SIZE)
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "8"):
        # Ask server to remove palindromes from list at specfic positions
        # Server will send back a list of the latest palindromes after the deletion operation
        list_positions = []
        user_rolling_input = True
        print("Please give me the positions of the palindromes you want to delete. Remember the list is indexed starting with 0")
        print("When you are finished, just write \"done\"")
        while (user_rolling_input):
            user_input = raw_input("Give me a position: ")
            # check if user is doing putting in position input
            if (user_input == "done"):
                print("Sending positions to server")
                user_rolling_input = False
            else:

                try:
                    # Verification if user input is a number
                    val = int(user_input)
                    if (val >= 0):
                        list_positions.append(user_input)
                except ValueError:
                    print("This is not a valid position, please try again")
        # Now send this list of positions to the server
        list_positions = ["8"] + list_positions # Insert the command to front of list
        payload = ",".join(list_positions)
        s.send(payload)  
        data = s.recv(BUFFER_SIZE)
        print(data)
        # If non-persistent connection was requested. Disconnect from server
        if (nonpersis):
            s.send("3")
            keep_alive = False
            break
    elif (command == "9"):
        # Client wants to move into a non-persistent connection
        print("Connection will close when command is executed")
        nonpersis = True
    elif (command == "3"):
		# Client wishes to disconnect from server
        s.send("3")
        data = s.recv(BUFFER_SIZE)
        print(data)
        keep_alive = False
        break
    else:
		# User may input an improper command. Tell user to rectify
        print("Please insert a command listed on the table")

print("Connection is closed")
# Close the socket connection
s.close()

# Prompt user if they wish to restart the application and reconnect
restart = raw_input("\nDo you want to restart the program? [y/n] > ")

if restart == "y":
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
else:
    print("\nThe program will be closed...")
    sys.exit(0)