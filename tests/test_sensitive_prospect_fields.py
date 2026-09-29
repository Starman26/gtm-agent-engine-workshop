import json
import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")

from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


class SensitiveProspectFieldsTest(unittest.TestCase):
    def test_sensitive_fields_are_absent_from_prospect_tool_results(self):
        prospect_result = get_prospect.invoke({"prospect_id": "LEAD-12853"})
        profile_result = build_prospect_profile.invoke({"prospect_id": "LEAD-39002"})
        cached_profile_result = build_prospect_profile.invoke({"prospect_id": "LEAD-39002"})

        serialized_results = json.dumps(
            [prospect_result, profile_result, cached_profile_result]
        )
        for field in (
            "billing_qualification",
            "tax_id",
            "date_of_birth",
            "card_on_file",
            "credit_check_ref",
        ):
            self.assertNotIn(field, serialized_results)


if __name__ == "__main__":
    unittest.main()
