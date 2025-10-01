# app/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 
# Importa as configurações do banco (URL de conexão)
from .config import settings  

# Cria o motor de conexão (Engine)
# 'settings.DATABASE_URL' contém a string de conexão completa (ex: mysql+pymysql://user:pass@host/db)
engine = create_engine(settings.DATABASE_URL)

# Cria a classe de Sessão
# sessionmaker cria uma "fábrica" de sessões para que cada requisição da API (get_db)
# possa obter uma sessão isolada e segura.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Objeto Base para os Modelos
# Base é o ponto de partida que as classes de modelo (models.py) herdam.
# Ela informa ao SQLAlchemy quais classes devem ser mapeadas para tabelas no banco.
Base = declarative_base()