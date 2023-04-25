from .models import Customer, Wallet
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import transaction


def initialize_user_and_customer(customer_xid):
    customer = Customer.objects.get_or_none(customer_xid=customer_xid)
    if customer:
        return "Failed"
    with transaction.atomic():
        user = User.objects.create_user(
            username=customer_xid)
        customer, _ = Customer.objects.get_or_create(
            customer_xid=customer_xid,
            user=user
        )
        wallet, _ = Wallet.objects.get_or_create(
            owned_by=customer,
            status=True,
            enabled_at=timezone.now()
        )
        token = Token.objects.create(user=user)
    return token.key


def enable_wallet(customer):
    with transaction.atomic():
        wallet = Wallet.objects.get_or_none(owned_by=customer)
        if not wallet:
            raise ValueError()
        if not wallet.status:
            wallet.status = True
            wallet.enabled_at = timezone.now()
            wallet.save()
    return wallet


def disable_wallet(customer):
    with transaction.atomic():
        wallet = Wallet.objects.get_or_none(owned_by=customer)
        if not wallet:
            raise ValueError()
        if wallet.status:
            wallet.status = False
            wallet.save()
    return wallet

def add_money(customer,data):
    with transaction.atomic():
        wallet = Wallet.objects.get_or_none(owned_by=customer)
        if not wallet:
            raise ValueError()
        if wallet.status==False:
            raise Exception("Wallet is disabled,please enable wallet to add money")
        wallet.balance+=data["amount"]
        wallet.save()
    return wallet

def withdraw_money(customer,data):
    with transaction.atomic():
        wallet = Wallet.objects.get_or_none(owned_by=customer)
        if not wallet:
            raise ValueError()
        if wallet.status==False:
            raise Exception("Wallet is disabled,please enable wallet to add money")
        if wallet.balance< data["amount"]:
            return("Insufficient balance")
        wallet.balance-=data["amount"]
        wallet.save()
    return wallet

