"""
Business Data Analysis Agent

- Created for analyzing daily sales and costs
- Simple state schema to mirror JSON-like data processing.
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph
import pytest

# State schema
class BusinessState(TypedDict):
    today_revenue: float
    today_cost: float
    today_customers: int
    yesterday_revenue: Optional[float]
    yesterday_cost: Optional[float]
    yesterday_customers: Optional[int]
    profit: Optional[float]
    revenue_change: Optional[float]
    cost_change: Optional[float]
    cac_today: Optional[float]
    cac_yesterday: Optional[float]
    cac_increase: Optional[float]
    profit_status: Optional[str]
    recommendations: Optional[list]
    alerts: Optional[list]

# input node
def input_data(state: BusinessState) -> dict:

    return state


def compute_metrics(state: BusinessState) -> dict:

    profit = state["today_revenue"] - state["today_cost"]

    # calculate changes
    revenue_change = None
    if state["yesterday_revenue"] and state["yesterday_revenue"] != 0:
        revenue_change = ((state["today_revenue"] - state["yesterday_revenue"]) / state["yesterday_revenue"]) * 100

    cost_change = None
    if state["yesterday_cost"] and state["yesterday_cost"] != 0:
        cost_change = ((state["today_cost"] - state["yesterday_cost"]) / state["yesterday_cost"]) * 100

    # CAC: cost per customer
    cac_today = None if state["today_customers"] == 0 else state["today_cost"] / state["today_customers"]
    cac_yesterday = None if state["yesterday_customers"] == 0 else state["yesterday_cost"] / state["yesterday_customers"]


    cac_increase = None
    if cac_today and cac_yesterday and cac_yesterday != 0:
        cac_increase = ((cac_today - cac_yesterday) / cac_yesterday) * 100

    return {
        "profit": profit,
        "revenue_change": revenue_change,
        "cost_change": cost_change,
        "cac_today": cac_today,
        "cac_yesterday": cac_yesterday,
        "cac_increase": cac_increase,
    }

# Recommendation node: generates business advice
def generate_advice(state: BusinessState) -> dict:
    recs = []
    alerts = []


    profit_status = "profit" if state["profit"] >= 0 else "loss"


    if state["profit"] is not None and state["profit"] < 0:
        recs.append("Reduce costs if profit is negative.")
        alerts.append("Warning: Negative profit detected.")

    if state["cac_increase"] is not None and state["cac_increase"] > 20:
        recs.append("Review marketing campaigns if CAC increased significantly.")
        alerts.append("Alert: CAC increased by more than 20%.")

    if state["revenue_change"] is not None and state["revenue_change"] > 0:
        recs.append("Consider increasing advertising budget if sales are growing.")

    if not recs:
        recs.append("Metrics stable. Continue current strategy.")

    return {
        "profit_status": profit_status,
        "recommendations": recs,
        "alerts": alerts
    }

#graph
graph = StateGraph(BusinessState)
graph.add_node("input", input_data)
graph.add_node("metrics", compute_metrics)
graph.add_node("advice", generate_advice)
graph.add_edge("input", "metrics")
graph.add_edge("metrics", "advice")
graph.set_entry_point("input")
compiled_graph = graph.compile()

# Tests
@pytest.fixture
def business_graph():
    return compiled_graph

def test_profitable_day(business_graph):
    """Test a day with profit and sales growth, like validating a model"""
    input_data = {
        "today_revenue": 12000.0,
        "today_cost": 8000.0,
        "today_customers": 100,
        "yesterday_revenue": 10000.0,
        "yesterday_cost": 7000.0,
        "yesterday_customers": 80,
    }
    result = business_graph.invoke(input_data)
    assert result["profit"] == 4000.0, "Profit calculation incorrect"
    assert result["profit_status"] == "profit", "Profit status incorrect"
    assert "Consider increasing advertising budget if sales are growing." in result["recommendations"], "Sales growth recommendation missing"
    assert result["alerts"] == [], "Unexpected alerts"

def test_loss_day(business_graph):
    """Test a loss scenario, ensuring alerts trigger"""
    input_data = {
        "today_revenue": 6000.0,
        "today_cost": 8000.0,
        "today_customers": 40,
        "yesterday_revenue": 9000.0,
        "yesterday_cost": 7000.0,
        "yesterday_customers": 45,
    }
    result = business_graph.invoke(input_data)
    assert result["profit"] == -2000.0, "Profit calculation incorrect"
    assert result["profit_status"] == "loss", "Profit status incorrect"
    assert "Reduce costs if profit is negative." in result["recommendations"], "Loss recommendation missing"
    assert "Warning: Negative profit detected." in result["alerts"], "Loss alert missing"

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
    assert result["cac_today"] == 500.0, "CAC today incorrect"
    assert result["cac_yesterday"] == 100.0, "CAC yesterday incorrect"
    assert result["cac_increase"] == 400.0, "CAC increase incorrect"
    assert "Review marketing campaigns if CAC increased significantly." in result["recommendations"], "CAC recommendation missing"
    assert "Alert: CAC increased by more than 20%." in result["alerts"], "CAC alert missing"

if __name__ == "__main__":
    print("Quick validation tests:")
    test_profitable_day(compiled_graph)
    test_loss_day(compiled_graph)
    test_high_cac_day(compiled_graph)
    print("All manual tests passed! Ready for LangGraph Studio.")