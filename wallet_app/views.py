from rest_framework.response import Response
from .utils import success_response
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Wallet, Transactions
from .serializers import InitializeWalletSerializer, TransactionSerializer, WalletSerializer,VirtualMoneySerializer
from .services import initialize_user_and_customer, enable_wallet, disable_wallet,add_money,withdraw_money
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class InitializeWalletView(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission
    serializer_class = InitializeWalletSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        customer_xid = serializer.validated_data['customer_xid']
        token = initialize_user_and_customer(customer_xid)
        return success_response({"token": token})


class WalletStatusChangeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
         customer = user.customer
         wallet = enable_wallet(customer)
         serializer = WalletSerializer(wallet)
         return success_response(serializer.data)
        else:
            return Response({"error":"User is not authenticated"})

    def patch(self, request, *args, **kwargs):
        user = request.user
        customer = user.customer
        wallet = disable_wallet(customer)
        serializer = WalletSerializer(wallet)
        return success_response(serializer.data)


class WalletBalance(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class Transactions(APIView):
    serializer_class= TransactionSerializer

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        transactions = Transactions.objects.filter(wallet=wallet)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class AddMoney(APIView):
    serializer_class = VirtualMoneySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_authenticated:
         customer = user.customer
         data=request.data
         wallet = add_money(customer,data)
         serializer = WalletSerializer(wallet)
         return success_response(serializer.data)
        else:
            return Response({"error":"User is not authenticated"})

        

class Usemoney(APIView):
    serializer_class = VirtualMoneySerializer 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        customer = user.customer
        data=request.data
        wallet = withdraw_money(customer,data)
        serializer = WalletSerializer(wallet)
        return success_response(serializer.data)
        














