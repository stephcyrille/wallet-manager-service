from rest_framework import serializers
from .models import TokenOperation


class BaseOpSerializer(serializers.ModelSerializer):
    trx_ref = serializers.CharField(required=False)
    ops_type = serializers.CharField(required=True, min_length=4, max_length=14)
    from_wallet = serializers.CharField(required=False, max_length=23, min_length=23)
    to_wallet = serializers.CharField(required=True, max_length=23, min_length=23)
    id_blockchain = serializers.CharField(required=True, max_length=42, min_length=42)
    token_code = serializers.CharField(required=True, max_length=5, min_length=2)
    amount = serializers.DecimalField(required=True, max_digits=12, decimal_places=2)

    class Meta:
        model = TokenOperation
        exclude = ["id"]

    def validate(self, data):
        """
            From wallet and to wallet check the difference before validation
        """
        if "P2P_TRANSFER" == data['ops_type']:
            if "from_wallet" not in data:
                raise serializers.ValidationError("The origin wallet is mandatory")
            if data['from_wallet'] == data['to_wallet']:
                raise serializers.ValidationError("The origin wallet must be different to the destination wallet")
        else:
            if "from_wallet" in data and data['from_wallet'] == data['to_wallet']:
                raise serializers.ValidationError("The origin wallet must be different to the destination wallet")
        return data
