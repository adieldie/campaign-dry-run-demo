from policy import PolicyEngine, PolicyStatus

class DryRunEngine:
    def __init__(self):
        self.policy_engine = PolicyEngine()

    def simulate_mutation(self, operation_type: str, plan: dict) -> dict:
        """
        Executa uma simulação (dry-run) da operação proposta e retorna o relatório de impacto.
        """
        # Checagem de campos obrigatórios para Campanha de Pesquisa Completa (Regra: Nunca inventar dados)
        required_fields = ["campaign_name", "ad_group_name", "budget_micros", "headlines", "descriptions", "keywords", "final_url"]
        missing_fields = [f for f in required_fields if not plan.get(f)]
        if missing_fields:
            return {
                "operation": operation_type,
                "dry_run": True,
                "proposed_changes": plan,
                "compliance": {
                    "status": "BLOCK",
                    "risk": "HIGH",
                    "reasons": [f"Parâmetros obrigatórios ausentes para campanha Search completa: {missing_fields}. Não é permitido inventar valores."],
                    "rules_checked": ["RequiredInputsCheck"]
                },
                "safety_status": "BLOCKED_BY_REQUIRED_INPUT",
                "can_proceed": False,
                "requires_confirmation": False
            }

        # Validate policy first
        policy_result = self.policy_engine.validate_campaign(plan)
        
        report = {
            "operation": operation_type,
            "dry_run": True,
            "proposed_changes": plan,
            "compliance": policy_result.to_dict(),
            "requires_confirmation": True
        }

        if policy_result.status == PolicyStatus.BLOCK:
            report["safety_status"] = "BLOCKED_BY_POLICY"
            report["can_proceed"] = False
        elif policy_result.status == PolicyStatus.REVIEW_REQUIRED:
            report["safety_status"] = "PENDING_HUMAN_REVIEW"
            report["can_proceed"] = False
        else:
            report["safety_status"] = "SIMULATION_PASSED"
            report["can_proceed"] = False

        return report


