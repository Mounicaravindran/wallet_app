from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from .serializers import InitializeWalletSerializer
from .views import InitializeWalletView
import unittest
from wallet_app import views
from django.urls import reverse
from rest_framework import status
# Create your tests here.

class InitializeWalletViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/initialize-wallet/'
        self.valid_payload = {'customer_xid': ''}

    def test_post_method(self):
        view = InitializeWalletView.as_view()
        serializer = InitializeWalletSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())
        response = self.client.post(self.url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('token', response.data.keys())



class WalletStatusChangeViewTestCase(APITestCase):

 def test_wallet_enable(self):
        url = reverse('wallet-status')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enabled'], True)

 def test_wallet_disable(self):
        url = reverse('wallet-status')
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['enabled'], False)

    
    