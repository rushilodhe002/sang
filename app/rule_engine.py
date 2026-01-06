class RuleEngine:
    def __init__(self):
        pass

    def evaluate(self, transaction_data: dict) -> dict:
        """
        Evaluate transaction against static rules.
        Returns a dict with 'status' and 'risk_score'.
        """
        amount = transaction_data.get("amount", 0)
        
        # Rule 1: High Value Transaction
        if amount > 5000:
            return {"status": "flagged", "risk_score": 0.85, "reason": "Amount exceeds 5000 limit"}
        
        # Rule 2: Moderate Value but Safe
        if 1000 <= amount <= 5000:
            return {"status": "approved", "risk_score": 0.30, "reason": "Moderate value"}
        
        # Default: Safe
        return {"status": "approved", "risk_score": 0.05, "reason": "Low risk"}
