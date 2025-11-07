import requests
import os
import json
from dotenv import load_dotenv
from src.utils.logger import logger

load_dotenv()

PLUGGY_CLIENT_ID = os.getenv("PLUGGY_CLIENT_ID")
PLUGGY_CLIENT_SECRET = os.getenv("PLUGGY_CLIENT_SECRET")
PLUGGY_BASE_URL = "https://api.pluggy.ai"

# Carrega os ITEM_IDS de forma segura
def get_all_item_ids():
    item_ids = os.getenv("ITEM_IDS_HRG3", "").replace(" ", "").split(",") + \
               os.getenv("ITEM_IDS_VARTEX", "").replace(" ", "").split(",") + \
               os.getenv("ITEM_IDS_GUESS", "").replace(" ", "").split(",")
    return [item for item in item_ids if item]

item_ids = get_all_item_ids()

# Autenticação
def get_api_key():
    url = f"{PLUGGY_BASE_URL}/auth"
    headers = {"accept": "application/json", "content-type": "application/json"}
    payload = {"clientId": PLUGGY_CLIENT_ID, "clientSecret": PLUGGY_CLIENT_SECRET}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("apiKey")
    except Exception as e:
        logger.error(f"Erro ao autenticar na Pluggy: {e}")
        return None

api_key = get_api_key()
if not api_key:
    logger.error("Não foi possível obter a API Key.")
    exit()

# Safe getter para JSON aninhado
def safe_get(data, *keys):
    for key in keys:
        if not isinstance(data, dict):
            return None
        data = data.get(key)
    return data

# Busca identidade (tax_number e company)
def get_identity(item_id):
    url = f"{PLUGGY_BASE_URL}/identity?itemId={item_id}"
    headers = {"X-API-KEY": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "tax_number": data.get("taxNumber", "Desconhecido"),
            "company": data.get("companyName", "Desconhecido")
        }
    except Exception as e:
        logger.error(f"Erro ao buscar identidade para item {item_id}: {e}")
        return {"tax_number": "Desconhecido", "company": "Desconhecido"}

# Busca metadados dos itens
def get_items():
    all_items = []

    for item_id in item_ids:
        url = f"{PLUGGY_BASE_URL}/items/{item_id}"
        headers = {"X-API-KEY": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            item = response.json()

            if item:
                all_items.append({
                    'item_id': item.get('id'),
                    'connector_name': item.get('connector', {}).get('name'),
                    'connector_type': item.get('connector', {}).get('type'),
                    'created_at': item.get('createdAt'),
                    'updated_at': item.get('updatedAt'),
                    'status': item.get('status'),
                    'execution_status': item.get('executionStatus'),
                    'last_updated_at': item.get('lastUpdatedAt')
                })
        except Exception as e:
            logger.error(f"Erro ao buscar item {item_id}: {e}")
    return all_items

# Busca contas bancárias por item
def get_accounts():
    all_accounts = []

    for item_id in item_ids:
        url = f"{PLUGGY_BASE_URL}/accounts?itemId={item_id}"
        headers = {"X-API-KEY": api_key}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            accounts = response.json().get("results", [])

            if accounts:
                logger.info(f"Encontradas {len(accounts)} contas para o item {item_id}.")
                all_accounts.extend(accounts)
            else:
                logger.warning(f"Nenhuma conta encontrada para o item {item_id}.")
        except Exception as e:
            logger.error(f"Erro ao buscar contas para o item {item_id}: {e}")
    
    return all_accounts


def get_investments(item_id):
    url = f"{PLUGGY_BASE_URL}/investments"
    headers = {"X-API-KEY": api_key}
    params = {"itemId": item_id}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get("results", [])
        logger.info(f"[{item_id}] Total de investimentos: {len(data)}")
        return data
    except Exception as e:
        logger.error(f"[{item_id}] Erro ao buscar investimentos: {e}")
        return []



def get_investment_transactions(investment_id, page_size=500):
    url = f"{PLUGGY_BASE_URL}/investments/{investment_id}/transactions"  
    headers = {"X-API-KEY": api_key}
    params = {"pageSize": page_size, "page": 1}

    transactions = []

    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if not results:
                break

            transactions.extend(results)
            if len(results) < page_size:
                break

            params["page"] += 1
        except Exception as e:
            logger.error(f"[{investment_id}] Erro ao buscar transações de investimento: {e}")
            break

    logger.info(f"[{investment_id}] Total de transações de investimento: {len(transactions)}")
    return transactions



def get_transactions(account_id, start_date="2012-01-01", end_date="2025-08-18", page_size=500):
    url = f"{PLUGGY_BASE_URL}/transactions"
    headers = {"X-API-KEY": api_key}
    params = {
        "accountId": account_id,
        "pageSize": page_size,
        "page": 1,
        "from": start_date,
        "to": end_date
    }

    transactions = []

    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if not results:
                break

            transactions.extend(results)
            if len(results) < page_size:
                break

            params["page"] += 1
        except Exception as e:
            logger.error(f"[{account_id}] Erro ao buscar transações: {e}")
            break

    logger.info(f"AccountID: {account_id}. Total de transações: {len(transactions)}.")
    return format_transactions(transactions, account_id)


def format_transactions(transactions, account_id):
    formatted = []

    for i, transaction in enumerate(transactions):
        try:
            formatted.append({
                "id": transaction.get("id"),
                "accountId": transaction.get("accountId"),
                "description": transaction.get("description"),
                "currencyCode": transaction.get("currencyCode"),
                "amount": transaction.get("amount"),
                "balance": transaction.get("balance"),
                "date": transaction.get("date"),
                "category": transaction.get("category"),
                "providerCode": transaction.get("providerCode"),
                "status": transaction.get("status"),
                "type": transaction.get("type"),
                "paymentMethod": safe_get(transaction, "paymentData", "paymentMethod"),
                "referenceNumber": safe_get(transaction, "paymentData", "referenceNumber"),
                "digitableLine": safe_get(transaction, "paymentData", "boletoMetadata", "digitableLine"),
                "baseAmount": safe_get(transaction, "paymentData", "boletoMetadata", "baseAmount"),
                "payerName": safe_get(transaction, "paymentData", "payer", "name"),
                "payerCnpj": safe_get(transaction, "paymentData", "payer", "documentNumber", "value"),
                "receiverName": safe_get(transaction, "paymentData", "receiver", "name"),
                "receiverCnpj": safe_get(transaction, "paymentData", "receiver", "documentNumber", "value"),
                "merchantName": safe_get(transaction, "merchant", "businessName"),
                "merchantCnpj": safe_get(transaction, "merchant", "cnpj"),
                "merchantCnae": safe_get(transaction, "merchant", "cnae"),
                "createdAt": transaction.get("createdAt"),
                "updatedAt": transaction.get("updatedAt")
            })
        except Exception as e:
            logger.error(f"[{account_id}] Erro ao processar transação #{i}: {e}")
            logger.error(f"Transação com erro: {json.dumps(transaction, indent=2, ensure_ascii=False)}")

    return formatted
