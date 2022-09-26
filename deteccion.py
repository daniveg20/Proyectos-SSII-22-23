import FuncionHash
import time
import os
import AperturaBaseDatos

sql = "INSERT INTO segundatabla(Nombre,NumeroHash) VALUES (%s, %s)"
#sql1 = "INSERT INTO segundatabla(Nombre,NumeroHash, ID) VALUES (%s, %s, %s)"
p = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/horario_provisional.png")
v = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/new.csv")

lista = []
val =[
        ("horario_provisional",p),
        ("new",v)
    ]
AperturaBaseDatos.cursor.executemany(sql,val)
AperturaBaseDatos.connection.commit()
 
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

while(True):
    time.sleep(1800) 
    val1 = "SELECT * FROM segundatabla" #se saca la lista del sql
    val1 = run_query(val1)
    v = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/new.csv")
    p = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/horario_provisional.png")
    val =[
        ("new",v),
        ("horario_provisional",p)
    ]
    
    if (val != val1):
        print("Se ha modificado el hash de un archivo")
        file = open("./registro.txt", "a")
        file.write("Un archivo ha sido alterado" + os.linesep)
        file.close()
    else:
        print("No se ha modificado el hash de ningún archivo")
        file = open("./registro.txt", "a")
        file.write("Ningún archivo ha sido alterado" + os.linesep)
        file.close()

