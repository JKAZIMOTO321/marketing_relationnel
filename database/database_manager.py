from dotenv import load_dotenv
import os
import mysql.connector as connector

load_dotenv()

class DatabaseManager():
    def __init__(self):
        self.configuration={
            'host':os.getenv("DB_Host"),
            'user':os.getenv("DB_user"),
            'password': os.getenv("DB_PassWord"),
            'database' : os.getenv("DB_Name")
        }

    def connecter(self):
        try:
            return connector.connect(**self.configuration)
        except:
            print(f"Echec de connexion a la base des donnees :{Exception}")
            return None
    
    def get_clients(self):
        conn = self.connecter()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clients")
            result = cursor.fetchall()
            conn.close()
            return result
        
    def add_client(self):
        pass

