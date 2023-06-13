from django.urls import path
from .views import *

urlpatterns = [
    path('init/', InitializeWalletView.as_view()),
    path('wallet/', WalletStatusChangeView.as_view()),
    path('wallet/deposits/',AddMoney.as_view()),
    path('wallet/withdraw/',Usemoney.as_view()),
    path('wallet/transactions/',Transactions.as_view()),
    
]