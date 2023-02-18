import uuid
from decouple import config
from django.utils import timezone
from wallet.models import Token, Wallet, EntityToken
from rest_framework.test import APITestCase
from rest_framework import status


class TokenOperationApiTest(APITestCase):
    def setUp(self):
        # =========================================================================================================
        # ================================== We are set up all wallet here ========================================
        # =========================================================================================================
        self.system_from_wallet = Wallet.objects.create(**{
            "ref": "%s%s" % (config("WALLET_DEBIT_2", default=''), config("WALLET_CLIENT_DEBIT_CODE", default='')),
            "code_client": config("WALLET_CLIENT_DEBIT_CODE", default=''),
            "owner_ref": config("WALLET_DEBIT_2_USER", default=''),
            "is_active": True,
            "fiat_amount": 100000000.0,
            "activated_date": timezone.now(),
        })
        self.system_to_wallet = Wallet.objects.create(**{
            "ref": "%s%s" % (config("WALLET_CREDIT_2", default=''), config("WALLET_CLIENT_CREDIT_CODE", default='')),
            "code_client": config("WALLET_CLIENT_CREDIT_CODE", default=''),
            "owner_ref": config("WALLET_CREDIT_2_USER", default=''),
            "is_active": True,
            "fiat_amount": 0.0,
            "activated_date": timezone.now(),
        })

        self.to_user_wallet = Wallet.objects.create(**{
            "ref": "W%sY%sE%s1111" % (str(uuid.uuid4()).split('-')[0], str(uuid.uuid4()).split('-')[1],
                                      str(uuid.uuid4()).split('-')[2]),
            "code_client": "1111",
            "owner_ref": "288391f6-f94a-4dd1-8708-36e4d6a058ca",
            "is_active": True,
            "fiat_amount": 0.0,
            "activated_date": timezone.now(),
        })

        self.sender_wallet = Wallet.objects.create(**{
            "ref": "W%sY%sE%s1111" % (str(uuid.uuid4()).split('-')[0], str(uuid.uuid4()).split('-')[1],
                                      str(uuid.uuid4()).split('-')[2]),
            "code_client": "1111",
            "owner_ref": "8a840bdd-fec4-4878-a00d-7102a75b88d2",
            "is_active": True,
            "fiat_amount": 100000.0,
            "activated_date": timezone.now(),
        })

        # =========================================================================================================
        # ======================================== We are set up Tokens ===========================================
        # =========================================================================================================
        self.token = Token.objects.create(**{
            "name": "Bitcoin",
            "symbol": "BTC",
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "unit_price": 21876.80,
        })

        # System entity token
        self.system_from_e_token = EntityToken.objects.create(**{
            "token_symbol": self.token.symbol,
            "token_ref": self.token.ref,
            "wallet_ref": self.system_from_wallet.ref,
            "owner_ref": config("WALLET_DEBIT_2_USER", default=''),
            "amount": 1000000,
            "fiat_value": self.token.unit_price * 1000000,
            "is_active": True,
            "activated_date": timezone.now(),
        })
        self.system_to_e_token = EntityToken.objects.create(**{
            "token_symbol": self.token.symbol,
            "token_ref": self.token.ref,
            "wallet_ref": self.system_to_wallet.ref,
            "owner_ref": config("WALLET_CREDIT_2_USER", default=''),
            "amount": 0,
            "fiat_value": self.token.unit_price * 1000000,
            "is_active": True,
            "activated_date": timezone.now(),
        })

        # Client user entity token
        self.user_e_token = EntityToken.objects.create(**{
            "token_symbol": self.token.symbol,
            "token_ref": self.token.ref,
            "wallet_ref": self.to_user_wallet.ref,
            "owner_ref": "288391f6-f94a-4dd1-8708-36e4d6a058ca",
            "amount": 0,
            "fiat_value": self.token.unit_price * 1000000,
            "is_active": True,
            "activated_date": timezone.now(),
        })
        # Client user entity token
        self.sender_e_token = EntityToken.objects.create(**{
            "token_symbol": self.token.symbol,
            "token_ref": self.token.ref,
            "wallet_ref": self.sender_wallet.ref,
            "owner_ref": "8a840bdd-fec4-4878-a00d-7102a75b88d2",
            "amount": 10000,
            "fiat_value": self.token.unit_price * 1000000,
            "is_active": True,
            "activated_date": timezone.now(),
        })

        # =========================================================================================================
        # ======================================= Create request Payload ==========================================
        # =========================================================================================================
        self.data_topup = {
            "ops_type": "TOP_UP",
            "from_wallet": self.system_from_wallet.ref,
            "to_wallet": self.to_user_wallet.ref,
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "token_code": "BTC",
            "amount": 125.00,
            "payment": {
                "name": "OM",
                "operator": "MOMO",
                "phone_number": "0640509688",
            }
        }
        self.data_wire = {
            "ops_type": "WIRE_TRANSFER",
            "from_wallet": self.sender_wallet.ref,
            "to_wallet": self.to_user_wallet.ref,
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "token_code": "BTC",
            "amount": 125.00,
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
            "ops_type": "WITHDRAW",
            "from_wallet": self.sender_wallet.ref,
            "to_wallet": self.system_to_wallet.ref,
            "to_external_wallet": "0x4710B608CEE3B7662606793B140F5CA553F8DE4C",
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "token_code": "BTC",
            "amount": 125.00,
            "payment": {
                "operator": "MOMO",
                "name": "MTNMOMO",
                "phone_number": "0640509688",
                "reason": "ID-TRX1205",
            }
        }

    def test_token_topup(self):
        url = "/apis/v1/operations/token/topup/"
        response = self.client.post(url, self.data_topup, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_wire_transfer(self):
        url = "/apis/v1/operations/token/wire-transfer/"
        response = self.client.post(url, self.data_wire, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_withdraw(self):
        url = "/apis/v1/operations/token/withdraw/"
        response = self.client.post(url, self.data_withdraw, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

