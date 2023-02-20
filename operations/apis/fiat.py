from decouple import config

from operations.serializers import BaseOpSerializer, PaymentMethodSerializer, WithdrawOpSerializer
from operations.utilities.ops_manager import save

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wallet.utilities.account_manager import move_fiat
from wallet.utilities.cursor import get_wallet_object


class FiatTopUpOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check serializer for payment
            p_serializer = PaymentMethodSerializer(data=request.data.get("payment"))
            if not p_serializer.is_valid():
                return Response(p_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # An internal debit wallet
            if serializer.data.get("from_wallet"):
                from_wallet = get_wallet_object(serializer.data.get("from_wallet"))
            else:
                from_wallet = get_wallet_object(config("WALLET_DEBIT_1", default=''))
            to_wallet = get_wallet_object(serializer.data.get("to_wallet"))

            if "FIAT_TOP_UP" == serializer.data.get("ops_type"):
                if from_wallet:
                    amount = serializer.data.get("amount")
                    # TODO call the payment external API depending on the operator key in payment serializer
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_fiat(from_wallet, to_wallet, amount)
                    # TODO Add a callback to listen when this operation is over et get the status, the proceed...
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    save(serializer.data)
                    response = {
                        "message": "Success",
                        "operation": "FIAT_TOP_UP"
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected Top up operation"}, status=status.HTTP_400_BAD_REQUEST)


class FiatWireTransferOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check serializer for payment
            p_serializer = PaymentMethodSerializer(data=request.data.get("payment"))
            if not p_serializer.is_valid():
                return Response(p_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Get from wallet in the posted values
            from_wallet = get_wallet_object(serializer.data.get("from_wallet"))
            to_wallet = get_wallet_object(serializer.data.get("to_wallet"))

            if "FIAT_WIRE_TRANSFER" == serializer.data.get("ops_type"):
                if from_wallet:
                    amount = serializer.data.get("amount")
                    # TODO call the payment external API here depending on the payment operator
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_fiat(from_wallet, to_wallet, amount)
                    # TODO Add a callback to listen when this operation is over et get the status, the proceed...
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    save(serializer.data)
                    response = {
                        "message": "Success",
                        "operation": "FIAT_WIRE_TRANSFER"
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected wire transfer operation"}, status=status.HTTP_400_BAD_REQUEST)


class FiatWithdrawOperationView(APIView):
    def post(self, request):
        serializer = WithdrawOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # TODO Create a custom serializer for payment output
            # Check serializer for payment
            # p_serializer = PaymentMethodSerializer(data=request.data.get("payment"))
            # if not p_serializer.is_valid():
            #     return Response(p_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Get from token wallet inside the request payload
            from_wallet = get_wallet_object(serializer.data.get("from_wallet"))
            if serializer.data.get("to_wallet"):
                to_wallet = get_wallet_object(serializer.data.get("to_wallet"))
            else:
                # An internal credit wallet
                to_wallet = get_wallet_object(config("WALLET_CREDIT_1", default=''))
            if "FIAT_WITHDRAW" == serializer.data.get("ops_type"):
                if to_wallet:
                    amount = serializer.data.get("amount")
                    # TODO call the payment external API here depending on the payment operator
                    # Move amount from origin entity wallet to the destination entity wallet
                    make_ops = move_fiat(from_wallet, to_wallet, amount)
                    # TODO Add a callback to listen when this operation is over et get the status, the proceed...
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # TODO create a task for an external API for withdrawal (we need to add mobile money or bank API)
                    save(serializer.data)
                    response = {
                        "message": "Success",
                        "operation": "FIAT_WITHDRAW"
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a Withdraw Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a Withdraw operation"}, status=status.HTTP_400_BAD_REQUEST)

