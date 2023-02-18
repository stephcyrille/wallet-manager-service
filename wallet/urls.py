from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from wallet.apis.token import ActivateUserTokenView
from wallet.apis.wallet import CreateWalletView, DetailWalletView, ActivateWalletView

urlpatterns = [
    path('create/', CreateWalletView.as_view()),
    path('detail/<str:owner_ref>', DetailWalletView.as_view()),
    path('activate/', ActivateWalletView.as_view()),
    path('token/activate/', ActivateUserTokenView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
