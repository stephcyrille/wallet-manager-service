from wallet.models import Blockchain


def generate_tokens():
    token_1 = {
        "name": "US Dollar",
        "symbol": "FIAT",
        "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
        "unit_price": 1.0,
    }

    token_2 = {
        "name": "Real Money System",
        "symbol": "FIAT",
        "id_blockchain": "US Dollar",
        "unit_price": "Real Money System Network",
    }

    token_3 = {
        "name": "Real Money System",
        "symbol": "FIAT",
        "id_blockchain": "US Dollar",
        "unit_price": "Real Money System Network",
    }

    token_4 = {
        "name": "Real Money System",
        "symbol": "FIAT",
        "id_blockchain": "US Dollar",
        "unit_price": "Real Money System Network",
    }

    try:
        Blockchain.objects.create(**bc_1)
        Blockchain.objects.create(**bc_2)
        Blockchain.objects.create(**bc_3)
        Blockchain.objects.create(**bc_4)
        print("The 4th bases Blockchain was created successfully!!")
    except Exception as e:
        print("An error occurred: %s" % e.__str__())