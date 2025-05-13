SELECT_ITEMS = """
    SELECT item_id, connector_name, connector_type, created_at, updated_at, status, execution_status, last_updated_at
    FROM pluggy_items
"""

INSERT_ITEM = """
    INSERT INTO pluggy_items (item_id, connector_name, connector_type, created_at, updated_at, status, execution_status, last_updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""


UPDATE_ITEM = """
    UPDATE pluggy_items
    SET connector_name = ?, connector_type = ?, status = ?, execution_status = ?, updated_at = GETDATE(), last_updated_at = GETDATE()
    WHERE item_id = ?
"""


SELECT_ACCOUNTS = """
    SELECT account_id, banco, agencia, conta, tipo, saldo, data_atualizacao, item_id, tax_number, company
    FROM pluggy_accounts
"""

INSERT_ACCOUNT = """
    INSERT INTO pluggy_accounts (account_id, banco, agencia, conta, tipo, saldo, data_atualizacao, item_id, tax_number, company)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

UPDATE_ACCOUNT = """
    UPDATE pluggy_accounts
    SET banco = ?, agencia = ?, conta = ?, tipo = ?, saldo = ?, data_atualizacao = ?, tax_number = ?, company = ?
    WHERE account_id = ?;
"""

SELECT_TRANSACTIONS = """
    SELECT *
    FROM pluggy_transactions
    WHERE data BETWEEN ? AND ?
"""

INSERT_TRANSACTION = """
    INSERT INTO pluggy_transactions (
        transaction_id, account_id, description, currency_code, debit, credit, date, category, balance,
        provider_code, status, type, payer_name, payer_cnpj, receiver_name, receiver_cnpj,
        merchant_name, merchant_cnpj, merchant_cnae, payment_method, reference_number, digitable_line,
        base_amount, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


UPDATE_TRANSACTION = """
    UPDATE pluggy_transactions
    SET debit = ?, credit = ?, status = ?, updated_at = GETDATE()
    WHERE transaction_id = ?
"""


