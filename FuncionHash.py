import hashlib

#Función Hash MD5
def getmd5file(fichero):
    fp = open(fichero, "rb")
    buffer = fp.read()
    # md5
    hashObj = hashlib.md5()
    hashObj.update(buffer)
    lastHash = hashObj.hexdigest()
    md5 = lastHash
    fp.close()
    return md5 

#Función Hash SHA-1
def getsha1file(fichero):
    fp = open(fichero, "rb")
    buffer = fp.read()
    # sha1
    hashObj = hashlib.sha1()
    hashObj.update(buffer)
    lastHash = hashObj.hexdigest()
    sha1 = lastHash
    fp.close()
    return sha1

#Función Hash SHA-256
def getsha256file(fichero):
    fp = open(fichero, "rb")
    buffer = fp.read()
    # sha256
    hashObj = hashlib.sha256()
    hashObj.update(buffer)
    lastHash = hashObj.hexdigest()
    sha256 = lastHash
    fp.close()
    return sha256 




