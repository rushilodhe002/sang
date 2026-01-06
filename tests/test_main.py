from fastapi.testclient import TestClient
from app.main import app
from app.rule_engine import RuleEngine

client = TestClient(app)

def test_health_check():
    """Week 1 Requirement: Health Check Endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

def test_rule_engine_high_risk():
    """Week 3 Requirement: High Risk Rule (> 5000)"""
    engine = RuleEngine()
    result = engine.evaluate({"amount": 6000})
    assert result["status"] == "flagged"
    assert result["risk_score"] == 0.85

def test_rule_engine_safe_transaction():
    """Week 3 Requirement: Safe Transaction (< 1000)"""
    engine = RuleEngine()
    result = engine.evaluate({"amount": 500})
    assert result["status"] == "approved"
    assert result["risk_score"] == 0.05
