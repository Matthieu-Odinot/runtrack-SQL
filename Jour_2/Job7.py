import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


load_dotenv()
PASSWORD = os.getenv("PASSWORD")

class Employe:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=PASSWORD,
            use_pure=True,
            database="Entreprise"
        )
        self.cursor = self.connection.cursor()

    def create_employe(self, nom, prenom, salaire, id_service):
        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        values = (nom, prenom, salaire, id_service)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Employé ajouté avec succès.")

    def read_employes(self):
        query = "SELECT * FROM employe"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_employe(self, id, salaire):
        query = "UPDATE employe SET salaire = %s WHERE id = %s"
        values = (salaire, id)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Employé mis à jour avec succès.")

    def delete_employe(self, id):
        query = "DELETE FROM employe WHERE id = %s"
        values = (id,)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Employé supprimé avec succès.")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    employe = Employe()

    employe.create_employe('saucisson', 'Luc', 4500.00, 2)

    print("Liste des employés :")
    for emp in employe.read_employes():
        print(emp)

    employe.update_employe(1, 3800.00)

    employe.delete_employe(2)

    employe.close_connection()