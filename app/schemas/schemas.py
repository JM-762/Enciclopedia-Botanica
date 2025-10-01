# app/schemas/schemas.py

from pydantic import BaseModel, ConfigDict

# Classe Base: Define os atributos comuns a todas as operações (Base do CRUD)
class PlantaBase(BaseModel): 
    # Atributos esperados nos dados de entrada/saída da API
    nome_popular: str 
    nome_cientifico: str 
    familia: str
    origem: str
    cuidados: str

# Classe de Criação (POST): Herda todos os campos de PlantaBase
# É usada na rota POST para garantir que todos os campos sejam fornecidos
class PlantaCreate(PlantaBase): 
    pass

# Classe de Atualização (PUT): Herda todos os campos de PlantaBase
# É usada na rota PUT para validar os dados de atualização
class PlantaUpdate(PlantaBase):
    pass

# Classe de Resposta (GET): Herda PlantaBase e adiciona o 'id'
# É o formato de dados que a API retorna para o frontend após qualquer operação.
class Planta(PlantaBase):
    id: int # O ID é gerado pelo banco, por isso só aparece no retorno.
    
    # Configuração necessária para que o Pydantic consiga ler
    # os dados diretamente de uma instância do modelo SQLAlchemy (models.Planta).
    model_config = ConfigDict(from_attributes=True)