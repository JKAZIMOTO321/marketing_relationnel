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
        self.connexion = None

    def connecter(self):
        if self.connexion is None or not self.connexion.is_connected():
            try:
                self.connexion = connector.connect(**self.configuration)
            except Exception as e:
                print(f"Echec de connexion a la base des donnees :{e}")
        return self.connexion
    
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

db = DatabaseManager()
db.connecter()