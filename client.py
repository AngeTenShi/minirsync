import os
import pickle
import checksums
import time
def getFiles(sync):
    pid = os.fork()
    if pid == 0:
        fd_read = os.open("/tmp/mkfifo", os.O_RDONLY)
        byte = os.read(fd_read, 1)
        size = b"s"
        index = b"i"
        filename = b"n"
        while byte:
            # read the size:size; index:index; name:name;
            while byte != b';':
                byte = os.read(fd_read, 1)
                size += byte
            if size[0:5] != b'size:':
                print("Error: format size not good")
                exit(1)
            size = int(size[5:-1])
            byte = os.read(fd_read, 1)
            while byte != b';':
                byte = os.read(fd_read, 1)
                index += byte
            byte = os.read(fd_read, 1)
            if index[0:6] != b'index:':
                print("Error: format index not good")
                exit(1)
            index = int(index[6:-1])
            while byte != b';':
                byte = os.read(fd_read, 1)
                filename += byte
            if filename[0:5] != b'name:':
                print("Error: format filename not good")
                exit(1)
            filename = filename[5:-1].decode()
            buffer = b""
            while len(buffer) < size:
                buffer += os.read(fd_read, size - len(buffer))
            if sync.args.verbose:
                print("Index : " + str(index) + " Size : " + str(size) + " Filename : " + filename)
            if filename[-1] == '/':
                if not os.path.exists(os.path.join(sync.dest, filename)):
                    os.makedirs(os.path.join(sync.dest, filename))
            else:
                # replace the part of the block who was modified by the new one
                # if file exist replace else create
                if os.path.exists(os.path.join(sync.dest, filename)):
                    fd = os.open(os.path.join(sync.dest, filename), os.O_RDWR)
                    os.lseek(fd, index * 1024, 0)
                    os.write(fd, buffer)
                    os.close(fd)
                else:
                    if not os.path.exists(os.path.dirname(os.path.join(sync.dest, filename))):
                        os.makedirs(os.path.dirname(os.path.join(sync.dest, filename)))
                    fd = os.open(os.path.join(sync.dest, filename), os.O_CREAT | os.O_WRONLY)
                    os.write(fd, buffer)
                    os.close(fd)
            byte = os.read(fd_read, 1)
            size = b"s"
            index = b"i"
            filename = b"n"
        os.close(fd_read)
        exit(0)
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
            for index in file.indexes_to_send:
                data = checksums.getBlockByIndex(file, index)
                size_t = len(data)
                size = "size:" + str(size_t) +";"
                index = "index:" + str(index) +";"
                name = "name:" + file.finalName +";"
                os.write(fd_write, size.encode())
                os.write(fd_write, index.encode())
                os.write(fd_write, name.encode())
                os.write(fd_write, data)
        os.close(fd_write)
    else:
        if sync.mode == "LOCAL":
            getFiles(sync)

