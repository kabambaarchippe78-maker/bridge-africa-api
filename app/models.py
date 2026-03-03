from email.policy import default

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base
class Demande(Base):
    __tablename__ = "demandes"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    email = Column(String, index=True)
    telephone = Column(String)
    pays = Column(String)
    service = Column(String)
    date_creation = Column(DateTime, default=datetime.utcnow)
    statut = Column(String, default="nouvelle")