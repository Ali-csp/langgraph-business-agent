
from typing import TypedDict, Optional
from langgraph.graph import StateGraph

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

# Input node
def input_data(state: BusinessState) -> dict:
    required = ["today_revenue", "today_cost", "today_customers"]
    for field in required:
        if field not in state:
            raise ValueError(f"Missing required input field: {field}")
    return state


def compute_metrics(state: BusinessState) -> dict:
    profit = state["today_revenue"] - state["today_cost"]

    revenue_change = None
    if state.get("yesterday_revenue") is not None and state["yesterday_revenue"] != 0:
        revenue_change = ((state["today_revenue"] - state["yesterday_revenue"]) / state["yesterday_revenue"]) * 100

    cost_change = None
    if state.get("yesterday_cost") is not None and state["yesterday_cost"] != 0:
        cost_change = ((state["today_cost"] - state["yesterday_cost"]) / state["yesterday_cost"]) * 100

    cac_today = None if state["today_customers"] == 0 else state["today_cost"] / state["today_customers"]

    if (
        state.get("yesterday_cost") is not None
        and state.get("yesterday_customers") is not None
        and state["yesterday_customers"] != 0
    ):
        cac_yesterday = state["yesterday_cost"] / state["yesterday_customers"]
    else:
        cac_yesterday = None

    cac_increase = None
    if cac_today is not None and cac_yesterday is not None and cac_yesterday != 0:
        cac_increase = ((cac_today - cac_yesterday) / cac_yesterday) * 100

    return {
        "profit": profit,
        "revenue_change": revenue_change,
        "cost_change": cost_change,
        "cac_today": cac_today,
        "cac_yesterday": cac_yesterday,
        "cac_increase": cac_increase,
    }

# Recommendation node
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


graph = StateGraph(BusinessState)
graph.add_node("input", input_data)
graph.add_node("metrics", compute_metrics)
graph.add_node("advice", generate_advice)
graph.add_edge("input", "metrics")
graph.add_edge("metrics", "advice")
graph.set_entry_point("input")
compiled_graph = graph.compile()
