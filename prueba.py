import FuncionHash
import os

path = "C:/Users/Ismael/Desktop/ficheros"
ficheros = os.listdir(path) 
ficheros1 = []
for fichero in ficheros:
    if os.path.isfile(os.path.join(path, fichero)):
        t = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/ficheros/" + fichero)
        ficheros1.append((fichero,t))
print(ficheros1)
