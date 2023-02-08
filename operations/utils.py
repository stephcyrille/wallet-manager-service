from mywallet.models import EntityToken, Wallet
from .models import WalletOperation


def get_entity_token_object(ref, token_code):
    try:
        return EntityToken.objects.get(wallet_ref=ref, token_symbol=token_code)
    except EntityToken.DoesNotExist:
        return ""


def move_token(origin, destination, amount):
    if origin.amount >= amount:
        origin.amount -= amount
        destination.amount += amount
        origin.save()
        destination.save()
        return True
    else:
        return False


def save_operation(data):
    data = {
        "ops_type": data.get("ops_type"),
        "from_wallet": data.get("from_wallet"),
        "to_wallet": data.get("to_wallet"),
        "id_blockchain": data.get("id_blockchain"),
        "token_code": data.get("token_code"),
        "amount": data.get("amount"),
        "to_external_wallet": data.get("to_external_wallet") or " ",
    }
    operation = WalletOperation.objects.create(**data)
    return operation


def get_wallet_object(ref):
    try:
        return Wallet.objects.get(ref=ref)
    except Wallet.DoesNotExist:
        return ""


def move_fiat(origin, destination, amount):
    if origin.fiat_amount >= amount:
        origin.fiat_amount -= amount
        destination.fiat_amount += amount
        origin.save()
        destination.save()
        return True
    else:
        return False

