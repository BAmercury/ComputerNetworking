#!/usr/bin/env python
# using Python 2.7

from socket import *
import threading
from SocketServer import ThreadingMixIn
# Server Host IP address and port information
BUFFER_SIZE = 1024 # TCP message buffer size
TCP_IP = '192.168.1.126'
TCP_PORT = 5005


# Create TCP socket objects, see report for furthur detail
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)


# Boolean to keep server running
keep_alive = True


# Function to check if given string is a palindrome
def isPalindrome(data):
    if len(data) < 2:
        #If the string has 0 or 1 characters, the string conforms to the palindrome definition
        return True
    if data[0] != data[-1]:
        #If the string has more than one character, check that the first and last item of the string are equivalent
        return False
    return isPalindrome(data[1:-1])
    #The first and last items of the string are equivalent, so remove the first and last items of the string and continue checking


# Load a file from local directory, returns a python list object
def file_to_list(ip):
    items = []
    filename = ip + ".txt"
    try:
        with open(filename, 'rb') as fp:
            items = fp.read().splitlines()
    except Exception:
        with open(filename, 'wb') as fp:
            fp.write("")
    return items

# Save python list to a file. File name is the IP of the client connecting to it
def list_to_file(ip, itemlist):
    filename = ip + ".txt"
    with open(filename, 'w') as fp:
        for items in itemlist:
            fp.write(items + "\n")
        
    
    


# Client callback function
class ClientCallBack(threading.Thread):

    def __init__(self,ip,port):
		# Initialize the instance as a Python Thread object, allow thread to have access to IP and port information
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
    def run(self):
		# Recall found palindromes from file .txt database. Use IP address to find the corresponding user data
        found_palindromes = file_to_list(self.ip)
        while True:
			# Recieve and format command packet as a python list
            data = conn.recv(BUFFER_SIZE)
            data_list = data.split(",")
			# Parse the command index of command packet
            if (data_list[0] == "1"):
                result = isPalindrome(data_list[1])
                if (result == True):
                    conn.send("Your word is a palindrome")
                    found_palindromes.append(data_list[1])
                else:
                    conn.send("Your word is not a palindrome")
            elif (data_list[0] == "2"):
                data_list.remove("2") # remove the command out of the list, leave only the words
                results = []
                for word in data_list:
                    result = str(isPalindrome(word))
                    results.append(result)
                    if (result == "True"):
                        found_palindromes.append(word)
                results_string = ",".join(results)
                conn.send(results_string)
            elif (data_list[0] == "4"):
                # Send back the amount of palindromes found
                payload = "Amount of palindromes found: " + str(len(found_palindromes))
                conn.send(payload)
            elif (data_list[0] == "5"):
                # Send back a list of palindromes found

                # First check to see if list is not empty
                if (len(found_palindromes) > 0):
                    payload = ",".join(found_palindromes) # Convert python list to a string
                    conn.send(payload) # Send the payload string
                else:
                    conn.send("No palindromes in list") # Tell client no palindromes are in list
            elif (data_list[0] == "6"):
                # Return the latest palindrome
                
                # First check to see if list is not empty
                if (len(found_palindromes) > 0):
                    latest = found_palindromes[-1] # read out the word in the end index
                    payload = "Latest palindrome: " + latest # Assemble string payload
                    conn.send(payload) # send payload
                else:
                    conn.send("No palindromes in the list")
            elif (data_list[0] == "7"):
                # Client wants to delete all palindromes found
                found_palindromes = [] # Clear the list of found palindromes
                conn.send("Cleared the palindrome found list")
            elif (data_list[0] == "8"):
                # Client wants to remove palindromes at specfic positions
                data_list.remove("8") # remove the command from the list. Leave only the positions
                # Convert list of strings to list of int:
                positions = map(int, data_list)
                for index in sorted(positions, reverse=True): # Delete in reverse order so subsequent indexes aren't thrown off
                    try:
                        del found_palindromes[index]
                    # Will throw exception if the index is out of range
                    except Exception:
                        pass
                # Return the updated list to the client

                # First check to see if list is not empty
                if (len(found_palindromes) > 0):
                    payload = ",".join(found_palindromes) # Convert python list to a string
                    conn.send(payload) # Send the payload string
                else:
                    conn.send("No palindromes in list") # Tell client no palindromes are in list
            elif (data_list[0] == "3"):
				# Save python list user data to file and close the connection
                list_to_file(self.ip, found_palindromes)
                conn.send("Bye")
                break
            
        conn.close()

if __name__ == '__main__':
    try:
        while keep_alive:
			# List for new connections
            server_socket.listen(4)
            print("Waiting for clients to connect...")
			# Accept the new connection
            (conn, (ip,address)) = server_socket.accept()
            print("Client connected. Address: ", address)
			# Spin and start a new thread, give thread object the IP and address
            newThread = ClientCallBack(ip,address)
            newThread.start()
		# Close the server down
        server_socket.close()
    except KeyboardInterrupt:
		# Close all running threads
        for t in threads:
            t.join()
        server_socket.close()
        pass



