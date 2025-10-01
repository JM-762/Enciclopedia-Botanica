# app/api/main.py - Definição das Rotas (Endpoints) da API
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
# Importa a função de sessão do DB
from app.database.database import SessionLocal 
from app.crud import crud 

# Cria o roteador da API com tag para documentação
router = APIRouter(tags=["Enciclopédia"])

# Dependência: Garante que cada requisição use uma sessão de DB e a feche
def get_db():
    db = SessionLocal()
    try:
        yield db # Retorna a sessão, mantendo-a aberta durante a requisição
    finally:
        db.close()

# ROTA: POST /plantas/ (CREATE)
@router.post("/plantas/", response_model=schemas.Planta)
def criar_planta(planta: schemas.PlantaCreate, db: Session = Depends(get_db)):
    # 1. Checa se o nome científico já existe no banco de dados (Regra de Negócio)
    if crud.get_planta_by_nome_cientifico(db, nome_cientifico=planta.nome_cientifico):
        # Se existir, retorna erro 400 Bad Request
        raise HTTPException(status_code=400, detail="Nome científico já cadastrado.")
    
    # 2. Chama a função CRUD para criar o registro no DB
    return crud.create_planta(db=db, planta=planta)

# ROTA: GET /plantas/ (READ ALL)
@router.get("/plantas/", response_model=List[schemas.Planta])
def listar_plantas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Simplesmente chama o CRUD para listar todas as plantas
    return crud.get_plantas(db, skip=skip, limit=limit)

# ROTA: GET /plantas/{planta_id} (READ ONE)
@router.get("/plantas/{planta_id}", response_model=schemas.Planta)
def consultar_planta(planta_id: int, db: Session = Depends(get_db)):
    db_planta = crud.get_planta(db, planta_id=planta_id)
    # Se a planta não for encontrada, retorna erro 404 Not Found
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada.")
    return db_planta

# ROTA: PUT /plantas/{planta_id} (UPDATE)
@router.put("/plantas/{planta_id}", response_model=schemas.Planta)
def atualizar_planta(planta_id: int, planta: schemas.PlantaUpdate, db: Session = Depends(get_db)):
    # 1. Encontra a planta existente pelo ID
    db_planta = crud.get_planta(db, planta_id=planta_id)
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada.")
    
    # 2. Checa a regra de unicidade (se o nome científico foi alterado)
    if planta.nome_cientifico != db_planta.nome_cientifico:
        if crud.get_planta_by_nome_cientifico(db, nome_cientifico=planta.nome_cientifico):
            raise HTTPException(status_code=400, detail="Novo nome científico já está em uso.")
            
    # 3. Chama o CRUD para atualizar o registro
    return crud.update_planta(db, db_planta, planta)

# ROTA: DELETE /plantas/{planta_id} (DELETE)
@router.delete("/plantas/{planta_id}", response_model=schemas.Planta)
def excluir_planta(planta_id: int, db: Session = Depends(get_db)):
    # 1. Encontra a planta existente pelo ID
    db_planta = crud.get_planta(db, planta_id=planta_id)
    if db_planta is None:
        raise HTTPException(status_code=404, detail="Planta não encontrada.")
    
    # 2. Chama o CRUD para excluir e retorna a planta excluída
    crud.delete_planta(db, db_planta)
    return db_planta