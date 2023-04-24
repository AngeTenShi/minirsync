import os
import pickle
import time
def getFiles(sync):
    pid = os.fork()
    if pid == 0:
        fd_read = os.open("/tmp/mkfifo", os.O_RDONLY)
        byte = os.read(fd_read, 1)
        size = b"s"
        while byte:
            while byte != b';':
                byte = os.read(fd_read, 1)
                size += byte
            if size[0:5] != b'size:':
                print("Error: format size not good")
                exit(1)
            size = int(size[5:-1])
            offset = 0
            buffer = b""
            while size > 0:
                byte = os.read(fd_read, 1)
                size -= 1
                buffer += byte
            file = pickle.loads(buffer)
            filename = file.name
            if file.type == "dir":
                os.makedirs(os.path.join(sync.dest, filename), exist_ok=True)
            else:
                fd = os.open(os.path.join(sync.dest, filename), os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
                os.write(fd, file.data)
                os.close(fd)
            byte = os.read(fd_read, 1)
            size = b"s"
        os.close(fd_read)
    else:
        os.wait()

def sendFiles(sync, list_file):
    if sync.args.verbose:
        print("Sending files...")
    if list_file == []:
        if sync.args.verbose:
            print("No files to send")
        return
    pid = os.fork()
    if pid == 0:
        fd_write = os.open("/tmp/mkfifo", os.O_WRONLY)
        for file in list_file:
            data = pickle.dumps(file)
            size_t = len(data)
            size = "size:" + str(size_t) +";"
            os.write(fd_write, size.encode())
            os.write(fd_write, data)
        os.close(fd_write)
    else:
        if sync.mode == "LOCAL":
            getFiles(sync)
