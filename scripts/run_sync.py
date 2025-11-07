from src.services.sync_items import sync_items
from src.services.sync_accounts import sync_accounts
from src.services.sync_transactions import sync_transactions
from src.services.sync_investments import sync_investments


if __name__ == "__main__":
    sync_items()
    sync_accounts()
    sync_transactions()
    sync_investments()
