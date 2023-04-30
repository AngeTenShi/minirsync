import os
import mrsync
import checksums
import client
import server
import receiver
import sender
import filelist as fl

def remove_first_level(path):
    # séparer le chemin en segments
    segments = path.split('/')

    # retirer le premier segment s'il est vide
    if segments[0] == '':
        segments = segments[1:]

    # retirer le deuxième segment s'il existe
    if len(segments) > 1:
        segments = segments[1:]

    # recombiner les segments en un nouveau chemin
    new_path = '/'.join(segments)

    return new_path

def compareIt(sync, filelist):
    list_file = []
    for src_files in sync.src_files:
        found = 0
        for dst_files in sync.dest_files:
            if os.path.basename(src_files.name) == os.path.basename(dst_files.name):
                found = 1
                if src_files.globalHash == dst_files.globalHash:  # use global hash to check if file compare and then use list of hash to check what to send
                    if sync.args.verbose:
                        print("File already exists, skipping...")
                else:
                    print(dst_files.name)
                    i = 0
                    while i < len(src_files.hashes) and i < len(dst_files.hashes):
                        if src_files.hashes[i] != dst_files.hashes[i]:
                            src_files.indexes_to_send.append(i)
                            if sync.args.verbose:
                                print("File has been modified, sending...")
                        i += 1
                    if i < len(src_files.hashes):
                        for j in range(i, len(src_files.hashes)):
                            src_files.indexes_to_send.append(j)
                            if sync.args.verbose:
                                print("File has been modified, sending...")
                    list_file.append(src_files)
        if found == 0:
            # if folder append index 0 else append all indexes
            if src_files.type == "dir":
                src_files.indexes_to_send.append(0)
            else:
                for i in range(len(src_files.hashes)):
                    src_files.indexes_to_send.append(i)
            if sync.args.verbose:
                print("File does not exist, sending...")
            list_file.append(src_files)
    return list_file
def compareFileLists(sync):
    if sync.push_or_pull== "PULL": #working in theory but not in practice because no remote
        list_file = []
        filelist = receiver.receiveListofFile(sync)
        for src_files in sync.src_files:
            for dst_files in filelist:
                if src_files.name == dst_files.name:
                    if src_files.globalHash == dst_files.globalHash:
                        if sync.args.verbose:
                            print("File already exists, skipping...")
                    else:
                        if sync.args.verbose:
                            print("File has been modified, sending...")
                        list_file.append(src_files)
        sender.sendFileList(sync, list_file)
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
            generateFiles(sync, fl.getDest(sync), sync.dest_files)
            list_file = sync.dest_files
        list_file = compareIt(sync, list_file)
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
        # final name = name without src example : ../TP/test.txt -> TP/test.txt /test/test2.txt -> test/test2.txt
        file.finalName = remove_first_level(src)
        if os.path.isdir(file.name):
            file.type = "dir"
        else:
            file.type = "file"
        generateData(sync, file)
        file.globalHash = checksums.generateGlobalHash(file)
        file.hashes = checksums.generateHash(file)
        file.header = f"Filename:{file.finalName},size:{file.size},hash:{file.globalHash}"
        filelist2.append(file)

def generateData(sync, file):
    if sync.args.verbose:
        print("Generating data...")
    if file.type == "dir":
        file.data = b"folder"
    else:
        file.data = open(file.name, 'rb').read()

