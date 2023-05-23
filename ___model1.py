from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Locataire(Base):
    __tablename__ = 'locataires'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    date_naissance = Column(Date)
    adresse = Column(String(200))
    ville = Column(String(100))
    telephone = Column(String(20))
    email = Column(String(100))
    depot_garantie = Column(Numeric(10, 2))
