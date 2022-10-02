import funcionHash
import time
import os
import AperturaBaseDatos
from datetime import datetime

file = open("./config.txt", "r")
config = []
for line in file: 
    line = line.strip() 
    words = line.split("=")     
    config.append(words[1])
tiempo = config[0]
directorio = config[1]
file.close()


def run_query(query=''): 
   
    cursor = AperturaBaseDatos.connection.cursor()
    cursor.execute(query)          # Ejecutar una consulta 
    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else:               # Hacer efectiva la escritura de datos 
        data = None
    return data

def clave_ordenacion(tupla):
  return (str(tupla[1]), tupla[0])

def apertura():
    ficheros = os.listdir(directorio) 
    val = []
    for fichero in ficheros:
        if os.path.isfile(os.path.join(directorio, fichero)):
            if config[2] == "md5":
                t = funcionHash.getmd5file(directorio + fichero)
            elif config[2] == "sha1":
                t = funcionHash.getsha1file(directorio + fichero)
            else:
                t = funcionHash.getsha256file(directorio + fichero)
            val.append((fichero,t))
            sorted(val, key=clave_ordenacion)
            if(funcionHash.getmd5file):
                val.sort(reverse=False)
            if(funcionHash.getsha1file):
                val.sort(reverse=True)
            if(funcionHash.getsha256file):
                val.sort(reverse=False)
    return val

sql = "INSERT INTO tablaservidor(Nombre,NumeroHash) VALUES (%s, %s)"
AperturaBaseDatos.cursor.executemany(sql, apertura())
AperturaBaseDatos.connection.commit()

sql1 = "INSERT INTO tablacliente2(Nombre,NumeroHash) VALUES (%s, %s)"
AperturaBaseDatos.cursor.executemany(sql1, apertura())
AperturaBaseDatos.connection.commit()

while(True):
    c = 0
    val5 = apertura()
    for i in val5:
        sql1 = "UPDATE tablaservidor SET NumeroHash ='"+ i[1] + "' WHERE Nombre ='"+ str(i[0]) + "'"
        AperturaBaseDatos.cursor.execute(sql1)
        AperturaBaseDatos.connection.commit()

    val1 = "SELECT * FROM tablaservidor" #se saca la lista del sql
    val1 = run_query(val1)

    while(c<30):
        archivo = "./log/" + str(datetime.now().strftime('%Y_%m'))
        
        file = open(archivo + ".txt", "a")
        
        tf = False
        cambios=[]

        val5 = apertura()
        for i in val5:
            sql1 = "UPDATE tablacliente2 SET NumeroHash ='"+ i[1] + "' WHERE Nombre ='"+ str(i[0]) + "'"
            AperturaBaseDatos.cursor.execute(sql1)
            AperturaBaseDatos.connection.commit() 

        val2 = "SELECT * FROM tablacliente2" #se saca la lista del sql
        val2 = run_query(val2)

        for x,y in zip(val2,val1):
            if x != y:
                tf = True
                cambios.append(x[0])

            for i in val1:                           
                AperturaBaseDatos.cursor.execute("UPDATE tablacliente2 SET NumeroHash ='"+ i[1] + "' WHERE Nombre ='"+ str(i[0]) + "'")
                AperturaBaseDatos.connection.commit()

        if (tf):
            print("Se ha modificado el hash de un archivo")
            file.write("Día " + str(datetime.now().strftime('%d')) + " a las " + str(datetime.now().strftime('%H:%M')) + ":  FALLO - El/Los archivo/s " + str(cambios) + " ha/n sido modificado/s" + os.linesep)
        else:
            print("No se ha modificado el hash de ningún archivo")
            file.write("Día " + str(datetime.now().strftime('%d')) + " a las " + str(datetime.now().strftime('%H:%M')) + ":  ACIERTO - El arhivo no ha sido alterado" + os.linesep) 
        
        file.close()
        c=c+1
        
        time.sleep(int(tiempo))
         
        despues = "./log/" + str(datetime.now().strftime('%Y_%m'))
        if despues != archivo:
            file = open(archivo + ".txt", "r")
            cont = 0
            for line in file: 
                line = line.strip() 
                words = line.split(" ")     
                for word in words: 
                    if word == 'FALLO':
                        cont = cont + 1
            file = open(archivo + ".txt", "a")
            file.write(os.linesep + "Han ocurrido un total de " + str(cont) + " fallos")
            file.close()