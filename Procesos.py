import funcionHash
import AperturaBaseDatos
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

file = open("./config.txt", "r")
config = []
for line in file: 
    line = line.strip() 
    words = line.split("=")     
    config.append(words[1])
tiempo = config[0]
path = config[1]
file.close()


suma = 0
suma1 = 0
val = []
def apertura():
    ficheros = os.listdir(path) 
    for fichero in ficheros:
        if os.path.isfile(os.path.join(path, fichero)):
            if config[2] == "md5":
                t = funcionHash.getmd5file(path + fichero)
            elif config[2] == "sha1":
                t = funcionHash.getsha1file(path + fichero)
            else:
                t = funcionHash.getsha256file(path + fichero)
            val.append((fichero,t)) 

    return val
val = apertura()
for i in val:           
    AperturaBaseDatos.cursor.execute("INSERT INTO tablacliente1(Nombre,NumeroHash) VALUES (%s, %s)",(i[0], i[1]))
    AperturaBaseDatos.connection.commit()

cont = 0
while(True):    

    ficheros = os.listdir(path)              
    user_input1 = input("¿Qué fichero quieres comprobar? Introduce el codigo de validacion del archivo: ")
    comprobacion(user_input1)

    val = apertura()

    for i in val:  
        sql1 = "UPDATE tablacliente1 SET NumeroHash ='"+ i[1] + "' WHERE Nombre ='"+ str(i[0]) + "'"
        AperturaBaseDatos.cursor.execute(sql1)
        AperturaBaseDatos.connection.commit()  
        
    val3 = "SELECT * FROM tablacliente1"
    val3 = run_query(val3)

    for t in val3:
        if(str(user_input1) == str(t[2])):
            val1 = "SELECT NumeroHash FROM tablacliente1 WHERE SumaHashNumero='" + str(user_input1) + "'"
            val1 = run_query(val1)
            
            val2 = "SELECT * FROM tablaservidor WHERE Nombre='" + str(t[0]) + "'"
            val2 = run_query(val2)
            
            if(comprobacion(user_input1)):
                suma = str(t[2]) + str(val2[0][1]) #Servidor
                suma1 = str(user_input1) + str(val1[0][0]) #Cliente
                if(suma1 == suma):
                    print("Acceso correcto al documento especificado")
                else:
                    print("No tienes acceso al documento especificado")
                    for i in val2:                           
                        AperturaBaseDatos.cursor.execute("UPDATE tablacliente1 SET NumeroHash ='"+ i[1] + "' WHERE Nombre ='"+ str(i[0]) + "'")
                        AperturaBaseDatos.connection.commit() 