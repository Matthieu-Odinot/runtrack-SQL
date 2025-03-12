import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


load_dotenv()
PASSWORD = "test"

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=PASSWORD,
    use_pure=True,
    database="LaPlateforme"
)


cursor = my_db.cursor() 
cursor.execute("SELECT * from etudiant;")
rows = cursor.fetchall()
print(rows)
cursor.close()
my_db.close()
