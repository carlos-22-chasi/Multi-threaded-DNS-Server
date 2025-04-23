Make sure the Python file (DNSServerV3.py) is in your working directory.

Open a terminal and navigate to the directory where the file is located.

Run the server using the command:

```
py -3 DNSServerV3.py
```
If successful, the terminal will display:

```
Server is listening...
```

Description of the Server
The DNS server performs the following tasks:

Initialization:

Sets up the server host and port.

Checks if a DNS mapping file exists. If not, it creates one.

Reads the DNS file and loads existing DNS records into a local cache (a dictionary).

Server Setup:

Creates a server socket bound to the specified host and port.

Starts listening for incoming client connections.

Thread Management:

Cache Save Thread: Periodically (every 15 seconds) checks for changes in the local cache and writes all current records back to the DNS file.

Quit Monitor Thread: Waits for user input in the terminal. If the input is "exit", it writes the final cache data to the file and shuts down the server.

Handling Client Connections:

When a client connects, the server accepts the connection and spawns a new thread to handle the query.

The server receives the client’s DNS query using recv().

It checks the local cache:

If the domain is found, the IP is returned from the cache and the resolution method is "CACHE".

If not, it uses socket.gethostbyname() to query the system's DNS and returns the result with the method "API".

The server logs the resolution method and response to the terminal.

Sends the IP address back to the client using send(), closes the connection socket, and logs the query to a log file.

The thread continues handling new client queries until the server is manually stopped.

