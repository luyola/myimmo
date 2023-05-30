from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship

# Création de la base de données
engine = create_engine("postgresql://db_user:zola@localhost:5432/flask_db")

# Déclaration de la base de modèle
Base = declarative_base()

# Associer la base de données à la base de modèle
Base.metadata.bind = engine


class Appartement(Base):
    __tablename__ = 'appartements'
    id = Column(Integer, primary_key=True)
    adresse = Column(String)
    surface = Column(Integer)
    loyer = Column(Integer)
    nombre_pieces = Column(Integer)
    etage = Column(Integer)
    locataires = relationship("Locataire", back_populates="appartement")
    paiements = relationship("Paiement", back_populates="appartement")


class Locataire(Base):
    __tablename__ = 'locataires'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    prenom = Column(String)
    date_naissance = Column(String)
    adresse = Column(String)
    ville = Column(String)
    telephone = Column(String)
    email = Column(String)
    depot_garantie = Column(Integer)
    appartement_id = Column(Integer, ForeignKey('appartements.id'))
    appartement = relationship("Appartement", back_populates="locataires")
    paiements = relationship("Paiement", back_populates="locataire")


class Paiement(Base):
    __tablename__ = 'paiements'
    id = Column(Integer, primary_key=True)
    locataire_id = Column(Integer, ForeignKey('locataires.id'))
    appartement_id = Column(Integer, ForeignKey('appartements.id'))
    montant = Column(Integer)
    statut = Column(String)
    mois = Column(String)
    date_paiement = Column(Date)

    locataire = relationship("Locataire", back_populates="paiements")
    appartement = relationship("Appartement", back_populates="paiements")


# Création des tables dans la base de données
Base.metadata.create_all(engine)
