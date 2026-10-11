import unittest
from dry_run import DryRunEngine
from demo import sample_plan
class Tests(unittest.TestCase):
    def test_missing_fields(self):
        self.assertEqual(DryRunEngine().simulate_mutation("preview",{})["safety_status"],"BLOCKED_BY_REQUIRED_INPUT")
    def test_preview_never_authorizes_execution(self):
        result=DryRunEngine().simulate_mutation("preview",sample_plan())
        self.assertEqual(result["safety_status"],"SIMULATION_PASSED")
        self.assertFalse(result["can_proceed"])
        self.assertTrue(result["requires_confirmation"])
    def test_restricted(self):
        plan=sample_plan();plan["keywords"]=["vinho"]
        self.assertEqual(DryRunEngine().simulate_mutation("preview",plan)["safety_status"],"PENDING_HUMAN_REVIEW")
    def test_block(self):
        plan=sample_plan();plan["keywords"]=["tabaco"]
        self.assertEqual(DryRunEngine().simulate_mutation("preview",plan)["safety_status"],"BLOCKED_BY_POLICY")
if __name__ == "__main__": unittest.main()
