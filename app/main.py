from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import router as api_router 
from app.database.database import engine, Base, SessionLocal
from app.models import models 


# --- INICIALIZAÇÃO E CONFIGURAÇÃO ---

# Cria as tabelas no MySQL, se não existirem
models.Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="Enciclopédia Botânica API - Pacotes Organizados",
    description="API RESTful com estrutura em camadas (API, CRUD, Models, Schemas).",
    version="1.0.0"
)

# Configuração CORS para conectividade com front-end
origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o router (que contém todos os endpoints do CRUD)
app.include_router(api_router) 

# --- LÓGICA DE SEEDING ---

def seed_db():
    db = SessionLocal()
    try:
        if db.query(models.Planta).count() == 0:
            print("Enciclopédia vazia. Semeando com dados iniciais...")
            plantas_iniciais = [
                models.Planta(nome_popular="Jiboia", nome_cientifico="Epipremnum aureum", familia="Araceae", origem="Ilhas Salomão", cuidados="Manter o solo úmido, mas não encharcado. Gosta de luz indireta. Tóxica para pets."),
                models.Planta(nome_popular="Espada-de-São-Jorge", nome_cientifico="Dracaena trifasciata", familia="Asparagaceae", origem="África", cuidados="Muito resistente. Regar apenas quando o solo estiver bem seco. Purifica o ar."),
                models.Planta(nome_popular="Costela-de-Adão", nome_cientifico="Monstera deliciosa", familia="Araceae", origem="México", cuidados="Luz indireta e solo levemente úmido. Limpar as folhas com um pano úmido para remover poeira."),
                models.Planta(nome_popular="Suculenta Orelha-de-Shrek", nome_cientifico="Crassula ovata 'Gollum'", familia="Crassulaceae", origem="África do Sul", cuidados="Solo bem drenado. Regar pouco e apenas quando o solo estiver completamente seco. Sol pleno.")
            ]
            db.add_all(plantas_iniciais)
            db.commit()
            print("Sementeira concluída.")
    finally:
        db.close()

seed_db()