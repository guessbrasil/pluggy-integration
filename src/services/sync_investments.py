import pyodbc
from src.app.client import get_items, get_investments, get_investment_transactions
from src.database.queries import (
    SELECT_INVESTMENTS, INSERT_INVESTMENT, UPDATE_INVESTMENT,
    SELECT_INVESTMENT_TRANSACTIONS, INSERT_INVESTMENT_TRANSACTION, UPDATE_INVESTMENT_TRANSACTION
)
from src.database.connection import get_db_connection
from src.utils.logger import logger

def sync_investments():
    conn = get_db_connection()
    cursor = conn.cursor()
    logger.info("INVESTMENTS - Iniciando sincronização de investimentos.")

    try:
        items = get_items()
        item_ids = [item['item_id'] for item in items]
        logger.info(f"INVESTMENTS - Encontrados {len(item_ids)} item_ids para sincronizar.")
    except Exception as e:
        logger.error(f"INVESTMENTS - Erro ao buscar itemIds: {e}")
        return

    for item_id in item_ids:
        try:
            logger.info(f"INVESTMENTS - Buscando investimentos para o item_id {item_id}")
            investments = get_investments(item_id)
            inserted_count = 0

            for inv in investments:
                try:
                    cursor.execute("SELECT COUNT(*) FROM pluggy_investments WHERE investment_id = ?", (inv['id'],))
                    exists = cursor.fetchone()[0] > 0

                    params = (
                        inv['id'],
                        item_id,
                        inv.get('number'),
                        inv.get('name'),
                        inv.get('balance'),
                        inv.get('currencyCode'),
                        inv.get('type'),
                        inv.get('subtype'),
                        inv.get('lastMonthRate'),
                        inv.get('lastTwelveMonthsRate'),
                        inv.get('annualRate'),
                        inv.get('code'),
                        inv.get('isin'),
                        inv.get('metadata'),
                        inv.get('value'),
                        inv.get('quantity'),
                        inv.get('amount'),
                        inv.get('taxes'),
                        inv.get('taxes2'),
                        inv.get('date'),
                        inv.get('owner'),
                        inv.get('amountProfit'),
                        inv.get('amountWithdrawal'),
                        inv.get('amountOriginal'),
                        inv.get('dueDate'),
                        inv.get('issuer'),
                        inv.get('issuerCNPJ'),
                        inv.get('issueDate'),
                        inv.get('rate'),
                        inv.get('rateType'),
                        inv.get('fixedAnnualRate'),
                        inv.get('status'),
                        inv.get('institution'),
                        inv.get('createdAt'),
                        inv.get('updatedAt')
                    )

                    if not exists:
                        cursor.execute(INSERT_INVESTMENT, params)
                        inserted_count += 1
                        logger.info(f"Inserindo novo investimento {inv['id']}")
                    else:
                        # UPDATE usa os mesmos campos, adicionando updated_at e created_at, e no final o investment_id
                        cursor.execute(UPDATE_INVESTMENT, params[2:] + (inv['id'],))
                        logger.info(f"Atualizando investimento existente {inv['id']}")

                    # Sincronizar transações
                    transactions = get_investment_transactions(inv['id'])
                    for tx in transactions:
                        cursor.execute(
                            "SELECT COUNT(*) FROM pluggy_investment_transactions WHERE transaction_id = ?", 
                            (tx['id'],)
                        )
                        tx_exists = cursor.fetchone()[0] > 0

                        tx_params = (
                            tx['id'],
                            inv['id'],
                            tx.get('amount'),
                            tx.get('description'),
                            tx.get('value'),
                            tx.get('quantity'),
                            tx.get('tradeDate'),
                            tx.get('date'),
                            tx.get('type'),
                            tx.get('netAmount'),
                            tx.get('brokerageNumber'),
                            tx.get('expenses'),
                            tx.get('agreedRate'),
                            tx.get('movementType')
                        )

                        if not tx_exists:
                            cursor.execute(INSERT_INVESTMENT_TRANSACTION, tx_params)
                            logger.info(f"Inserindo transação {tx['id']} do investimento {inv['id']}")
                        else:
                            cursor.execute(UPDATE_INVESTMENT_TRANSACTION, tx_params[2:] + (tx['id'],))
                            logger.info(f"Atualizando transação {tx['id']} do investimento {inv['id']}")

                except Exception as e:
                    logger.error(f"Erro ao processar investimento {inv['id']}: {str(e)}")

            if inserted_count == 0:
                logger.info(f"INVESTMENTS - ItemID {item_id}: Nenhum novo investimento inserido.")
            else:
                logger.info(f"INVESTMENTS - ItemID {item_id}: {inserted_count} novo(s) investimento(s) inserido(s).")

        except Exception as e:
            logger.error(f"INVESTMENTS - Erro ao buscar investimentos para item_id {item_id}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("INVESTMENTS - Sincronização de investimentos concluída.")

if __name__ == "__main__":
    sync_investments()
