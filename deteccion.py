import FuncionHash
import time
import os
import AperturaBaseDatos
from datetime import datetime

 
def run_query(query=''): 
   
    cursor = AperturaBaseDatos.connection.cursor()
    cursor.execute(query)          # Ejecutar una consulta 
    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else:               # Hacer efectiva la escritura de datos 
        data = None
    return data

file = open("./registro.txt", "w")
file.close()

sql = "INSERT INTO segundatabla(Nombre,NumeroHash) VALUES (%s, %s)"
def clave_ordenacion(tupla):
  return (str(tupla[1]), tupla[0])

datos = [ (3, 1), (2, 3), (3, 2), (1, 2), (4, 1), (4,2), (3,3)]
def apertura():
    path = "C:/Users/Ismael/Desktop/ficheros"
    ficheros = os.listdir(path) 
    val = []
    for fichero in ficheros:
        if os.path.isfile(os.path.join(path, fichero)):
            t = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/ficheros/" + fichero)
            val.append((fichero,t))
            sorted(val, key=clave_ordenacion)
            val.sort(reverse=True)
    return val

AperturaBaseDatos.cursor.executemany(sql, apertura())
AperturaBaseDatos.connection.commit()

while(True):
    c = 0
    val1 = "SELECT Nombre, NumeroHash FROM segundatabla" #se saca la lista del sql
    val1 = run_query(val1)
    while(c<30):
        
        
        archivo = "./log/" + str(datetime.now().strftime('%Y_%m'))
        
        file = open(archivo + ".txt", "a")
        
        tf = False
        cambios=[]
        print(val1)
        print(apertura())
        for x,y in zip(apertura(),val1):
            if x != y:
                tf = True
                cambios.append(x[0])
                m = "UPDATE segundatabla SET NumeroHash ='"+ str(val1[0][1]) + "' WHERE Nombre ='"+ str(val1[0][0]) + "'"                    
                AperturaBaseDatos.cursor.execute(m)
                AperturaBaseDatos.connection.commit()
        
        if (tf):
            print("Se ha modificado el hash de un archivo")
            file.write("Día " + str(datetime.now().strftime('%d')) + " a las " + str(datetime.now().strftime('%H:%M')) + ":  FALLO - El/Los archivo/s " + str(cambios) + " ha/n sido modificado/s" + os.linesep)
        else:
            print("No se ha modificado el hash de ningún archivo")
            file.write("Día " + str(datetime.now().strftime('%d')) + " a las " + str(datetime.now().strftime('%H:%M')) + ":  ACIERTO - El arhivo no ha sido alterado" + os.linesep)        
        file.close()
        c=c+1
        
        time.sleep(10) 
        despues = "./log/" + str(datetime.now().strftime('%Y_%m'))
        if despues != archivo:
            file = open(archivo + ".txt", "r")
            cont = 0
            print(despues)
            print(archivo)
            for line in file: 
                line = line.strip() 
                words = line.split(" ")     
                for word in words: 
                    if word == 'FALLO':
                        cont = cont + 1
            file = open(archivo + ".txt", "a")
            file.write(os.linesep + "Han ocurrido un total de " + str(cont) + " fallos")
            file.close()

