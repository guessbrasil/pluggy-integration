from src.app.client import get_items
from src.database.connection import get_db_connection
from src.utils.logger import logger
from src.database.queries import INSERT_ITEM, UPDATE_ITEM

def sync_items():
    """Sincroniza os itens da API Pluggy com o banco do ERP."""
    logger.info("ITEMS - Iniciando sincronização de itens...")

    items = get_items()  
    
    if not items:
        logger.warning("ITEMS - Nenhum item encontrado.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for item in items:
        item_id = item.get("item_id")
        item_name = item.get("connector_name")
        item_type = item.get("connector_type")
        created_at = item.get("created_at")
        updated_at = item.get("updated_at")
        status = item.get("status")
        execution_status = item.get("execution_status")
        last_updated_at = item.get("last_updated_at")

        cursor.execute("SELECT COUNT(*) FROM pluggy_items WHERE item_id = ?", (item_id,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            logger.info(f"ITEMS - Item {item_id} já cadastrado. Atualizando informações...")
            cursor.execute(UPDATE_ITEM, (item_name, item_type, status, execution_status, item_id))
        else:
            logger.info(f"ITEMS - Inserindo item com id: {item_id}, nome: {item_name}, tipo: {item_type}")
            cursor.execute(INSERT_ITEM, (item_id, item_name, item_type, created_at, updated_at, status, execution_status, last_updated_at))

    conn.commit()
    conn.close()
    logger.info("ITEMS - Sincronização de itens concluída com sucesso!")


sync_items()