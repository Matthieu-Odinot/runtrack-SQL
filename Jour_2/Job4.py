import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


load_dotenv()
PASSWORD = os.getenv("PASSWORD")

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=PASSWORD,
    use_pure=True,
    database="LaPlateforme"
)


cursor = my_db.cursor() 
cursor.execute("SELECT nom, capacite FROM salle")
rows = cursor.fetchall()
print("Noms et capacités des salles :")
for (nom, capacite) in rows:
    print(f"- {nom}: {capacite} places")

cursor.close()
my_db.close()