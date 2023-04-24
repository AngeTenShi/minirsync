import os
import client
import pickle
import receiver
import sender
import generator


def createServer(sync):
    if sync.args.verbose:
        print("Creating server...")
    if not os.path.exists("/tmp/mkfifo"):
        os.mkfifo("/tmp/mkfifo")        # Créer un pipe
    generator.compareFileLists(sync)
    try:
        os.unlink("/tmp/mkfifo")
    except OSError:
        pass
