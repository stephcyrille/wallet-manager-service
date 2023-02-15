from decouple import config
from django.utils import timezone
from mywallet.models import Wallet


def generate_wallet():
    wallet_param_c1 = {
        "ref": "%s%s" % (config("WALLET_CREDIT_1", default=''), config("WALLET_CLIENT_CREDIT_CODE", default='')),
        "code_client": config("WALLET_CLIENT_CREDIT_CODE", default=''),
        "owner_ref": config("WALLET_CREDIT_1_USER", default=''),
        "is_active": True,
        "fiat_amount": 0.0,
        "activated_date": timezone.now(),
    }

    wallet_param_c2 = {
        "ref": "%s%s" % (config("WALLET_CREDIT_2", default=''), config("WALLET_CLIENT_CREDIT_CODE", default='')),
        "code_client": config("WALLET_CLIENT_CREDIT_CODE", default=''),
        "owner_ref": config("WALLET_CREDIT_2_USER", default=''),
        "is_active": True,
        "fiat_amount": 0.0,
        "activated_date": timezone.now(),
    }

    wallet_param_d1 = {
        "ref": "%s%s" % (config("WALLET_DEBIT_1", default=''), config("WALLET_CLIENT_DEBIT_CODE", default='')),
        "code_client": config("WALLET_CLIENT_DEBIT_CODE", default=''),
        "owner_ref": config("WALLET_DEBIT_1_USER", default=''),
        "is_active": True,
        "fiat_amount": 100000000.0,
        "activated_date": timezone.now(),
    }

    wallet_param_d2 = {
        "ref": "%s%s" % (config("WALLET_DEBIT_2", default=''), config("WALLET_CLIENT_DEBIT_CODE", default='')),
        "code_client": config("WALLET_CLIENT_DEBIT_CODE", default=''),
        "owner_ref": config("WALLET_DEBIT_2_USER", default=''),
        "is_active": True,
        "fiat_amount": 100000000.0,
        "activated_date": timezone.now(),
    }

    # TODO Activate all the wallet before use it (Maybe by creating an activate model method)
    try:
        Wallet.objects.create(**wallet_param_c1)
        Wallet.objects.create(**wallet_param_c2)
        Wallet.objects.create(**wallet_param_d1)
        Wallet.objects.create(**wallet_param_d2)
        print("The 4th bases wallets was created successfully!!")
    except Exception as e:
        print("An error occurred: %s" % e.__str__())

    # TODO Create entity token Wallet for each changed token
