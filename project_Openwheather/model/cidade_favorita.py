from sqlalchemy import Column, Integer, String
from database.connection import Base

class CidadeFavorita(Base):
    __tablename__ = "cidades_favoritas"

    id = Column(Integer, primary_key=True)
    cidade = Column(String(120), nullable=False)
    apelido = Column(String(120), nullable=False)
