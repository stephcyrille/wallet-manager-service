from operations.models import WalletOperation


def save(data):
    data = {
        "ops_type": data.get("ops_type"),
        "from_wallet": data.get("from_wallet"),
        "to_wallet": data.get("to_wallet"),
        "id_blockchain": data.get("id_blockchain") or " ",
        "token_code": data.get("token_code") or " ",
        "amount": data.get("amount"),
        "to_external_wallet": data.get("to_external_wallet") or " ",
    }
    operation = WalletOperation.objects.create(**data)
    return operation

