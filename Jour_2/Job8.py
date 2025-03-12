#SQL :
# CREATE DATABASE zoo;
# USE zoo;

# CREATE TABLE cage (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     superficie DECIMAL(10, 2),
#     capacite_max INT
# );

# CREATE TABLE animal (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     nom VARCHAR(255),
#     race VARCHAR(255),
#     id_cage INT,
#     date_naissance DATE,
#     pays_origine VARCHAR(255),
#     FOREIGN KEY (id_cage) REFERENCES cage(id)
# );

#python :
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv


load_dotenv()
PASSWORD = os.getenv("PASSWORD")

class Zoo:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=PASSWORD,
                use_pure=True,
                database="zoo"
            )
            self.cursor = self.connection.cursor()
            print("Connexion à la base de données réussie.")
        except Error as e:
            print(f"Erreur de connexion à la base de données : {e}")

    def ajouter_animal(self, nom, race, id_cage, date_naissance, pays_origine):
        try:
            query = """
                INSERT INTO animal (nom, race, id_cage, date_naissance, pays_origine)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (nom, race, id_cage, date_naissance, pays_origine)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Animal ajouté avec succès.")
        except Error as e:
            print(f"Erreur lors de l'ajout de l'animal : {e}")

    def supprimer_animal(self, id):
        try:
            query = "DELETE FROM animal WHERE id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Animal supprimé avec succès.")
        except Error as e:
            print(f"Erreur lors de la suppression de l'animal : {e}")

    def modifier_animal(self, id, nom=None, race=None, id_cage=None, date_naissance=None, pays_origine=None):
        try:
            updates = []
            values = []
            if nom:
                updates.append("nom = %s")
                values.append(nom)
            if race:
                updates.append("race = %s")
                values.append(race)
            if id_cage:
                updates.append("id_cage = %s")
                values.append(id_cage)
            if date_naissance:
                updates.append("date_naissance = %s")
                values.append(date_naissance)
            if pays_origine:
                updates.append("pays_origine = %s")
                values.append(pays_origine)
            values.append(id)
            query = f"UPDATE animal SET {', '.join(updates)} WHERE id = %s"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Animal modifié avec succès.")
        except Error as e:
            print(f"Erreur lors de la modification de l'animal : {e}")

    def ajouter_cage(self, superficie, capacite_max):
        try:
            query = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
            values = (superficie, capacite_max)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Cage ajoutée avec succès.")
        except Error as e:
            print(f"Erreur lors de l'ajout de la cage : {e}")

    def supprimer_cage(self, id):
        try:
            query = "DELETE FROM cage WHERE id = %s"
            values = (id,)
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Cage supprimée avec succès.")
        except Error as e:
            print(f"Erreur lors de la suppression de la cage : {e}")

    def modifier_cage(self, id, superficie=None, capacite_max=None):
        try:
            updates = []
            values = []
            if superficie:
                updates.append("superficie = %s")
                values.append(superficie)
            if capacite_max:
                updates.append("capacite_max = %s")
                values.append(capacite_max)
            values.append(id)
            query = f"UPDATE cage SET {', '.join(updates)} WHERE id = %s"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Cage modifiée avec succès.")
        except Error as e:
            print(f"Erreur lors de la modification de la cage : {e}")

    def afficher_animaux(self):
        try:
            query = "SELECT * FROM animal"
            self.cursor.execute(query)
            animaux = self.cursor.fetchall()
            print("Liste des animaux :")
            for animal in animaux:
                print(animal)
        except Error as e:
            print(f"Erreur lors de la récupération des animaux : {e}")

    def afficher_animaux_par_cage(self):
        try:
            query = """
                SELECT c.id AS cage_id, a.nom, a.race, a.date_naissance, a.pays_origine
                FROM cage c
                LEFT JOIN animal a ON c.id = a.id_cage
                ORDER BY c.id
            """
            self.cursor.execute(query)
            resultats = self.cursor.fetchall()
            print("Animaux par cage :")
            for resultat in resultats:
                print(resultat)
        except Error as e:
            print(f"Erreur lors de la récupération des animaux par cage : {e}")

    def calculer_superficie_totale(self):
        try:
            query = "SELECT SUM(superficie) FROM cage"
            self.cursor.execute(query)
            superficie_totale = self.cursor.fetchone()[0]
            print(f"Superficie totale des cages : {superficie_totale} m²")
        except Error as e:
            print(f"Erreur lors du calcul de la superficie totale : {e}")

    def close_connection(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Connexion à la base de données fermée.")
        except Error as e:
            print(f"Erreur lors de la fermeture de la connexion : {e}")

# Exemple 
if __name__ == "__main__":
    zoo = Zoo()

    # Ajouter des cages
    zoo.ajouter_cage(50.5, 5)
    zoo.ajouter_cage(30.0, 3)

    # Ajouter des animaux
    zoo.ajouter_animal('Lion', 'Félin', 1, '2018-05-15', 'Afrique')
    zoo.ajouter_animal('Tigre', 'Félin', 1, '2019-03-20', 'Asie')
    zoo.ajouter_animal('Ours', 'Ursidé', 2, '2017-07-10', 'Amérique du Nord')

    # Afficher les animaux
    zoo.afficher_animaux()

    # Afficher les animaux par cage
    zoo.afficher_animaux_par_cage()

    # Calculer la superficie totale des cages
    zoo.calculer_superficie_totale()

    # Fermer la connexion
    zoo.close_connection()