from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Wallet
from .serializers import BaseWalletSerializer, WalletSerializer


class CreateWalletView(APIView):
    def post(self, request):
        serializer = BaseWalletSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Create data object to save in the database
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailWalletView(APIView):
    def get_object(self, owner_ref):
        try:
            return Wallet.objects.get(owner_ref=owner_ref)
        except Wallet.DoesNotExist:
            return ""

    def get(self, request, owner_ref, format=None):
        data = {"owner_ref": owner_ref}
        get_serializer = BaseWalletSerializer(data=data)
        if get_serializer.is_valid(raise_exception=True):
            # Create data object to save in the database
            wallet = self.get_object(owner_ref)
            if wallet:
                serializer = WalletSerializer(wallet)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Resource is not found"}, status=status.HTTP_404_NOT_FOUND)


class ActivateWalletView(APIView):
    def get_object(self, owner_ref):
        try:
            return Wallet.objects.get(owner_ref=owner_ref)
        except Wallet.DoesNotExist:
            return ""

    def post(self, request):
        serializer = BaseWalletSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            wallet = self.get_object(serializer.data.get("owner_ref"))
            if wallet and not wallet.is_active:
                wallet.activated_date = timezone.now()
                wallet.is_active = True
                wallet.code_client = '1101'
                wallet.ref = '%s%s' % (wallet.ref, '1101')
                wallet.save()
                response_serializer = BaseWalletSerializer(wallet)
                return Response(response_serializer.data, status=status.HTTP_202_ACCEPTED)
            elif wallet and wallet.is_active:
                return Response({"message": "The wallet is already activated"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"message": "We cannot activate wallet because the resource is not found"},
                                status=status.HTTP_404_NOT_FOUND)
