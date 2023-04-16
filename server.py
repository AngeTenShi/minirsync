import os
import sys
import client
import pickle

def createServer(sync):
    if sync.args.verbose:
        print("Creating server...")
    fd_read, fd_write = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(fd_read)
        for srcs_files in sync.src_files:
            data = pickle.dumps(srcs_files)
            size = len(data)
            size = "size:" + str(size) +";"
            os.write(fd_write, size.encode())
            os.write(fd_write, data)
        os.close(fd_write) # Fermer fd_write après avoir écrit dans le pipe
    else:
        client.createClient(sync, fd_read)
        os.close(fd_write)
