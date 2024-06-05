import  mysql.connector
from dotenv import load_dotenv
import os
import pyodbc
import pandas as pd



class Connect:

    def __init__(self):

        current_dir = os.path.dirname(__file__)
        dotenv_path = os.path.join(current_dir, '.env')            
        load_dotenv(dotenv_path)

        self.server = os.getenv("SERVER")
        self.database = os.getenv("DATABASE")
        self.uid = os.getenv("UID")
        self.pwd = os.getenv("PWD")
        self.port = os.getenv("PORT")
        self.table = os.getenv("TABLE")

     

    def connect_to_sql_server(self, server, database, username, password):
        try:
            connection_string = (
                'DRIVER={SQL Server};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}'
            )
            connection = pyodbc.connect(connection_string)
            print("Connected to SQL Server")
            return connection
        except pyodbc.Error as e:
            print("Error while connecting to SQL Server", e)
            return None

    def insert_data(connection, table, data):
        try:
            cursor = connection.cursor()
            # Construct the SQL INSERT statement
            placeholders = ', '.join('?' * len(data))
            columns = ', '.join(data.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            connection.commit()
            print("Data inserted successfully")
        except pyodbc.Error as e:
            print("Error while inserting data into SQL Server", e)

    def select_data(self,connection, table):
        
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            print(f"Total number of rows in {table}: {len(rows)}")
            for row in rows:
                print(row)
        
        
        except pyodbc.Error as e:
            print("Error while fetching data from SQL Server", e)
        
        return rows

    def main(self):
        server = self.server
        database = self.database
        username = self.uid
        password = self.pwd
        table = self.table

        # Connect to SQL Server
        
        connection = self.connect_to_sql_server(server, database, username, password)
        if connection is None:
            return

        
        #self.insert_data(connection, table, data)
        
        # Select data from the table
        rows = self.select_data(connection, table)

        # Close the connection
        connection.close()
        print("SQL Server connection is closed")
        return rows

if __name__ == "__main__":
    connect = Connect()
    connect.main()
