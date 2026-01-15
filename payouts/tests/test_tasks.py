import uuid
from unittest.mock import patch

from rest_framework.test import APITestCase


class PayoutTaskTest(APITestCase):
    
    @patch('payouts.tasks.process_payout.delay')
    def test_payout_creation_triggers_task(self, mock_task):
        payload = {
            "amount": "150.00",
            "currency": "USD",
            "bank_details": "test bank",
        }
        
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post("/api/payouts/", payload, format="json")
            
            # check if API response success
        self.assertEqual(response.status_code, 201)
        
        # check if the task has been called only once
        self.assertTrue(mock_task.called)
        
        # check if the sent to task ID is correct
        payout_id = response.data['id']
        mock_task.assert_called_once_with(uuid.UUID(payout_id))
