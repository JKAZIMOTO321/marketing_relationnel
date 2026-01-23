from dotenv import load_dotenv
import os
import mysql.connector as connector

load_dotenv()

class DataBaseManager():
    def __init__(self):
        self.configuration={
            'host':os.getenv("DB_Host"),
            'user':os.getenv("DB_user"),
            'password': os.getenv("DB_PassWord"),
            'database' : os.getenv("DB_Name")
        }

    def connecter(self):
        return connector.connect(**self.configuration)
