import mysql.connector
from mysql.connector import Error

class Users:
    def create_server_connection(host_name, user_name, user_password):
        connection = None
        
        try:
            connection = mysql.connector.connect(
                host = host_name,
                user = user_name,
                password = user_password
            )
            print("Mysql database connection successful")

        except Error as err:
            print(err)

        return connection


    


    connection = create_server_connection('localhost','bella','admin123')
