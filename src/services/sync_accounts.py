from src.app.client import get_identity
from src.app.client import get_accounts
from src.database.connection import get_db_connection
from src.utils.logger import logger
from src.database.queries import INSERT_ACCOUNT, UPDATE_ACCOUNT
from datetime import datetime



def extract_agency_and_account(transfer_number):
    """Extrai agência e conta do campo transferNumber."""
    try:
        parts = transfer_number.split("/")
        if len(parts) == 3:
            _, agency, account = parts 
            return agency.strip(), account.strip()
        return "", ""
    except Exception as e:
        logger.error(f"ACCOUNTS - Erro ao extrair agência e conta: {e}")
        return "", ""



def sync_accounts():
    """Sincroniza as contas bancárias da API Pluggy com o banco do ERP."""
    logger.info("ACCOUNTS - Iniciando sincronização de contas bancárias...")

    accounts = get_accounts()
    
    if not accounts:
        logger.warning("ACCOUNTS - Nenhuma conta encontrada.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    for account in accounts:
        account_id = account.get("id")
        item_id = account.get("itemId")
        transfer_number = (account.get("bankData") or {}).get("transferNumber", "")
        agency, number = extract_agency_and_account(transfer_number)
        account_type = account.get("type", "Desconhecido")
        balance = account.get("balance", 0.0)
        updated_at = datetime.now()  # Data de atualização local
        identity_data = get_identity(item_id)
        identity_data = get_identity(item_id)
        tax_number = identity_data.get("tax_number", "Desconhecido")
        company = identity_data.get("company", "Desconhecido")

        
        cursor.execute("SELECT connector_name FROM pluggy_items WHERE item_id = ?", (item_id,))
        row = cursor.fetchone()
        connector_name = row[0] if row else "Desconhecido"

        cursor.execute("SELECT COUNT(*) FROM pluggy_accounts WHERE account_id = ?", (account_id,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            logger.info(f"ACCOUNTS - Conta {account_id} já cadastrada. Atualizando informações...")
            cursor.execute(UPDATE_ACCOUNT, (connector_name, agency, number, account_type, balance, updated_at, tax_number, company, account_id)) 
        else:
            logger.info(f"ACCOUNTS - Inserindo nova conta: {account_id} - Banco {connector_name}.")
            cursor.execute(INSERT_ACCOUNT, (account_id, connector_name, agency, number, account_type, balance, updated_at, item_id, tax_number, company))

    conn.commit()
    conn.close()
    logger.info("ACCOUNTS - Sincronização de contas concluída com sucesso!")

sync_accounts()
