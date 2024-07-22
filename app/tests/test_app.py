import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, load_config, validate_config, get_last_log_entries
from unittest.mock import patch, mock_open
import json

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """Test the home route returns 200 and contains expected content."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Meds Consumption Logger', response.data)

    @patch('app.load_config')
    def test_push_button(self, mock_load_config):
        """Test the push_button route logs the action and returns success."""
        mock_load_config.return_value = {'email_enabled': True}
        response = self.app.post('/push_button', json={'send_email': True})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

    def test_validate_config(self):
        """Test the validate_config function with valid and invalid configs."""
        valid_config = {
            'sender_email': 'test@example.com',
            'recipient_email': 'recipient@example.com',
            'email_password': 'password123',
            'time_slots': ['14:00', '02:00'],
            'reminder_intervals': [60, 90, 180],
            'email_enabled': True
        }
        self.assertTrue(validate_config(valid_config))

        invalid_config = {
            'sender_email': 'test@example.com',
            'time_slots': ['14:00'],  # Missing one time slot
            'reminder_intervals': [60, 90, 180],
        }
        self.assertFalse(validate_config(invalid_config))

    @patch('builtins.open', new_callable=mock_open, read_data='2023-07-22 10:00:00\n2023-07-22 09:00:00\n')
    def test_get_last_log_entries(self, mock_file):
        """Test the get_last_log_entries function returns correct number of entries."""
        entries = get_last_log_entries(2)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0], '2023-07-22 10:00:00')
        self.assertEqual(entries[1], '2023-07-22 09:00:00')

if __name__ == '__main__':
    unittest.main()
