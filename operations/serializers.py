from rest_framework import serializers


class PaymentMethodSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=2, max_length=50)
    operator = serializers.CharField(required=True, min_length=4, max_length=18)
    reason = serializers.CharField(required=False)
    card_number = serializers.CharField(required=False, max_length=16, min_length=16)
    card_CVV = serializers.CharField(required=False, max_length=3, min_length=3)
    card_owner = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    card_expiry_date = serializers.CharField(required=False, max_length=5, min_length=5)

    def create(self):
        return ""

    def update(self):
        return ""

    def validate(self, data):
        """
            From wallet and to wallet check the difference before validation
        """
        if "MOMO" == data['operator']:
            if "phone_number" not in data:
                raise serializers.ValidationError("The phone number field is mandatory")
            if "MTNMOMO" == data['name'] and "reason" not in data:
                raise serializers.ValidationError("The reason of the transaction is mandatory")
        elif "BANK" == data['operator']:
            if "card_number" not in data:
                raise serializers.ValidationError("The card number field is mandatory")
            elif "card_CVV" not in data:
                raise serializers.ValidationError("The card CVV field is mandatory")
            elif "card_owner" not in data:
                raise serializers.ValidationError("The card owner field is mandatory")
            elif "card_expiry_date" not in data:
                raise serializers.ValidationError("The card expiry date field is mandatory")
        else:
            raise serializers.ValidationError("The operator field got a wrong key")
        return data


class BaseOpSerializer(serializers.Serializer):
    trx_ref = serializers.CharField(required=False)
    ops_type = serializers.CharField(required=True, min_length=4, max_length=18)
    from_wallet = serializers.CharField(required=False, max_length=23, min_length=23)
    to_wallet = serializers.CharField(required=True, max_length=23, min_length=23)
    id_blockchain = serializers.CharField(required=True, max_length=42, min_length=42)
    token_code = serializers.CharField(required=True, max_length=5, min_length=2)
    amount = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)

    def create(self):
        return ""

    def update(self):
        return ""

    def validate(self, data):
        """
            From wallet and to wallet check the difference before validation
        """
        if "WIRE_TRANSFER" == data['ops_type'] or "FIAT_WIRE_TRANSFER" == data['ops_type']:
            if "from_wallet" not in data:
                raise serializers.ValidationError("The origin wallet is mandatory")
            if data['from_wallet'] == data['to_wallet']:
                raise serializers.ValidationError("The origin wallet must be different to the destination wallet")
        else:
            if "from_wallet" in data and data['from_wallet'] == data['to_wallet']:
                raise serializers.ValidationError("The origin wallet must be different to the destination wallet")
        return data


class WithdrawOpSerializer(serializers.Serializer):
    trx_ref = serializers.CharField(required=False)
    ops_type = serializers.CharField(required=True, min_length=4, max_length=18)
    from_wallet = serializers.CharField(required=False, max_length=23, min_length=23)
    to_wallet = serializers.CharField(required=False, max_length=23, min_length=23)
    to_external_wallet = serializers.CharField(required=False, max_length=42, min_length=42)
    id_blockchain = serializers.CharField(required=True, max_length=42, min_length=42)
    token_code = serializers.CharField(required=True, max_length=5, min_length=2)
    amount = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)

    def create(self):
        return ""

    def update(self):
        return ""

    def validate(self, data):
        if "WITHDRAW" == data['ops_type']:
            if "to_external_wallet" not in data:
                raise serializers.ValidationError("The customer destination wallet (to_external_wallet) is mandatory")
            elif "from_wallet" not in data:
                raise serializers.ValidationError("The origin (from_wallet) wallet is mandatory")
        elif "FIAT_WITHDRAW" == data['ops_type']:
            if "from_wallet" not in data:
                raise serializers.ValidationError("The origin (from_wallet) wallet is mandatory")
            if not "FIAT" == data["token_code"]:
                raise serializers.ValidationError("(token_code) Not good token code")
        return data
