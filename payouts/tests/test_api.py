import uuid
from decimal import Decimal

from rest_framework.test import APITestCase

from payouts.models import Payouts


class PayoutApiTest(APITestCase):
    def setUp(self):
        # Create an initial record for GET and Detail tests
        self.payout = Payouts.objects.create(
            amount=Decimal('50.00'),
            currency='USD',
            bank_details='Initial bank details for testing'
        )
        self.list_url = "/api/payouts/"
        self.detail_url = f"/api/payouts/{self.payout.id}/"

    def test_get_non_existent_payout_returns_json_404(self) -> None:
        """
        Ensure that requesting a non-existent UUID returns a JSON 404 response.
        """
        # Generate a random UUID that definitely isn't in the database
        random_id = uuid.uuid4()
        response = self.client.get(f"/api/payouts/{random_id}/")

        # 1. Check status code
        self.assertEqual(response.status_code, 404)
        # 2. Ensure the response is JSON, not HTML
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        # 3. Check the error message format
        self.assertEqual(str(response.data['detail']), 'No Payouts matches the given query.')

    def test_invalid_uuid_format_returns_json_404(self) -> None:
        """
        Ensure that a malformed ID (not a UUID) also returns a JSON 404.
        This tests our re_path 'catch-all' logic in config/urls.py.
        """
        response = self.client.get("/api/payouts/not-a-valid-uuid/")
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_list_payouts(self):
        """Ensure we can retrieve the list of payouts."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_payout(self):
        """Ensure we can retrieve a specific payout by ID."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], '50.00')

    def test_create_payout_valid_data(self):
        """Test successful creation with valid data."""
        payload = {
            "amount": "120.50",
            "currency": "EUR",
            "bank_details": "Standard bank details format"
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payouts.objects.count(), 2)

    def test_create_payout_invalid_amount(self):
        """Validation: Negative amount should return 400."""
        payload = {"amount": "-5.00", "currency": "USD", "bank_details": "Valid bank details"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('amount', response.data)

    def test_create_payout_invalid_currency(self):
        """Validation: Incorrect currency format."""
        payload = {"amount": "10.00", "currency": "USDT", "bank_details": "Valid bank details"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_payout_missing_fields(self):
        """Validation: Missing required fields."""
        payload = {"amount": "10.00"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, 400)
