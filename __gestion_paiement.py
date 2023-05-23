from app import Locataire
from datetime import datetime
from typing import List


class Paiement:
    def __init__(self, id: int, locataire: Locataire, montant: float, date_paiement: datetime):
        self.id = id
        self.locataire = locataire
        self.montant = montant
        self.date_paiement = date_paiement


class GestionPaiement:
    def __init__(self):
        self.paiements = []

    def ajouter_paiement(self, locataire: Locataire, montant: float):
        paiement = Paiement(
            id=len(self.paiements) + 1,
            locataire=locataire,
            montant=montant,
            date_paiement=datetime.now()
        )
        self.paiements.append(paiement)

    def get_paiements(self) -> List[Paiement]:
        return self.paiements
