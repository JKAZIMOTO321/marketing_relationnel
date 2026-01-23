from dotenv import load_dotenv
import os
import mysql.connector as connector

load_dotenv()

connexion = connector.connect(
    host=os.getenv("DB_Host"),
    user=os.getenv("DB_user"),
    password = os.getenv("DB_PassWord"),
    database = os.getenv("DB_Name"),)

print("Connecté à MySQL :", connexion.is_connected())
connexion.close()