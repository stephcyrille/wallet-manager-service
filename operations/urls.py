from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .token import TokenTopUpOperationView, TokenWireTransferOperationView, TokenWithdrawOperationView
from .fiat import FiatTopUpOperationView, FiatWireTransferOperationView, FiatWithdrawOperationView

urlpatterns = [
    # Token operations
    path('token/topup/', TokenTopUpOperationView.as_view()),
    path('token/wire-transfer/', TokenWireTransferOperationView.as_view()),
    path('token/withdraw/', TokenWithdrawOperationView.as_view()),

    # Fiat operations
    path('fiat/topup/', FiatTopUpOperationView.as_view()),
    path('fiat/wire-transfer/', FiatWireTransferOperationView.as_view()),
    path('fiat/withdraw/', FiatWithdrawOperationView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
