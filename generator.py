import os
import mrsync
import checksums
import client
import server
import receiver
import sender
import filelist as fl
def compareFileLists(sync):
    if sync.push_or_pull== "PULL":
        list_file = []
        filelist = receiver.receiveListofFile(sync)
        for src_files in sync.src_files:
            for dst_files in filelist:
                if src_files.name == dst_files.name:
                    if src_files.hash == dst_files.hash:
                        if sync.args.verbose:
                            print("File already exists, skipping...")
                    else:
                        if sync.args.verbose:
                            print("File has been modified, sending...")
                        list_file.append(src_files)
        #envoyer nouvelle filelist a recevoir
        if sync.args.verbose:
            print("Comparing file lists...")
        sender.sendFileList(sync, list_file)
        client.getFiles(sync)
    if sync.push_or_pull == "PUSH":
        if sync.args.verbose:
            print("Comparing file lists...")
        if sync.mode == "REMOTE":
            list_file = receiver.receiveListofFile(sync)
        else:
            list_file = []
            generateFiles(sync, fl.getDest(sync), sync.dest_files)
            if sync.dest_files == []:
                list_file = sync.src_files
                client.sendFiles(sync, list_file)
                return
            for src_files in sync.src_files:
                found = 0
                for dst_files in sync.dest_files:
                    # print("src : ", src_files.name)
                    # print("dst : ", dst_files.name)
                    if os.path.basename(src_files.name) == os.path.basename(dst_files.name):
                        found = 1
                        if src_files.hash == dst_files.hash:
                            if sync.args.verbose:
                                print("File already exists, skipping...")
                        else:
                            if sync.args.verbose:
                                print("File has been modified, sending...")
                            list_file.append(src_files)
                if found == 0:
                    list_file.append(src_files)
        client.sendFiles(sync, list_file)

def generateFiles(sync, filelist, filelist2):
    for src in filelist:
        if sync.args.verbose:
            print("Generating files...")
        file = mrsync.File()
        file.size = os.stat(src).st_size
        if src.startswith('./'):  # on enleve le ./ si les srcs sont dans le dossier courant
            src = src[2:]
        file.name = src
        if os.path.isdir(file.name):
            file.type = "dir"
        else:
            file.type = "file"
        generateData(sync, file)
        file.hash = checksums.generateHash(file)
        file.header = f"Filename:{file.name},size:{file.size},hash:{file.hash}"
        filelist2.append(file)

def generateData(sync, file):
    if sync.args.verbose:
        print("Generating data...")
    if file.type == "dir":
        file.data = ""
    else:
        file.data = open(file.name, 'rb').read()

