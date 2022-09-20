from mysql.connector import Error
import mysql.connector
import FuncionHash 
try:
    connection = mysql.connector.connect(
        host='localhost',
        port=3307,
        user='root',
        password='ismael',
        db='ssii_pruebas'
    )

    if connection.is_connected():
        print("Conexión exitosa.")
        infoServer = connection.get_server_info()
        print("Info del servidor: {}".format(infoServer))
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        row = cursor.fetchone()
        print("Conectado a la base de datos: {}".format(row))
except Error as ex:
    print("Error durante la conexión: {}".format(ex))


cursor = connection.cursor()
sql = "INSERT INTO primeratabla(IdHash,NumeroHash) VALUES (%s, %s)"
p = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/horario_provisional.png")
v = FuncionHash.getmd5file("C:/Users/Ismael/Desktop/new.csv")

val = [
    (5,p),
    (6,v)
]
cursor.executemany(sql,val)


connection.commit()