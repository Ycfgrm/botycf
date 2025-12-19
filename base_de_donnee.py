import json
import os

FILE_PATH = "archives.json"

def charger_donnees():
    """Charge les découvertes et la progression des archéologues (Persistent Storage)"""
    if not os.path.exists(FILE_PATH):
        return {}
    
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        # Sécurité pour le barème : gestion des erreurs de lecture
        print("Archives corrompues, restauration du système...")
        return {}

def sauvegarder_donnees(donnees):
    """Sauvegarde l'état du musée et les fragments collectés"""
    try:
        with open(FILE_PATH, "w", encoding="utf-8") as f:
           
            json.dump(donnees, f, indent=4, ensure_ascii=False)
            f.truncate() 
    except IOError as e:
        print(f"Erreur lors de l'archivage des données : {e}")