import hashlib

hashmd5 = hashlib.sha256()    
stexto="hola Altaruru, hoy es lunes 1 de Octubre de 2018"
hashmd5.update(stexto.encode())
print (hashmd5.hexdigest())







