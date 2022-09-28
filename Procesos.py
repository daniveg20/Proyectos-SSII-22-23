##SUMA BASE DE DATOS
from multiprocessing.resource_sharer import stop
import FuncionHash
import AperturaBaseDatos
import time
import os

def run_query(query=''):    
    cursor = AperturaBaseDatos.connection.cursor()
    cursor.execute(query)          # Ejecutar una consulta 
    if query.upper().startswith('SELECT'): 
        data = cursor.fetchall()   # Traer los resultados de un select 
    else:               # Hacer efectiva la escritura de datos 
        data = None
    return data

def comprobacion(user_input):
    try:
        if(int(user_input)):
            return True
    except ValueError:
        return False

suma = 0
suma1 = 0
val = []
path = "C:/Users/Ismael/Desktop/ficheros"
ficheros = os.listdir(path) 
for fichero in ficheros:
    if os.path.isfile(os.path.join(path, fichero)):
        t = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/ficheros/" + fichero)
        val.append((fichero,t)) 


for i in val:           
    AperturaBaseDatos.cursor.execute("INSERT INTO terceratabla(Nombre,NumeroHash) VALUES (%s, %s)",(i[0], i[1]))
    AperturaBaseDatos.connection.commit()
cont = 0
while(True):
    for i in val:   
        sql1 = "UPDATE terceratabla SET NumeroHash ='"+ i[1] + "' WHERE Nombre ='"+ i[0] + "' "
        AperturaBaseDatos.cursor.execute(sql1)
        AperturaBaseDatos.connection.commit()

    path = "C:/Users/Ismael/Desktop/ficheros"
    ficheros = os.listdir(path) 
    for fichero in ficheros:
        if os.path.isfile(os.path.join(path, fichero)):
            t = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/ficheros/" + fichero)
            val.append((fichero,t))
                  
    user_input1 = input("¿Qué fichero quieres comprobar? Introduce el codigo de validacion del archivo: ")
    comprobacion(user_input1)
    val3 = "SELECT SumaHashNumero, Nombre FROM terceratabla"
    val3 = run_query(val3)
    print(val3)
    for t in val3:
        if(str(user_input1) == str(t[0])):
            val1 = "SELECT NumeroHash FROM terceratabla WHERE SumaHashNumero='" + str(user_input1) + "'"
            val1 = run_query(val1)
            val2 = "SELECT * FROM segundatabla WHERE Nombre='" + str(t[1]) + "'"
            val2 = run_query(val2)
            if(comprobacion(user_input1)==True):
                suma = str(t[0]) + str(val2[0][1]) #Servidor
                suma1 = str(user_input1) + str(val1[0][0]) #Cliente
                if(suma1 == suma):
                    print("OK")
                else:
                    print("NO OK")
                    print(val2)
                    m = "UPDATE terceratabla SET NumeroHash ='"+ val2[0][1] + "' WHERE Nombre ='"+ str(val2[0][0]) + "'"                    
                    AperturaBaseDatos.cursor.execute(m)
                    AperturaBaseDatos.connection.commit()

                    #poner que se restaure la base de datos 3       