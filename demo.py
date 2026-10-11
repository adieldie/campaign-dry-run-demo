from dry_run import DryRunEngine
from pprint import pprint

def sample_plan():
    return {"campaign_name":"Campanha fictícia", "ad_group_name":"Papelaria demonstrativa",
            "budget_micros":1000000, "headlines":["Cadernos de exemplo"],
            "descriptions":["Plano fictício para teste local"], "keywords":["papelaria"],
            "final_url":"https://example.invalid/demo"}
if __name__ == "__main__": pprint(DryRunEngine().simulate_mutation("preview",sample_plan()))
