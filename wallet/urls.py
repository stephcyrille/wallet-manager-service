from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import wallet, token

urlpatterns = [
    path('create/', wallet.CreateWalletView.as_view()),
    path('detail/<str:owner_ref>', wallet.DetailWalletView.as_view()),
    path('activate/', wallet.ActivateWalletView.as_view()),
    path('token/activate/', token.ActivateUserTokenView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
