from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


def test_prospect_tools_do_not_return_billing_qualification():
    prospect = get_prospect.invoke({"prospect_id": "LEAD-50002"})
    profile = build_prospect_profile.invoke({"prospect_id": "LEAD-50002"})

    assert "billing_qualification" not in prospect["prospect"]
    assert "billing_qualification" not in profile["prospect_profile"]
