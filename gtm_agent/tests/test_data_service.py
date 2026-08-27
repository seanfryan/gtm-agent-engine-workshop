import sys
import types
import unittest
from pathlib import Path

package_root = Path(__file__).resolve().parents[1]
package = types.ModuleType("gtm_agent")
package.__path__ = [str(package_root)]
sys.modules["gtm_agent"] = package

from gtm_agent import data_service


class UpdateProspectInfoTest(unittest.TestCase):
    def test_update_persists_technology_and_invalidates_profile(self):
        prospect_id = "LEAD-39002"
        original_tech_stack = data_service.PROSPECTS[prospect_id]["tech_stack"]
        original_profile = data_service._PROFILES.get(prospect_id)
        data_service._PROFILES[prospect_id] = {
            "prospect_id": prospect_id,
            "tech_stack": list(original_tech_stack),
        }

        try:
            result = data_service.update_prospect_info(prospect_id, "Kafka")

            self.assertTrue(result["updated"])
            self.assertIn("Kafka", data_service.fetch_tech_stack(prospect_id))
            profile = data_service.get_profile_from_db(prospect_id)["prospect_profile"]
            self.assertTrue(profile is None or "Kafka" in profile["tech_stack"])
        finally:
            data_service.PROSPECTS[prospect_id]["tech_stack"] = original_tech_stack
            if original_profile is None:
                data_service._PROFILES.pop(prospect_id, None)
            else:
                data_service._PROFILES[prospect_id] = original_profile
