
import pytest
from agent import compiled_graph

@pytest.fixture
def business_graph():
    return compiled_graph

def test_profitable_day(business_graph):
    input_data = {
        "today_revenue": 12000.0,
        "today_cost": 8000.0,
        "today_customers": 100,
        "yesterday_revenue": 10000.0,
        "yesterday_cost": 7000.0,
        "yesterday_customers": 80,
    }
    result = business_graph.invoke(input_data)
    assert result["profit"] == 4000.0
    assert result["profit_status"] == "profit"
    assert "Consider increasing advertising budget if sales are growing." in result["recommendations"]
    assert result["alerts"] == []

def test_loss_day(business_graph):
    input_data = {
        "today_revenue": 6000.0,
        "today_cost": 8000.0,
        "today_customers": 40,
        "yesterday_revenue": 9000.0,
        "yesterday_cost": 7000.0,
        "yesterday_customers": 45,
    }
    result = business_graph.invoke(input_data)
    assert result["profit"] == -2000.0
    assert result["profit_status"] == "loss"
    assert "Reduce costs if profit is negative." in result["recommendations"]
    assert "Warning: Negative profit detected." in result["alerts"]

def test_high_cac_day(business_graph):
    input_data = {
        "today_revenue": 10000.0,
        "today_cost": 10000.0,
        "today_customers": 20,
        "yesterday_revenue": 10000.0,
        "yesterday_cost": 5000.0,
        "yesterday_customers": 50,
    }
    result = business_graph.invoke(input_data)
    assert result["cac_today"] == 500.0
    assert result["cac_yesterday"] == 100.0
    assert result["cac_increase"] == 400.0
    assert "Review marketing campaigns if CAC increased significantly." in result["recommendations"]
    assert "Alert: CAC increased by more than 20%." in result["alerts"]

def test_no_previous_data(business_graph):
    input_data = {
        "today_revenue": 12000.0,
        "today_cost": 8000.0,
        "today_customers": 100,
        "yesterday_revenue": None,
        "yesterday_cost": None,
        "yesterday_customers": None,
    }
    result = business_graph.invoke(input_data)
    assert result["profit"] == 4000.0
    assert result["profit_status"] == "profit"
    assert result["revenue_change"] is None
    assert result["cost_change"] is None
    assert result["cac_increase"] is None
    assert "Metrics stable. Continue current strategy." in result["recommendations"]
    assert result["alerts"] == []
