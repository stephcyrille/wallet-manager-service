from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from operations.utilities.ops_manager import save
from operations.serializers import BaseOpSerializer, PaymentMethodSerializer, WithdrawOpSerializer
from wallet.utilities.account_manager import move_token
from wallet.utilities.cursor import get_entity_token_object


# TODO Add a key to specify if buy offer, sale offer etc.
class TokenTopUpOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check serializer for payment
            p_serializer = PaymentMethodSerializer(data=request.data.get("payment"))
            if not p_serializer.is_valid():
                return Response(p_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # An internal debit token wallet
            if serializer.data.get("from_wallet"):
                from_token_wallet = get_entity_token_object(serializer.data.get("from_wallet"),
                                                            serializer.data.get("token_code"))
            else:
                from_token_wallet = get_entity_token_object(config("WALLET_DEBIT_2", default=''),
                                                            serializer.data.get("token_code"))
            to_token_wallet = get_entity_token_object(serializer.data.get("to_wallet"),
                                                      serializer.data.get("token_code"))

            if "TOP_UP" == serializer.data.get("ops_type"):
                if from_token_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    # TODO Here will be the start point of our trading service
                    make_ops = move_token(from_token_wallet, to_token_wallet,
                                          serializer.data.get("amount"))
                    # TODO Add a callback to listen when this operation is over et get the status, the proceed...
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = save(serializer.data)
                    response_serializer = BaseOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a Top up operation"}, status=status.HTTP_400_BAD_REQUEST)


class TokenWireTransferOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Check serializer for payment
            p_serializer = PaymentMethodSerializer(data=request.data.get("payment"))
            if not p_serializer.is_valid():
                return Response(p_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Get entity token objects
            # Get from wallet in the posted values
            from_token_wallet = get_entity_token_object(serializer.data.get("from_wallet"),
                                                        serializer.data.get("token_code"))
            to_token_wallet = get_entity_token_object(serializer.data.get("to_wallet"),
                                                      serializer.data.get("token_code"))

            if "WIRE_TRANSFER" == serializer.data.get("ops_type"):
                if from_token_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_token(from_token_wallet, to_token_wallet,
                                          serializer.data.get("amount"))
                    # TODO Add a callback to listen when this operation is over et get the status, the proceed...
                    # If the move operation didn't passed well, return bad request error
                    # TODO Here will be the start point of our trading service
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = save(serializer.data)
                    response_serializer = BaseOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a transfer operation"}, status=status.HTTP_400_BAD_REQUEST)


class TokenWithdrawOperationView(APIView):
    def post(self, request):
        serializer = WithdrawOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get from token wallet inside the request payload
            from_token_wallet = get_entity_token_object(serializer.data.get("from_wallet"),
                                                        serializer.data.get("token_code"))
            # An internal credit token wallet
            if serializer.data.get("to_wallet"):
                to_token_wallet = get_entity_token_object(serializer.data.get("to_wallet"),
                                                          serializer.data.get("token_code"))
            else:
                to_token_wallet = get_entity_token_object(config("WALLET_CREDIT_2", default=''),
                                                          serializer.data.get("token_code"))
            if "WITHDRAW" == serializer.data.get("ops_type"):
                if to_token_wallet:
                    # TODO Get external wallet address in the request body
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    # TODO Here will be the start point of our trading service
                    make_ops = move_token(from_token_wallet, to_token_wallet,
                                          serializer.data.get("amount"))
                    # TODO Add a callback to listen when this operation is over et get the status, the proceed...
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # TODO create a task for an external API withdrawal (we need to add blockchain operation here)
                    operation = save(serializer.data)
                    response_serializer = WithdrawOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a Withdraw Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a Withdraw operation"}, status=status.HTTP_400_BAD_REQUEST)

