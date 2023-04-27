import options # import du fichier options.py
import filelist #import du fichier filelist.py
import server #import du fichier server.py
import generator #import du fichier generator.py
import client #import du fichier client.py
import sender
import os
class File:
    def __init__(self):
        self.header = None
        self.name = None
        self.size = None
        self.hashes = [] # list of hash for rolling checksum
        self.globalHash = None # global hash for file
        self.data = None
        self.type = None
        self.indexes_to_send = []


class Sync :
    def __init__(self):
        self.args = None
        self.src = None
        self.dest = None
        self.src_files = []
        self.dest_files = []
        self.mode = "LOCAL"  # LOCAL or REMOTE
        self.push_or_pull = None # PUSH or PULL
        self.ip = None
        self.remoteUser = None
    def setArgs(self, args):
        self.args = args
    def setSrc(self, srcs):
        self.src = srcs
    def setDest(self, dest):
        self.dest = dest

def checkModeAndPushOrPull(sync):
    # if src or dest contains @ then it is a remote connection
    for src in sync.args.src:
        if src.find("@") != -1:
            sync.mode = "REMOTE"
            sync.push_or_pull = "PULL"
            if src.find(":") == -1:  # check if format name@ip:dir is correct
                print("Error: format name@ip:dir not good")
                exit(1)
            ip = src.split("@")[1].split(":")[0]
            sync.args.src.remove(src)
            src = src.split("@")[1].split(":")[1]
            sync.args.src.append(src)
            remoteUser = src.split("@")[0]
            if sync.args.src == "":
                sync.args.src = "."
            else:
                sync.args.src = sync.args.src.split("@")[1].split(":")[1]
            return 0
        else:
            sync.mode = "LOCAL"
            sync.push_or_pull = "PUSH"
            return 0
    if sync.args.dest.find("@") != -1:
        sync.mode = "REMOTE"
        sync.push_or_pull = "PUSH"
        if sync.args.dest.find(":") == -1:  # check if format name@ip:dir is correct
            print("Error: format name@ip:dir not good")
            exit(1)
        remoteUser = sync.args.dest.split("@")[0]
        ip = sync.args.dest.split("@")[1].split(":")[0]
        if sync.args.dest == "": #if only : is given as dest then it is the current directory
            sync.args.dest = "."
        else:
            sync.args.dest = sync.args.dest.split("@")[1].split(":")[1]
    sync.remoteUser = remoteUser
    sync.ip = ip

if __name__ == '__main__':
    sync = Sync()
    sync.setArgs(options.getArgs())
    checkModeAndPushOrPull(sync)
    sync.setSrc(filelist.getSrcs(sync))
    sync.setDest(sync.args.dest)
    if sync.args.list_only:
        filelist.printSrcs(sync.src)
        exit(0)
    if sync.args.verbose:
        print("Source(s) : ", sync.src)
        print("Destination : ", sync.dest)
        #printLog(sync) function to print log while executing the copy
    if sync.args.server:
        server.createServer(sync)
        sync.push_or_pull = "PULL"
        sender.sendFileList(sync, )
    else:
        generator.generateFiles(sync, sync.src, sync.src_files)
        server.createServer(sync)