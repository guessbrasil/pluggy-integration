import time
from src.utils.logger import logger

def run_with_retry(func, max_attempts=3, wait_seconds=5):
    """Executa uma função com tentativas de repetição em caso de erro."""
    attempt = 0
    while attempt < max_attempts:
        try:
            func()
            return  # Sucesso, sai da função
        except Exception as e:
            attempt += 1
            logger.error(f"Erro ao executar '{func.__name__}' (tentativa {attempt}/{max_attempts}): {e}")
            if attempt < max_attempts:
                logger.info(f"Tentando novamente em {wait_seconds} segundos...")
                time.sleep(wait_seconds)
            else:
                logger.critical(f"Falha ao executar '{func.__name__}' após {max_attempts} tentativas.")
