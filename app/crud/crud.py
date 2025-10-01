# app/crud/crud.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from app.models import models 
from app.schemas import schemas

# ----------------------------------
# Funções de Leitura (GET)
# ----------------------------------

def get_planta(db: Session, planta_id: int):
    """Consulta uma planta pelo ID."""
    db_planta = db.query(models.Planta).filter(models.Planta.id == planta_id).first()
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada na enciclopédia")
    return db_planta

def get_plantas(db: Session, skip: int = 0, limit: int = 100):
    """Lista todas as plantas, com paginação opcional."""
    return db.query(models.Planta).order_by(models.Planta.id).offset(skip).limit(limit).all()

# ----------------------------------
# Função de Criação (POST) - Com Validação de Unicidade
# ----------------------------------

def create_planta(db: Session, planta: schemas.PlantaCreate):
    """Inclui uma nova planta no banco, verificando a unicidade do nome científico."""
    
    # Validação de Negócio (Unicidade do Nome Científico)
    db_planta = db.query(models.Planta).filter(models.Planta.nome_cientifico == planta.nome_cientifico).first()
    if db_planta:
        raise HTTPException(status_code=400, detail="Nome científico já cadastrado na enciclopédia.")

    # Criação da nova planta
    db_planta = models.Planta(**planta.model_dump())
    db.add(db_planta)
    db.commit()
    db.refresh(db_planta)
    return db_planta

# ----------------------------------
# Função de Atualização (PUT) - COM VALIDAÇÃO DE NEGÓCIO DE UNICIDADE
# ----------------------------------

def update_planta(db: Session, planta_id: int, planta_update: schemas.PlantaUpdate):
    """Atualiza uma planta existente, incluindo a verificação de unicidade no nome científico."""
    
    # 1. Tenta encontrar a planta (trata o 404)
    db_planta = get_planta(db, planta_id) 
    
    # 2. VALIDAÇÃO DE NEGÓCIO: Checar unicidade do novo nome científico
    if planta_update.nome_cientifico and planta_update.nome_cientifico != db_planta.nome_cientifico:
        planta_existente = db.query(models.Planta).filter(
            models.Planta.nome_cientifico == planta_update.nome_cientifico
        ).filter(
            models.Planta.id != planta_id 
        ).first()
        
        if planta_existente:
            raise HTTPException(status_code=400, detail="Nome científico já está em uso por outra planta.")

    # 3. Atualização dos campos
    update_data = planta_update.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(db_planta, key, value)
        
    db.commit()
    db.refresh(db_planta)
    return db_planta

# ----------------------------------
# Função de Exclusão (DELETE)
# ----------------------------------

def delete_planta(db: Session, planta_id: int):
    """Exclui uma planta pelo ID."""
    
    db_planta = get_planta(db, planta_id)

    db.delete(db_planta)
    db.commit()
    return db_planta