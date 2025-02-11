import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '123454321',
    auth_plugin = 'mysql_native_password',
)


cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE sebastian")

print("All Done!")