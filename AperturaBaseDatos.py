from mysql.connector import Error
import mysql.connector

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