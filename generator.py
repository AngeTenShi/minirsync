import os
import mrsync
import checksums
def generator(sync):
    pid = os.pipe()
    if pid == 0:
        pass
def generateFiles(sync):
    for src in sync.src:
        if sync.args.verbose:
            print("Generating files...")
        file = mrsync.File()
        file.size = os.stat(src).st_size
        if src.startswith('./'):  # on enleve le ./ si les srcs sont dans le dossier courant
            src = src[2:]
        file.name = src
        file.header = f"Filename:{file.name},size:{file.size},"
        generateData(sync, file)
        file.hash = checksums.generateHash(file)
        sync.files.append(file)
def generateData(sync, file):
    if sync.args.verbose:
        print("Generating data...")
    file.data = open(file.name, 'rb').read()