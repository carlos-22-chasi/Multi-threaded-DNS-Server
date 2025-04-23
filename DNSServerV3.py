# Spring 2024 CSCI 4211: Introduction to Computer Networks
# DNSServerV3.py
# This program serves as the server of the DNS query.
# Written in Python v3.
#Carlos Chasi-Mejia (chasi009)

import sys, threading, os, random
from socket import *

import time
import argparse
# The following two modules may be useful to implement the extra credit.
import subprocess
import re

class Server:
    def __init__(self, serverHost = "localhost", serverPort = 5001):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.DNS_FILE = "dns_mapping.txt"
        self.LOG_FILE = "dns-server-log.csv"
        self.dictionary = {}

        # TODO: Check if the DNS file already exists. Create it if it does 
        # not.

        #check if file exists 
        if(os.path.isfile(self.DNS_FILE)):
            # TODO: Open and read the entire DNS file and save the cache 
            # information to a data structure that the server will use as its 
            # local cache during the time it's running.
            fp = open(self.DNS_FILE, 'r')
            lines = fp.readlines() #read every line of the file
            for line in lines:
                items = line.split(",")    #seperate the line content by commas
                hostname = items[0]
                ip_address = items[1]
                ip_address = ip_address.replace("\n", "")
                self.dictionary[hostname] = ip_address #add the line contenet to the dictionary 
            fp.close()

        #file doesn't exist so create it 
        else:
            fp = open(self.DNS_FILE, "w")
            fp.close()

    def run(self):
        # TODO: Create a socket object named serverSocket, SOCK_STREAM for 
        # TCP.
        try:
            serverSocket = socket(AF_INET, SOCK_STREAM)
        # Handle exception
        except error as message:
            serverSocket = None 
        # If the socket cannot be opened, then quit the program.
        if serverSocket is None:
            print("Error: cannot open socket")
            sys.exit(1)

	    # TODO: Bind the socket to the current address on port 5001.
        serverSocket.bind((self.serverHost, self.serverPort))

	    # TODO: Listen on the given socket while the allowed maximum number
        # of connections to be queued is 20.
        serverSocket.listen(20)

        # Create and start the save thread.
        save = threading.Thread(target = self.saveFile, args = [])
        save.start()
        # Create and start the monitor thread.
        monitor = threading.Thread(target = self.monitorQuit, args = [])
        monitor.start()
        
        print("Server is listening...")

        while 1:
            # Blocked until a remote machine connects to the local port.
            connectionSocket, addr = serverSocket.accept()
            server = threading.Thread(target = self.dnsQuery, args = [connectionSocket])
            server.start()
    
    def dnsQuery(self, connectionSocket):		
        # TODO: Read the client's query from the connection socket.
        query_hostname = connectionSocket.recv(1024).decode()
        # print("hostname: ", query_hostname)

	    # TODO: Check the local cache data structure to see if the queried 
        # hostname already has an entry in it. If there is a match, then 
        # directly use the entry in the cache.
        ip_address = self.dictionary.get(query_hostname)
        resolution_method = "CACHE"  

	    # TODO: If there's no match, then query the local machine's DNS 
        # API to get the hostname resolution.
        # TODO: Save the newly resolved hostname and its corresponding
            # IP address(es) in the local cache data structure.
        try:
            if ip_address == None:
                ip_address = gethostbyname(query_hostname)
                self.dictionary[query_hostname] = ip_address #save ip address to the cache
                resolution_method = "API" #if ip_adress not in cache, set resolution method to API
        except gaierror: #ip_address doesnt exist 
            ip_address = "Host Not Found"
            resolution_method = "API"   #if ip_adress not in cache, set resolution method to API

        # NOTE: If you're implementing the extra credit, then you will need 
        # to call ipSelection() at least once in this function to have an IP 
        # address properly selected. If you're not doing the extra credit,
        # then do NOT call ipSelection() at all and you can simply delete 
        # this note.
        
	    # TODO: Print the response to the terminal.
        response = "{}:{}:{}".format(query_hostname, ip_address, resolution_method)
        print(response)

	    # TODO: Send the encoded response back to the client.
        connectionSocket.send(response.encode()) 

	    # TODO: Close the connection socket.
        connectionSocket.close()

	    # TODO: Append a new entry for this query to the log file.
        fp = open(self.LOG_FILE, 'a')
        fp.write("{},{},{}\n".format(query_hostname, ip_address, resolution_method)) #append content to log file 
        fp.close()

        return


    # NOTE: This function should only be implemented if you're intending to
    # complete the extra credit part. It does NOT need to be implemented for
    # the required parts of the project.
    def ipSelection(self, ipList):
        # TODO: Check the number of IP addresses in the passed IP address
        # list. If there is only one IP address in the list, then immediately 
        # return that IP address.

        # TODO: Otherwise, if there are multiple IP addresses in the list, 
        # then return the IP address in the list that has the best performance 
        # (i.e., lowest latency) by using Ping.

        return
        
    
    def saveFile(self):
        while 1:
            # TODO: Check for updates that have been made to the local cache 
            # data structure and save all of the updates to the DNS file to 
            # keep it up-to-date.  
            fp = open(self.DNS_FILE, 'w+') 
            for hostname, ip_address in self.dictionary.items():
                fp.write("{},{}\n".format(hostname, ip_address)) #write dictionary items to DNS file
            fp.close()

            # This thread goes to sleep for 15 seconds.
            time.sleep(15)
            
    def monitorQuit(self):
        while 1:
            # Get input from the user.
            sentence = input()
            if (sentence == "exit"):
                # TODO: Write all new values from the local cache data 
                # structure to the DNS file before the server process is 
                # killed so that the most current version of the cache is 
                # persistently stored in a file.
                fp = open(self.DNS_FILE, 'w+')
                for hostname, ip_address in self.dictionary.items():
                    fp.write("{},{}\n".format(hostname, ip_address))
                fp.close()

                os.kill(os.getpid(), 9)

# The following code will be executed immediately and will allow your server
# code to run after entering 'python3 DNSServerV3.py' into the terminal.
if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description = 'Get Port.')
    parser.add_argument("-p","--port", type = int, default = 5001,
                    help = "port number")
    args = parser.parse_args()
    print("port = ", args.port)
    server = Server(serverPort = args.port)
    server.run()