Overview

This project implements a custom DNS server in Python, designed to resolve domain names into IP addresses while supporting multi-threaded client handling, intelligent response caching, and comprehensive logging. Built for efficiency and scalability, the server mimics core DNS behaviors and is ideal for exploring how DNS works under the hood — particularly from a cybersecurity and networking standpoint.

Features

- Multi-threaded Request Handling: Efficiently manages multiple concurrent client queries using Python’s threading module.

- DNS Response Caching: Improves performance by storing previously resolved queries and serving them without redundant lookups.

- Persistent Logging: Logs every incoming query, the resolved IP, timestamp, and whether the result was served from cache.

- Timeout & Error Management: Handles unreachable domains and failed resolutions gracefully.

- Custom DNS Query Parsing: Parses and processes queries without relying on high-level libraries.


How To Run: 

Start the server using the command:

```
py -3 DNSServerV3.py
```
If successful, the terminal will display:

```
Server is listening...
```
In another terminal, run the client: 
```
py -3 DNSClientV3.py
```
then type any domain name:
```
google.com
```
Both domain name and ip address will be saved in separete files: dns-server-log.csv and dns_mapping.txt

