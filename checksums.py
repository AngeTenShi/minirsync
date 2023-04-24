import hashlib
def compare_hash(file1, file2):
    if file1.hash == file2.hash:
        return True

def generateHash(file):
    if file.type == "dir":
        hash = hashlib.md5(b"").hexdigest()
    else:
        hash = hashlib.md5(file.data).hexdigest()
    return hash