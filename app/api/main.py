# app/api/main.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import schemas 
from app.database.database import SessionLocal 
from app.crud import crud 

# Define o router para agrupar todas as rotas de plantas
router = APIRouter(tags=["Enciclopédia"])

# --- DEPENDÊNCIA (Obter a Sessão do DB) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS ---

@router.post("/plantas/", response_model=schemas.Planta, status_code=status.HTTP_201_CREATED)
def create_planta_endpoint(planta: schemas.PlantaCreate, db: Session = Depends(get_db)):
    """Incluir: Adiciona uma nova planta à enciclopédia."""
    return crud.create_planta(db=db, planta=planta)


@router.get("/plantas/", response_model=List[schemas.Planta])
def read_plantas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar: Retorna a lista de todas as plantas."""
    return crud.get_plantas(db, skip=skip, limit=limit)


@router.get("/plantas/{planta_id}", response_model=schemas.Planta)
def read_planta_endpoint(planta_id: int, db: Session = Depends(get_db)):
    """Consultar: Retorna os detalhes de uma planta específica."""
    return crud.get_planta(db, planta_id=planta_id)


@router.put("/plantas/{planta_id}", response_model=schemas.Planta)
def update_planta_endpoint(planta_id: int, planta_update: schemas.PlantaUpdate, db: Session = Depends(get_db)):
    """Alterar: Atualiza todos os dados de uma planta existente."""
    return crud.update_planta(db, planta_id=planta_id, planta_update=planta_update)


@router.delete("/plantas/{planta_id}", response_model=schemas.Planta)
def delete_planta_endpoint(planta_id: int, db: Session = Depends(get_db)):
    """Excluir: Remove uma planta da enciclopédia."""
    return crud.delete_planta(db, planta_id=planta_id)