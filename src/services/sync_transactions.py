import requests
import pyodbc
from datetime import datetime
from src.app.client import get_transactions
from src.database.queries import INSERT_TRANSACTION, UPDATE_TRANSACTION
from src.database.connection import get_db_connection  
from src.utils.logger import logger  

def sync_transactions():
    """Sincroniza as transações da Pluggy para o banco de dados."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logger.info("TRANSACTIONS - Iniciando a sincronização das transações.")
    
    try:
        cursor.execute("SELECT DISTINCT account_id FROM pluggy_accounts")
        account_ids = [row[0] for row in cursor.fetchall()]
        logger.info(f"TRANSACTIONS - Encontrados {len(account_ids)} account_ids para sincronizar.")
    except Exception as e:
        logger.error(f"TRANSACTIONS - Erro ao buscar accountIds: {e}")
        return

    for account_id in account_ids:
        try:
            logger.info(f"TRANSACTIONS - Buscando transações para o account_id {account_id}")
            item_transactions = get_transactions(account_id)

            inserted_count = 0
            for transaction in item_transactions:
                try:
                    cursor.execute("SELECT COUNT(*) FROM pluggy_transactions WHERE transaction_id = ?", (transaction['id'],))
                    exists = cursor.fetchone()[0] > 0

                    if not exists:
                        cursor.execute(INSERT_TRANSACTION, (
                            transaction['id'],
                            transaction['accountId'],
                            transaction['description'],
                            transaction['currencyCode'],
                            0 if transaction['amount'] >= 0 else abs(transaction['amount']),  # debit
                            0 if transaction['amount'] < 0 else abs(transaction['amount']),   # credit
                            transaction['date'],
                            transaction['category'],
                            transaction['balance'],
                            transaction['providerCode'],
                            transaction['status'],
                            transaction['type'],

                            transaction.get('payerName', ''),
                            transaction.get('payerCnpj', ''),
                            transaction.get('receiverName', ''),
                            transaction.get('receiverCnpj', ''),
                            transaction.get('merchantName', ''),
                            transaction.get('merchantCnpj', ''),
                            transaction.get('merchantCnae', ''),
                            transaction.get('paymentMethod', ''),
                            transaction.get('referenceNumber', ''),
                            transaction.get('digitableLine', ''),
                            transaction.get('baseAmount', 0),

                            transaction['createdAt'],
                            transaction['updatedAt']
                        ))

                        inserted_count += 1
                        logger.info(f"Inserindo nova transação {transaction['id']}")
                except Exception as e:
                    logger.error(f"Erro ao processar a transação {transaction['id']}: {str(e)}")
                    logger.error(f"Detalhes da transação: {transaction}")

            #logger.info(f"Fim das transações para account_id {account_id}.")
            if inserted_count == 0:
                logger.info(f"TRANSACTIONS - AccountID {account_id}: Nenhuma nova transação inserida.")
            else:
                logger.info(f"TRANSACTIONS - AccountID {account_id}: {inserted_count} nova(s) transação(ões) inserida(s).")
            
        except Exception as e:
            logger.error(f"TRANSACTIONS - Erro ao buscar transações para o account_id {account_id}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    logger.info("TRANSACTIONS - Sincronização das transações concluída.")


if __name__ == "__main__":
    sync_transactions()
