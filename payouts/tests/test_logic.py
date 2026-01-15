from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from payouts.models import Payouts
from payouts.tasks import process_payout


class PayoutLogicTest(TestCase):
    def test_payout_initial_status(self):
        """Unit: Check that default status is 'pending'."""
        payout = Payouts.objects.create(
            amount=Decimal('10.00'),
            currency='USD',
            bank_details='Checking initial status logic'
        )
        self.assertEqual(payout.status, 'CREATED')

    @patch('payouts.tasks.process_payout.delay')
    def test_celery_task_called(self, mock_delay):
        """Integration: Task should be triggered by the view (mocked)."""
        # Note: We trigger this via API because perform_create is in the view
        from rest_framework.test import APIClient
        client = APIClient()
        data = {"amount": "10.00", "currency": "USD", "bank_details": "Bank details for celery test"}
        with self.captureOnCommitCallbacks(execute=True):
            client.post("/api/payouts/", data, format="json")
        
        self.assertTrue(mock_delay.called)

    def test_task_execution_logic(self):
        """Logic: Test the actual task function (synchronously)."""
        payout = Payouts.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            bank_details='Task execution test'
        )
        
        # Run task synchronously (without delay) for testing
        process_payout(payout.id)
        
        # Refresh from DB and check status
        payout.refresh_from_db()
        self.assertEqual(payout.status, 'processed')
