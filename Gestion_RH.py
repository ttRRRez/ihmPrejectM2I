from dbScript import DatabaseHandler


class Employe:
    def __init__(self, id, prenom, nom, age, poste, salaire):
        self.id = id
        self.prenom = prenom
        self.nom = nom
        self.age = age
        self.poste = poste
        self.salaire = salaire

    def __str__(self):
        return f"ID: {self.id}, Prénom: {self.prenom}, Nom: {self.nom}, Age: {self.age}, Poste: {self.poste}, Salaire: {self.salaire}"


class Departement:
    def __init__(self, id, nom, id_manager=None, nom_manager=None, salaire_total=0):
        self.id = id
        self.nom = nom
        self.id_manager = id_manager
        self.nom_manager = nom_manager
        self.salaire_total = salaire_total

    def __str__(self):
        return f"ID: {self.id}, Nom: {self.nom}, Manager: {self.nom_manager}, Salaire Total (TL): {self.salaire_total}"


class SystemeRH:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def ajouter_employe(self, prenom, nom, age, poste, salaire):
        """Ajouter un employé à la base de données."""
        try:
            self.db_handler.execute_query(
                "INSERT INTO employes (prenom, nom, age, poste, salaire) VALUES (?, ?, ?, ?, ?)",
                (prenom, nom, age, poste, salaire)
            )
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'employé: {e}")

    def obtenir_employe(self, id):
        """Obtenir un employé à partir de son ID."""
        try:
            result = self.db_handler.fetch_query("SELECT * FROM employes WHERE id = ?", (id,))
            if result:
                ligne = result[0]
                return Employe(ligne[0], ligne[1], ligne[2], ligne[3], ligne[4], ligne[5])
            return None
        except Exception as e:
            print(f"Erreur lors de l'obtention de l'employé: {e}")
            return None

    def ajouter_departement(self, nom, id_manager=None):
        """Ajouter un département à la base de données."""
        try:
            self.db_handler.execute_query(
                "INSERT INTO departements (nom, id_manager) VALUES (?, ?)", (nom, id_manager)
            )
        except Exception as e:
            print(f"Erreur lors de l'ajout du département: {e}")

    def obtenir_departement(self, id):
        """Obtenir un département à partir de son ID."""
        try:
            result = self.db_handler.fetch_query("SELECT * FROM departements WHERE id = ?", (id,))
            if result:
                ligne = result[0]
                if ligne[2]: 
                    manager_result = self.db_handler.fetch_query("SELECT prenom, nom FROM employes WHERE id = ?", (ligne[2],))
                    manager = manager_result[0]
                    nom_manager = f"{manager[0]} {manager[1]}"
                else:
                    nom_manager = "Aucun manager"

                salaire_total_result = self.db_handler.fetch_query("SELECT SUM(salaire) FROM employes WHERE id_manager = ?", (ligne[0],))
                salaire_total = salaire_total_result[0][0] if salaire_total_result[0][0] else 0

                return Departement(ligne[0], ligne[1], ligne[2], nom_manager, salaire_total)
            return None
        except Exception as e:
            print(f"Erreur lors de l'obtention du département: {e}")
            return None

    def lister_employes(self):
        """Lister tous les employés."""
        try:
            result = self.db_handler.fetch_query("SELECT * FROM employes")
            return [Employe(ligne[0], ligne[1], ligne[2], ligne[3], ligne[4], ligne[5]) for ligne in result]
        except Exception as e:
            print(f"Erreur lors de la liste des employés: {e}")
            return []

    def lister_departements(self):
        """Lister tous les départements."""
        try:
            result = self.db_handler.fetch_query("SELECT * FROM departements")
            departements = []
            for ligne in result:
                if ligne[2]:
                    manager_result = self.db_handler.fetch_query("SELECT prenom, nom FROM employes WHERE id = ?", (ligne[2],))
                    manager = manager_result[0]
                    nom_manager = f"{manager[0]} {manager[1]}"
                else:
                    nom_manager = "Aucun manager"

                salaire_total_result = self.db_handler.fetch_query("SELECT SUM(salaire) FROM employes WHERE id_manager = ?", (ligne[0],))
                salaire_total = salaire_total_result[0][0] if salaire_total_result[0][0] else 0

                departement = Departement(ligne[0], ligne[1], ligne[2], nom_manager, salaire_total)
                departements.append(departement)
            return departements
        except Exception as e:
            print(f"Erreur lors de la liste des départements: {e}")
            return []

    def supprimer_employe(self, id):
        """Supprimer un employé de la base de données."""
        try:
            result = self.db_handler.fetch_query("SELECT id FROM departements WHERE id_manager = ?", (id,))
            if result: 
                print("Impossible de supprimer cet employé car il est un manager dans un département.")
                return False

            self.db_handler.execute_query("DELETE FROM employes WHERE id = ?", (id,))
            print(f"Employé avec ID {id} supprimé avec succès.")
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de l'employé: {e}")
            return False

    def update_employe(self, id, prenom=None, nom=None, age=None, poste=None, salaire=None):
        """Met à jour les informations d'un employé."""
        try:
            update_fields = []
            update_values = []

            if prenom:
                update_fields.append("prenom = ?")
                update_values.append(prenom)
            if nom:
                update_fields.append("nom = ?")
                update_values.append(nom)
            if age:
                update_fields.append("age = ?")
                update_values.append(age)
            if poste:
                update_fields.append("poste = ?")
                update_values.append(poste)
            if salaire:
                update_fields.append("salaire = ?")
                update_values.append(salaire)

            # Si des champs ont été fournis pour la mise à jour
            if update_fields:
                query = f"UPDATE employes SET {', '.join(update_fields)} WHERE id = ?"
                update_values.append(id)
                self.db_handler.execute_query(query, tuple(update_values))
                print(f"Employé avec ID {id} mis à jour avec succès.")
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'employé: {e}")
            return False

    def fermer(self):
        """Fermer la connexion à la base de données."""
        self.db_handler.fermer()


if __name__ == "__main__":
    # Créer l'instance de DatabaseHandler
    db_handler = DatabaseHandler()

    # Créer l'instance de SystemeRH
    systeme_rh = SystemeRH(db_handler)

    # Ajouter des employés
    systeme_rh.ajouter_employe("Mohamed", "El Amrani", 30, "Ingénieur Informatique", 70000)
    systeme_rh.ajouter_employe("Yassir", "Benkirane", 28, "Développeur Web", 50000)
    systeme_rh.ajouter_employe("Fatima Zahra", "Oufkir", 34, "Responsable RH", 80000)
    systeme_rh.ajouter_employe("Imane", "Berrada", 27, "Chargée de recrutement", 45000)

    # Ajouter des départements
    systeme_rh.ajouter_departement("Technologie", 1)  # Mohamed El Amrani est le manager
    systeme_rh.ajouter_departement("Ressources Humaines", 3)  # Fatima Zahra Oufkir est le manager

    # Obtenir et afficher un employé
    employe = systeme_rh.obtenir_employe(1)
    if employe:
        print(employe)

    # Obtenir et afficher un département
    departement = systeme_rh.obtenir_departement(1)
    if departement:
        print(departement)

    # Lister tous les employés
    print("\nTous les Employés:")
    for emp in systeme_rh.lister_employes():
        print(emp)

    # Lister tous les départements
    print("\nTous les Départements:")
    for dep in systeme_rh.lister_departements():
        print(dep)

    # Mettre à jour un employé
    systeme_rh.update_employe(1, salaire=75000, poste="Senior Ingénieur Informatique")

    # Supprimer un employé
    systeme_rh.supprimer_employe(2)  # Suppression de l'employé avec ID 2

    # Fermer la connexion à la base de données
    systeme_rh.fermer()
