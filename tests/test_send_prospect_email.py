import os
import unittest
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTests(unittest.TestCase):
    def test_disqualified_prospect_is_blocked_without_message_id(self):
        result = send_prospect_email.func(
            {
                "prospect_id": "LEAD-50001",
                "email": "priya@example.com",
                "disqualified": False,
            },
            "Pricing deck",
            "Here is the pricing deck.",
            SimpleNamespace(config={}),
            {"email": "rep@example.com", "name": "Rep"},
        )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["reason"], "prospect_disqualified")
        self.assertNotIn("message_id", result)

    def test_non_disqualified_prospect_is_sent(self):
        result = send_prospect_email.func(
            {"prospect_id": "LEAD-12853", "email": "omar@example.com"},
            "Follow-up",
            "Following up as requested.",
            SimpleNamespace(config={}),
            {"email": "rep@example.com", "name": "Rep"},
        )

        self.assertEqual(result["status"], "sent")
        self.assertIn("message_id", result)


if __name__ == "__main__":
    unittest.main()
