import uuid
from mywallet.models import Token, Wallet
from rest_framework.test import APITestCase
from rest_framework import status


class CreateWalletApiTest(APITestCase):
    def setUp(self):
        self.data = {"owner_ref": "1675f851-e244-4f9d-b3f0-7fbc6288d521"}

    def test_create_wallet(self):
        url = "/apis/v1/wallet/create/"
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Wallet.objects.count(), 1)


class WalletApiTest(APITestCase):
    def setUp(self):
        self.data = {"owner_ref": "1675f851-e244-4f9d-b3f0-7fbc6288d521"}
        self.wallet = Wallet.objects.create(**self.data)

    def test_get_wallet(self):
        url = "/apis/v1/wallet/detail/%s" % self.wallet.owner_ref
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_wallet(self):
        url = "/apis/v1/wallet/activate/"
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


class TokenApiTest(APITestCase):
    def setUp(self):
        value = {
            "name": "Bitcoin",
            "symbol": "BTC",
            "id_blockchain": "CHAIN-bd91a052-2e9f-43af-95e8-73ca2e494d2b",
            "unit_price": 21876.80,
        }
        ref = "W%sY%sE%s1111" % (str(uuid.uuid4()).split('-')[0], str(uuid.uuid4()).split('-')[1],
                                 str(uuid.uuid4()).split('-')[2])
        self.token = Token.objects.create(**value)
        self.data = {
            "owner_ref": "1675f851-e244-4f9d-b3f0-7fbc6288d521",
            "wallet_ref": ref,
            "token_ref": self.token.ref
        }
        self.wallet = Wallet.objects.create(**{"owner_ref": self.data["owner_ref"], "ref": ref})

    def test_activate_token(self):
        url = "/apis/v1/wallet/token/activate/"
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)





