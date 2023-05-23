from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

# Création du moteur de base de données
engine = create_engine("postgresql://db_user:zola@localhost:5432/flask_db")

# Création de la session
Session = sessionmaker(bind=engine)
session = Session()

# Définition de la classe modèle
Base = declarative_base()

class Appartement(Base):
    __tablename__ = 'appartements'
    id = Column(Integer, primary_key=True)
    adresse = Column(String)
    surface = Column(Integer)
    loyer = Column(Integer)
    nombre_pieces = Column(Integer)
    etage = Column(Integer)

    def __repr__(self):
        return f"<Appartement(id={self.id}, adresse={self.adresse}, surface={self.surface}, loyer={self.loyer}, nombre_pieces={self.nombre_pieces}, etage={self.etage})>"
