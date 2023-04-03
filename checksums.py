import hashlib
def compare_hash(file1, file2):
    if file1.hash == file2.hash:
        return True

def generateHash(file):
    hash = hashlib.md5(file.data).hexdigest()
    return hash