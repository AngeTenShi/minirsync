import os
import sys
import options # import du fichier options.py
import filelist #import du fichier filelist.py

class Sync :
    def __init__(self):
        self.args = None
        self.src = None
        self.dest = None

    def setArgs(self, args):
        self.args = args
    def setSrc(self, srcs):
        self.src = srcs
    def setDest(self, dest):
        self.dest = dest

if __name__ == '__main__':
    sync = Sync()
    sync.setArgs(options.getArgs())
    sync.setSrc(filelist.getSrcs(sync))
    sync.setDest(sync.args.dest)
    if sync.args.list_only:
        filelist.printSrcs(sync.src)