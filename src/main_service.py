# src/main.py
from src.services import sync_items, sync_accounts, sync_transactions

def main():
    print("Sincronizando itens...")
    sync_items.sync_items()

    print("Sincronizando contas...")
    sync_accounts.sync_accounts()

    print("Sincronizando transações...")
    sync_transactions.sync_transactions()

if __name__ == "__main__":
    main()
