from src.utils.logger import logger
import pyodbc
from src.config.settings import DB_DRIVER, DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

print("Iniciando conexão com o banco de dados...") 

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQL Server."""
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{DB_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
            #"TrustServerCertificate=yes;"
        )
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return None
