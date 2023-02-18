from wallet.models import EntityToken, Wallet


def get_entity_token_object(ref, token_code):
    try:
        return EntityToken.objects.get(wallet_ref=ref, token_symbol=token_code)
    except EntityToken.DoesNotExist:
        return ""


def get_wallet_object(ref):
    try:
        return Wallet.objects.get(ref=ref)
    except Wallet.DoesNotExist:
        return ""


