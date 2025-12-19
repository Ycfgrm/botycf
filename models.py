import random

ENIGMES = [
    {"question": "Je suis le dieu de la foudre et le roi de l'Olympe. Qui suis-je ?", "reponse": "zeus"},
    {"question": "Quel héros a vaincu la Méduse et tranché sa tête ?", "reponse": "persée"},
    {"question": "Je garde les Enfers et possède trois têtes. Qui suis-je ?", "reponse": "cerbère"},
    {"question": "Quelle déesse est née de l'écume de la mer ?", "reponse": "aphrodite"}
]


class Artefact:
    
    
    def __init__(self, rarete, nom=None, fragments_possedes=1, est_reconstitue=False):
        # Liste thématique liée à l'archéologie et la mythologie [cite: 3, 7]
        artefacts_mythiques = {
            "Commun": ["Éclat de Vase Grec", "Fragment de Tablette", "Pointe de Flèche"],
            "Rare": ["Statue Brisée d'Athéna", "Relique d'Osiris", "Masque de Jade"],
            "Légendaire": ["Foudre de Zeus", "Trident de Poséidon", "Égide d'Athéna"]
        }
        
        self.rarete = rarete
        self.nom = nom if nom else random.choice(artefacts_mythiques.get(rarete))
        self.fragments_possedes = fragments_possedes
        self.fragments_requis = self._definir_besoin()
        self.est_reconstitue = est_reconstitue
        self.valeur_base = self._generer_valeur()

    def _definir_besoin(self):
        """Définit combien de fragments sont nécessaires selon la rareté """
        besoins = {"Commun": 1, "Rare": 3, "Légendaire": 5}
        return besoins.get(self.rarete, 1)

    def _generer_valeur(self):
        """Valeur estimée de l'artefact une fois complet [cite: 17]"""
        mult = {"Commun": 20, "Rare": 150, "Légendaire": 1000}
        return mult.get(self.rarete, 20) + random.randint(1, 50)

    def prix_revente(self):
        """L'objet vaut beaucoup plus s'il est reconstitué [cite: 14, 16]"""
        if self.est_reconstitue:
            return int(self.valeur_base)
        # Un objet en fragments ne vaut que 10% de sa valeur finale
        return int(self.valeur_base * 0.10)

    def to_dict(self):
        """Format pour le stockage JSON persistant [cite: 10]"""
        return {
            "nom": self.nom,
            "rarete": self.rarete,
            "fragments_possedes": self.fragments_possedes,
            "fragments_requis": self.fragments_requis,
            "est_reconstitue": self.est_reconstitue,
            "valeur_base": self.valeur_base
        }