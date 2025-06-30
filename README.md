

Business Data Analysis Agent
Overview
A LangGraph agent for analyzing daily business data (sales, costs, customers) and generating actionable recommendations. Built with my AI and NLP background, focusing on structured data processing similar to JSON pipelines.
Features

Input: Daily revenue, cost, customers, and optional previous-day data.
Processing: Computes profit, revenue/cost changes, and Customer Acquisition Cost (CAC).
Output: Dictionary with profit_status, alerts, and recommendations.
Tests: pytest tests for profitable, loss, and high-CAC scenarios.

Setup

Install dependencies:pip install langgraph pytest


Run tests:pytest agent2.py


Run manually:python agent2.py



LangGraph Studio

Import agent2.py into LangGraph Studio.
Test with sample input:{
    "today_revenue": 12000.0,
    "today_cost": 8000.0,
    "today_customers": 100,
    "yesterday_revenue": 10000.0,
    "yesterday_cost": 7000.0,
    "yesterday_customers": 80
}



Submission

Files: agent2.py, README.md
GitHub: [Insert your repo URL]
Telegram: Submit with title "Studio"
