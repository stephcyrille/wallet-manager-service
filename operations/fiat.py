from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseOpSerializer, WithdrawOpSerializer
from .utils import *


class FiatTopUpOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # An internal debit wallet
            from_wallet = get_wallet_object(config("WALLET_DEBIT_1", default=''))
            to_wallet = get_wallet_object(serializer.data.get("to_wallet"))

            if "FIAT_TOP_UP" == serializer.data.get("ops_type"):
                if from_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_fiat(from_wallet, to_wallet, serializer.data.get("amount"))
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = save_operation(serializer.data)
                    response_serializer = BaseOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected Top up operation"}, status=status.HTTP_400_BAD_REQUEST)


class FiatWireTransferOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get entity token objects
            # Get from wallet in the posted values
            from_wallet = get_wallet_object(serializer.data.get("from_wallet"))
            to_wallet = get_wallet_object(serializer.data.get("to_wallet"))

            if "FIAT_WIRE_TRANSFER" == serializer.data.get("ops_type"):
                if from_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_fiat(from_wallet, to_wallet, serializer.data.get("amount"))
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = save_operation(serializer.data)
                    response_serializer = BaseOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected Top up operation"}, status=status.HTTP_400_BAD_REQUEST)


class FiatWithdrawOperationView(APIView):
    def post(self, request):
        serializer = WithdrawOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get from token wallet inside the request payload
            from_wallet = get_wallet_object(serializer.data.get("from_wallet"))
            # An internal credit wallet
            to_wallet = get_wallet_object(config("WALLET_CREDIT_1", default=''))
            if "FIAT_WITHDRAW" == serializer.data.get("ops_type"):
                if to_wallet:
                    # Move amount from origin entity wallet to the destination entity wallet
                    make_ops = move_fiat(from_wallet, to_wallet,
                                         serializer.data.get("amount"))
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # TODO create a task for an external API for withdrawal (we need to add mobile money or bank API)
                    operation = save_operation(serializer.data)
                    response_serializer = WithdrawOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a Withdraw Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a Withdraw operation"}, status=status.HTTP_400_BAD_REQUEST)

