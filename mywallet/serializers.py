from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField
from .models import Wallet, EntityToken


class BaseWalletSerializer(serializers.ModelSerializer):
    owner_ref = serializers.CharField(required=True, max_length=36, min_length=36)
    fiat_amount = MoneyField(max_digits=14, decimal_places=2, required=False)

    class Meta:
        model = Wallet
        exclude = ["id"]


class WalletSerializer(serializers.ModelSerializer):
    fiat_amount = MoneyField(max_digits=14, decimal_places=2, required=False)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        exclude = ["id"]

    def get_tokens(self, instance):
        user_tokens = EntityToken.objects.filter(wallet_ref=instance.ref)
        return WalletEntityTokenSerializer(user_tokens, many=True).data


class ActivateTokenRequestSerializer(serializers.ModelSerializer):
    token_symbol = serializers.CharField(required=False)
    owner_ref = serializers.CharField(required=True, max_length=36, min_length=36)
    wallet_ref = serializers.CharField(required=True, max_length=23, min_length=23)
    token_ref = serializers.CharField(required=True, max_length=42, min_length=42)

    class Meta:
        model = EntityToken
        exclude = ["id"]


class EntityTokenSerializer(serializers.ModelSerializer):
    fiat_value = MoneyField(max_digits=14, decimal_places=2)
    amount = MoneyField(max_digits=14, decimal_places=2)

    class Meta:
        model = EntityToken
        exclude = ["id"]


class WalletEntityTokenSerializer(serializers.ModelSerializer):
    fiat_value = MoneyField(max_digits=14, decimal_places=2)

    class Meta:
        model = EntityToken
        fields = ["token_symbol", "token_ref", "amount", "fiat_value", "fiat_value_currency",
                  "is_active", "activated_date"]

