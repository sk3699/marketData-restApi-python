from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class PricesAndMarketAPITests(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.data = [
            {
                "option": "BRN",
                "delivery_month": "Apr24",
                "call_put": "call",
                "price": 400,
                "currency_units": "USD"
            },
            {
                "option": "HH",
                "delivery_month": "Sep24",
                "call_put": "call",
                "price": 300,
                "currency_units": "AUD"
            }
        ]
        self.url = "/markets/"

    def test_get_markets(self) -> None:
        test_data = self.data
        test_data[1].pop('price')
        res = self.client.post(self.url, test_data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
