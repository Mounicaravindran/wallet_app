from django.urls import path
from .views import *

urlpatterns = [
    path('init/', InitializeWalletView.as_view()),
    path('wallet/', WalletStatusChangeView.as_view()),
    path('wallet/deposits/',AddMoney.as_view()),
    path('wallet/withdraw/',Usemoney.as_view()),
    path('wallet/transactions/',Transactions.as_view()),
    # path('enable-wallet/', EnableWallet.as_view(), name='enable_wallet'),
    # path('view-balance/', WalletBalance.as_view(),name='view_balance'),
    # path('view-transactions/',WalletTransactions.as_view(),name='view_transactions'),
    # path('add-money/',AddMoney.as_view(),name='add_money'),
    # path('withdraw-money/',Usemoney.as_view(),name='withdraw_money'),
    # path('disable-wallet/',Disablewallet.as_view(),name='disable_wallet'),
]