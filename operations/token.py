from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseOpSerializer, WithdrawOpSerializer
from .utils import *


class TokenTopUpOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get entity token objects
            # TODO Set from wallet from configuration file or env file
            from_token_wallet = get_entity_token_object(serializer.data.get("from_wallet"),
                                                        serializer.data.get("token_code"))
            to_token_wallet = get_entity_token_object(serializer.data.get("to_wallet"),
                                                      serializer.data.get("token_code"))

            if "TOP_UP" == serializer.data.get("ops_type"):
                if from_token_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_token(from_token_wallet, to_token_wallet,
                                          serializer.data.get("amount"))
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = save_operation(serializer.data)
                    response_serializer = BaseOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a topUp Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a Top up operation"}, status=status.HTTP_400_BAD_REQUEST)


class TokenWireTransferOperationView(APIView):
    def post(self, request):
        serializer = BaseOpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)

                    operation = save_operation(serializer.data)
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
            # TODO Set the destination wallet from configuration file or env file
            to_token_wallet = get_entity_token_object(serializer.data.get("to_wallet"),
                                                      serializer.data.get("token_code"))
            if "WITHDRAW" == serializer.data.get("ops_type"):
                if to_token_wallet:
                    # Move amount from origin entity token wallet to the destination entity token wallet
                    make_ops = move_token(from_token_wallet, to_token_wallet,
                                          serializer.data.get("amount"))
                    # If the move operation didn't passed well, return bad request error
                    if not make_ops:
                        return Response({"message": "The origin account hasn't enough amount"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    # TODO create a task for an external API withdrawal (we need to add blockchain operation here)
                    operation = save_operation(serializer.data)
                    response_serializer = WithdrawOpSerializer(operation)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                return Response({"message": "You need to create a Withdraw Wallet first"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Expected a Withdraw operation"}, status=status.HTTP_400_BAD_REQUEST)

