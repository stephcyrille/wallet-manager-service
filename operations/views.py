from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TokenOperation
from .serializers import BaseOpSerializer
from mywallet.models import EntityToken


class TopUpOperationView(APIView):
    def get_entity_token_object(self, ref):
        try:
            return EntityToken.objects.get(wallet_ref=ref)
        except EntityToken.DoesNotExist:
            return ""

    def topup_entity_wallet(self, origin, destination, amount):
        if origin.amount >= amount:
            origin.amount -= amount
            destination.amount += amount
            origin.save()
            destination.save()
            return True
        else:
            return False

    def save_operation(self, data):
        data = {
            "ops_type": data.get("ops_type"),
            "from_wallet": data.get("from_wallet"),
            "to_wallet": data.get("to_wallet"),
            "id_blockchain": data.get("id_blockchain"),
            "token_code": data.get("token_code"),
            "amount": data.get("amount"),
        }
        operation = TokenOperation.objects.create(**data)
        return operation

    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get entity token objects
            from_token_wallet = self.get_entity_token_object(serializer.data.get("from_wallet"))
            to_token_wallet = self.get_entity_token_object(serializer.data.get("to_wallet"))

            if "TOP_UP" == serializer.data.get("ops_type"):
                if from_token_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = self.topup_entity_wallet(from_token_wallet, to_token_wallet,
                                                        serializer.data.get("amount"))
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = self.save_operation(serializer.data)
                    response_serializer = BaseOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected Top up operation"}, status=status.HTTP_400_BAD_REQUEST)
