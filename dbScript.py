import sqlite3
import sqlite3

class DatabaseHandler:
    def __init__(self, nom_db="base_de_donnees_rh.db"):
        self.connexion = sqlite3.connect(nom_db)
        self.curseur = self.connexion.cursor()
        self._creer_tables()

    def _creer_tables(self):
  
        self.curseur.execute("""
            CREATE TABLE IF NOT EXISTS employes (
                id INTEGER PRIMARY KEY,
                prenom TEXT NOT NULL,
                nom TEXT NOT NULL,
                age INTEGER,
                poste TEXT,
                salaire REAL
            )
        """)
        self.curseur.execute("""
            CREATE TABLE IF NOT EXISTS departements (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                id_manager INTEGER,
                FOREIGN KEY (id_manager) REFERENCES employes(id)
            )
        """)
        
    
        self.curseur.execute("""
            CREATE TABLE IF NOT EXISTS rh (
                id INTEGER PRIMARY KEY,
                nom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        
        self.connexion.commit()

    def execute_query(self, query, params=()):
        self.curseur.execute(query, params)
        self.connexion.commit()

    def fetch_query(self, query, params=()):
        self.curseur.execute(query, params)
        return self.curseur.fetchall()

    def fermer(self):
        self.connexion.close()
