import os
import pickle

def sendFileList(sync, list_file=None):
    if sync.args.verbose:
        print("Sending file list...")
    if list_file is None:
        list_file = sync.src_files
    data = pickle.dumps(list_file)
    size = len(data)
    size = "size:" + str(size) +";"
    fd_write = os.open("/tmp/mkfifo", os.O_WRONLY)
    if sync.mode == "REMOTE":
        os.dup2() #pas fini
    os.write(fd_write, size.encode())
    os.write(fd_write, data)
    os.close(fd_write)