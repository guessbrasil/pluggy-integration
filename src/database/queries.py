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


# INVESTMENTS
# --- INVESTIMENTOS ---
SELECT_INVESTMENTS = """
    SELECT investment_id, item_id, name, balance, type, subtype, date
    FROM pluggy_investments
"""
INSERT_INVESTMENT = """
    INSERT INTO pluggy_investments (
        investment_id, item_id, number, name, balance, currency_code, type, subtype,
        last_month_rate, last_twelve_months_rate, annual_rate, code, isin, metadata,
        value, quantity, amount, taxes, taxes2, date, owner, amount_profit, amount_withdrawal,
        amount_original, due_date, issuer, issuer_cnpj, issue_date, rate, rate_type,
        fixed_annual_rate, status, institution, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
UPDATE_INVESTMENT = """
    UPDATE pluggy_investments
    SET number = ?, name = ?, balance = ?, currency_code = ?, type = ?, subtype = ?,
        last_month_rate = ?, last_twelve_months_rate = ?, annual_rate = ?, code = ?, isin = ?, metadata = ?,
        value = ?, quantity = ?, amount = ?, taxes = ?, taxes2 = ?, date = ?, owner = ?, amount_profit = ?,
        amount_withdrawal = ?, amount_original = ?, due_date = ?, issuer = ?, issuer_cnpj = ?, issue_date = ?,
        rate = ?, rate_type = ?, fixed_annual_rate = ?, status = ?, institution = ?, updated_at = ?, created_at = ?
    WHERE investment_id = ?
"""

# --- TRANSACOES DE INVESTIMENTOS ---
SELECT_INVESTMENT_TRANSACTIONS = """
    SELECT transaction_id, investment_id, amount, date
    FROM pluggy_investment_transactions
"""
INSERT_INVESTMENT_TRANSACTION = """
    INSERT INTO pluggy_investment_transactions (
        transaction_id, investment_id, amount, description, value, quantity, trade_date, date,
        type, net_amount, brokerage_number, expenses, agreed_rate, movement_type
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
UPDATE_INVESTMENT_TRANSACTION = """
    UPDATE pluggy_investment_transactions
    SET amount = ?, description = ?, value = ?, quantity = ?, trade_date = ?, date = ?,
        type = ?, net_amount = ?, brokerage_number = ?, expenses = ?, agreed_rate = ?, movement_type = ?,
        updated_at = GETDATE()
    WHERE transaction_id = ?
"""