from celery import shared_task 
from .services import enable_wallet,disable_wallet,add_money,withdraw_money

@shared_task
def perform_external_call():
       enable_wallet()
       add_money()
       withdraw_money()
       disable_wallet()