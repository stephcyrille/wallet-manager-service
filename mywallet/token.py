from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Token, EntityToken, Wallet
from .serializers import ActivateTokenRequestSerializer, EntityTokenSerializer


class ActivateUserTokenView(APIView):
    def get_token_object(self, token_ref):
        try:
            return Token.objects.get(ref=token_ref)
        except Token.DoesNotExist:
            return ""

    def get_user_wallet_object(self, wallet_ref, user_ref):
        try:
            return Wallet.objects.get(owner_ref=user_ref, ref=wallet_ref)
        except Wallet.DoesNotExist:
            return ""

    def get_user_token_object(self, token_ref, user_ref):
        try:
            return EntityToken.objects.get(token_ref=token_ref, owner_ref=user_ref)
        except EntityToken.DoesNotExist:
            return ""

    def post(self, request):
        serializer = ActivateTokenRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = self.get_token_object(serializer.data["token_ref"])
            if token:
                user_token = self.get_user_token_object(serializer.data["token_ref"], serializer.data["owner_ref"])
                if not user_token:
                    # Check if it's a user Wallet
                    user_wallet = self.get_user_wallet_object(serializer.data["wallet_ref"],
                                                              serializer.data["owner_ref"])
                    if user_wallet:
                        # Create a userToken instance
                        data = {
                            "token_symbol": token.symbol,
                            "token_ref": serializer.data["token_ref"],
                            "wallet_ref": serializer.data["wallet_ref"],
                            "owner_ref": serializer.data["owner_ref"],
                            "is_active": True,
                            "activated_date": timezone.now(),
                        }
                        new_user_token = EntityToken.objects.create(**data)
                        response_serializer = EntityTokenSerializer(new_user_token)
                        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message": "We cannot activate the user token because it isn't the specified "
                                                    "user wallet"}, status=status.HTTP_404_NOT_FOUND)
                elif not user_token.is_active:
                    user_token.is_active = True
                    user_token.activated_date = timezone.now()
                    user_token.save()
                    response_serializer = EntityTokenSerializer(user_token)
                    return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({"message": "The User token is already created"},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({"message": "We cannot activate the user token because the token isn't found"},
                            status=status.HTTP_404_NOT_FOUND)
