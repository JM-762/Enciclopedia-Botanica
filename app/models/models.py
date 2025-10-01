# app/models/models.py

from sqlalchemy import Column, Integer, String, Text 
from app.database.database import Base # Importa o objeto Base para a declaração da tabela
    
# Classe principal que mapeia a tabela 'plantas_enciclopedia' no banco
class Planta(Base): 
    __tablename__ = "plantas_enciclopedia" # Nome da tabela no MySQL

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True) # Chave primária e índice
    nome_popular = Column(String(100), index=True) 
    # unique=True: Impede que haja duas plantas com o mesmo nome científico (regra de negócio)
    nome_cientifico = Column(String(100), unique=True, index=True)
    familia = Column(String(100))
    origem = Column(String(200))
    cuidados = Column(Text)