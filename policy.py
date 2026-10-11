from enum import Enum
from typing import List, Dict, Any

class PolicyStatus(Enum):
    PASS = "PASS"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCK = "BLOCK"

class PolicyResult:
    def __init__(self, status: PolicyStatus, risk: str, reasons: List[str], rules_checked: List[str]):
        self.status = status
        self.risk = risk
        self.reasons = reasons
        self.rules_checked = rules_checked

    def to_dict(self):
        return {
            "status": self.status.value,
            "risk": self.risk,
            "reasons": self.reasons,
            "rules_checked": self.rules_checked
        }

class PolicyEngine:
    def __init__(self):
        self.prohibited_keywords = ["cigarro", "tabaco", "fumar", "vape", "charuto", "nicotina"]
        
        self.restricted_keywords = ["cerveja", "vinho", "cachaça", "álcool", "chopp", "licor"]
        
        self.banned_claims = [
            "cura ressaca", "relaxe", "dirigir", "fique bebado", "menores",
            "rolê resolvido", "role resolvido", "combinação irresistível", "combinacao irresistivel",
            "encher a cara", "beba até cair", "sucesso social", "anti-stress", "carro", "trânsito"
        ]

    def _extract_text_fields(self, plan: Dict[str, Any]) -> str:
        """
        Extrai campos de texto estruturados relevantes do plano de campanha
        (headlines, descrições, palavras-chave) em vez de usar str() no objeto inteiro.
        """
        texts = []
        for key, value in plan.items():
            if isinstance(value, str):
                texts.append(value.lower())
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, str):
                        texts.append(v.lower())
        return " ".join(texts)

    def validate_campaign(self, plan: Dict[str, Any]) -> PolicyResult:
        reasons = []
        rules_checked = ["IllustrativeProductRule", "IllustrativeClaimsRule", "IllustrativeFormatRule"]
        status = PolicyStatus.PASS
        risk = "LOW"

        all_text = self._extract_text_fields(plan)
        channel_type = str(plan.get("advertising_channel_type", plan.get("channel", "SEARCH"))).upper()

        for word in self.prohibited_keywords:
            if word in all_text:
                return PolicyResult(
                    PolicyStatus.BLOCK, 
                    "HIGH", 
                    [f"Regra demonstrativa de produto: '{word}' é expressamente proibido."], 
                    rules_checked
                )

        for claim in self.banned_claims:
            if claim in all_text:
                return PolicyResult(
                    PolicyStatus.BLOCK,
                    "HIGH",
                    [f"Regra demonstrativa de texto: '{claim}' não é permitida em anúncios de bebidas."],
                    rules_checked
                )

        restricted_found = [w for w in self.restricted_keywords if w in all_text]
        if restricted_found:
            if "PERFORMANCE_MAX" in channel_type or "PMAX" in channel_type:
                return PolicyResult(
                    PolicyStatus.BLOCK,
                    "HIGH",
                    ["Formato solicitado bloqueado pela regra ilustrativa desta demonstração."],
                    rules_checked
                )

            status = PolicyStatus.REVIEW_REQUIRED
            risk = "MEDIUM"
            reasons.append(f"Regra demonstrativa: termo restrito ({restricted_found}). Revisão humana necessária.")

        return PolicyResult(status, risk, reasons, rules_checked)


