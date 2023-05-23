from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Création du moteur de base de données
engine = create_engine("postgresql://db_user:zola@localhost:5432/flask_db")

# Déclaration de la base de modèle
Base = declarative_base()

# Associer le moteur de base de données à la base de modèle
Base.metadata.bind = engine

# Définition du modèle Appartement
class Appartement(Base):
    __tablename__ = 'appartements'
    id = Column(Integer, primary_key=True)
    adresse = Column(String)
    surface = Column(Integer)
    loyer = Column(Integer)
    nombre_pieces = Column(Integer)
    etage = Column(Integer)
    locataires = relationship("Locataire", back_populates="appartement")

    # Définition du modèle Locataire
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

# Création des tables dans la base de données
Base.metadata.create_all(engine)
