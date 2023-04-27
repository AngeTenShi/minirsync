import hashlib

def getBlockByIndex(file, index):
    return file.data[index*1024:(index+1)*1024]

def compare_hash(file1, file2):
    if file1.globalHash == file2.globalHash:
        return True

def generateGlobalHash(file):
    if file.type == "dir":
        hash = hashlib.md5(b"folder").hexdigest()
    else:
        hash = hashlib.md5(file.data).hexdigest()
    return hash

def generateHash(file):
    if file.type == "dir":
        hash = [hashlib.md5(b"folder").hexdigest()]
    else:
        # generate list of hash for a data
        if len(file.data) < 1024:
            iteration = 1
        else:
            iteration = len(file.data) // 1024
            if len(file.data) % 1024 != 0:
                iteration += 1
        hash = []
        for i in range(iteration):
            hash.append(hashlib.md5(file.data[i*1024:(i+1)*1024]).hexdigest())
    return hash