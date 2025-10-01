# app/models/models.py

from sqlalchemy import Column, Integer, String, Text 
from app.database.database import Base # Importa Base do database.py

class Planta(Base): 
    __tablename__ = "plantas_enciclopedia" 

    id = Column(Integer, primary_key=True, index=True) 
    nome_popular = Column(String(100), index=True) 
    nome_cientifico = Column(String(100), unique=True, index=True)
    familia = Column(String(100))
    origem = Column(String(200))
    cuidados = Column(Text)