import uuid
from decouple import config
from django.utils import timezone
from mywallet.models import Token, Wallet
from rest_framework.test import APITestCase
from rest_framework import status


class FiatOperationApiTest(APITestCase):
    def setUp(self):
        wallet_param_d1 = {
            "ref": "%s%s" % (config("WALLET_DEBIT_1", default=''), config("WALLET_CLIENT_DEBIT_CODE", default='')),
            "code_client": config("WALLET_CLIENT_DEBIT_CODE", default=''),
            "owner_ref": config("WALLET_DEBIT_1_USER", default=''),
            "is_active": True,
            "fiat_amount": 100000000.0,
            "activated_date": timezone.now(),
        }
        self.from_system_wallet = Wallet.objects.create(**wallet_param_d1)

        wallet_param_c1 = {
            "ref": "%s%s" % (config("WALLET_CREDIT_1", default=''), config("WALLET_CLIENT_CREDIT_CODE", default='')),
            "code_client": config("WALLET_CLIENT_CREDIT_CODE", default=''),
            "owner_ref": config("WALLET_CREDIT_1_USER", default=''),
            "is_active": True,
            "fiat_amount": 0.0,
            "activated_date": timezone.now(),
        }
        self.to_system_wallet = Wallet.objects.create(**wallet_param_c1)

        owner_ref_1 = "1675f851-e244-4f9d-b3f0-7fbc6288d521",
        ref_1 = "W%sY%sE%s1111" % (str(uuid.uuid4()).split('-')[0], str(uuid.uuid4()).split('-')[1],
                                   str(uuid.uuid4()).split('-')[2])
        owner_ref_2 = "288391f6-f94a-4dd1-8708-36e4d6a058ca",
        ref_2 = "W%sY%sE%s1111" % (str(uuid.uuid4()).split('-')[0], str(uuid.uuid4()).split('-')[1],
                                   str(uuid.uuid4()).split('-')[2])
        # TODO Activate the wallet before use it (Maybe by creating an activate model method)
        self.to_wallet = Wallet.objects.create(**{"owner_ref": owner_ref_1, "ref": ref_1})
        self.from_wallet = Wallet.objects.create(**{"owner_ref": owner_ref_2, "ref": ref_2, "fiat_amount": 1000000})

        self.data_topup = {
            "ops_type": "FIAT_TOP_UP",
            "from_wallet": self.from_system_wallet.ref,
            "to_wallet": self.to_wallet.ref,
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "token_code": "FIAT",
            "amount": 1218760.80,
            "payment": {
                "name": "OM",
                "operator": "MOMO",
                "phone_number": "0640509688",
            }
        }

        self.data_wire = {
            "ops_type": "FIAT_WIRE_TRANSFER",
            "from_wallet": self.from_wallet.ref,
            "to_wallet": self.to_wallet.ref,
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "token_code": "FIAT",
            "amount": 21876.80,
            "payment": {
                "operator": "BANK",
                "name": "VISA",
                "card_number": "0640509688841214",
                "card_CVV": "521",
                "card_owner": "John Doe",
                "card_expiry_date": "10/28",
            }
        }

        self.data_withdraw = {
            "ops_type": "FIAT_WITHDRAW",
            "from_wallet": self.from_wallet.ref,
            "to_wallet": self.to_system_wallet.ref,
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "token_code": "FIAT",
            "amount": 218276.80,
            "payment": {
                "operator": "MOMO",
                "name": "MTNMOMO",
                "phone_number": "0640509688",
                "reason": "ID-TRX1205",
            }
        }

    def test_fiat_topup(self):
        url = "/apis/v1/operations/fiat/topup/"
        response = self.client.post(url, self.data_topup, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fiat_wire_transfer(self):
        url = "/apis/v1/operations/fiat/wire-transfer/"
        response = self.client.post(url, self.data_wire, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fiat_withdraw(self):
        url = "/apis/v1/operations/fiat/withdraw/"
        response = self.client.post(url, self.data_withdraw, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
