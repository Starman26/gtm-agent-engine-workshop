import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


def test_update_prospect_refreshes_source_and_cached_profile():
    prospect_id = "LEAD-39002"
    technology = "Terraform"
    original_stack = list(data_service.PROSPECTS[prospect_id]["tech_stack"])
    original_profile = data_service._PROFILES.pop(prospect_id, None)

    try:
        cached_profile = build_prospect_profile.invoke({"prospect_id": prospect_id})
        assert technology not in cached_profile["prospect_profile"]["tech_stack"]

        result = data_service.update_prospect_info(prospect_id, technology)

        assert result["updated"] is True
        assert technology in data_service.fetch_tech_stack(prospect_id)
        rebuilt_profile = build_prospect_profile.invoke({"prospect_id": prospect_id})
        assert technology in rebuilt_profile["prospect_profile"]["tech_stack"]
    finally:
        data_service.PROSPECTS[prospect_id]["tech_stack"] = original_stack
        if original_profile is None:
            data_service._PROFILES.pop(prospect_id, None)
        else:
            data_service._PROFILES[prospect_id] = original_profile
