from django.db import models
from django.contrib.auth.models import User
from .constants import WalletTransactionType
from django.core import exceptions


class GetInstanceMixin(object):
    def get_or_none(self, **kwargs):
        """Extends get to return None if no object is found based on query."""
        try:

            instance = self.get(**kwargs)
            return instance
        except exceptions.ObjectDoesNotExist:
            return None


class TimeStampedModel(models.Model):
    cdate = models.DateTimeField(auto_now_add=True)
    udate = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class CustomerManager(models.Manager, GetInstanceMixin):
    pass


class Customer(TimeStampedModel):
    customer_id = models.AutoField(db_column='customer_id', primary_key=True)
    customer_xid = models.TextField(unique=True, db_index=True, db_column='customer_xid')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, db_column='user_id')
    objects = CustomerManager()

    class Meta(object):
        db_table = 'customer'


class WalletManager(models.Manager, GetInstanceMixin):
    pass


class Wallet(TimeStampedModel):
    id = models.AutoField(max_length=10, primary_key=True, db_column='wallet_id')
    owned_by = models.OneToOneField(Customer, models.DO_NOTHING, db_column='owned_by_id')
    status = models.BooleanField(default=False, db_column='status')
    enabled_at = models.DateTimeField()
    balance = models.FloatField(max_length=20, default=0)
    objects = WalletManager()

    class Meta(object):
        db_table = 'wallet'


class TransactionManager(models.Manager, GetInstanceMixin):
    pass


class Transactions(TimeStampedModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, db_column='wallet_id')
    transaction_type = models.CharField(choices=(
        (WalletTransactionType.WITHDRAWAL, WalletTransactionType.WITHDRAWAL),
        (WalletTransactionType.DEPOSIT, WalletTransactionType.DEPOSIT)
    ),
        db_column='transaction_type', max_length=30
    )
    amount = models.FloatField(max_length=20)
    transacted_at = models.DateTimeField(auto_now_add=True)
    objects = TransactionManager()

    class Meta(object):
        db_table = 'transactions'
