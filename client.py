import os
import pickle
import time
def connectToServer(sync, fd_read):
    pid = os.fork()
    if pid == 0:
        byte = os.read(fd_read, 1)
        size = b"s"
        while byte:
            while byte.decode() != ';':
                byte = os.read(fd_read, 1)
                size += byte
            if size[0:5] != b'size:':
                print("Error: format size not good")
                exit(1)
            size = int(size[5:-1])
            time.sleep(1)
            byte = os.read(fd_read, size)
            file = pickle.loads(byte)
            filename = file.name
            with open(os.path.join(sync.dest, filename), 'wb') as f:
                f.write(file.data)
            byte = os.read(fd_read, 1)
            size = b"s"
        os.close(fd_read)