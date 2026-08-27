import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
from gtm_agent.gtm_agent import send_prospect_email


class SendProspectEmailTest(unittest.TestCase):
    def test_disqualified_prospect_is_blocked(self):
        result = send_prospect_email.func(
            {"name": "Test Prospect", "email": "test@example.com", "disqualified": True},
            "Subject",
            "Body",
            runtime=None,
        )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(
            result["reason"],
            "Prospect is flagged disqualified; explicit rep confirmation required.",
        )
