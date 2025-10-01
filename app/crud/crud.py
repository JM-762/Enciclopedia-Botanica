# app/crud/crud.py - Lógica de Interação com o Banco de Dados

from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

# Consulta uma planta pelo ID (Usado para UPDATE, DELETE e GET por ID)
def get_planta(db: Session, planta_id: int):
    # Filtra a tabela Planta pelo ID e retorna o primeiro resultado
    return db.query(models.Planta).filter(models.Planta.id == planta_id).first()

# Consulta todas as plantas (Usado para listar o acervo)
def get_plantas(db: Session, skip: int = 0, limit: int = 100):
    # Retorna todas as plantas, aplicando paginação básica (offset e limit)
    return db.query(models.Planta).offset(skip).limit(limit).all()

# Consulta uma planta pelo nome científico (Usado para checar duplicidade na criação/edição)
def get_planta_by_nome_cientifico(db: Session, nome_cientifico: str):
    return db.query(models.Planta).filter(models.Planta.nome_cientifico == nome_cientifico).first()

# CRIAÇÃO (CREATE)
def create_planta(db: Session, planta: schemas.PlantaCreate):
    # Cria uma instância do modelo do DB a partir dos dados do schema Pydantic
    db_planta = models.Planta(**planta.dict())
    
    # Adiciona o objeto à sessão
    db.add(db_planta)
    # Persiste a mudança no banco de dados (commit)
    db.commit()
    db.refresh(db_planta)
    
    return db_planta

# ATUALIZAÇÃO (UPDATE)
def update_planta(db: Session, db_planta: models.Planta, planta_data: schemas.PlantaUpdate):
    # Itera sobre os dados recebidos para atualizar os atributos do objeto no DB
    for key, value in planta_data.dict().items():
        setattr(db_planta, key, value)
        
    db.commit()
    db.refresh(db_planta)
    return db_planta

# EXCLUSÃO (DELETE)
def delete_planta(db: Session, db_planta: models.Planta):
    # Exclui o objeto da sessão
    db.delete(db_planta)
    db.commit()
    return db_planta