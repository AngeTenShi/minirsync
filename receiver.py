import socket
import time
import os
import pickle
def receiveListofFile(sync):
    fd_read = os.open("/tmp/mkfifo", os.O_RDONLY)
    s = b""
    byte = os.read(fd_read, 1)
    size = b"s"
    listOfFiles = []
    while byte.decode() != ';':
        byte = os.read(fd_read, 1)
        size += byte
    if size[0:5] != b'size:':
        print("Error: format size not good")
        exit(1)
    size = int(size[5:-1])
    while size > 0:
        byte = os.read(fd_read, 1)
        s += byte
        size -= 1
    listOfFiles = pickle.loads(s)
    os.close(fd_read)
    return listOfFiles #return a list of files

"""
def receiveListOfFiles():
    #receive the list of files by a socket
    #put it in a list
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5000))
    server.listen(5)
    client, address = server.accept()
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        print("From connected user: " + str(data))
        #check if final data is a list of files
        #if not, send an error message

        data = str(data).upper()

        print("sending: " + str(data))
        client.send(data.encode())
    client.close()
"""