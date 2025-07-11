# Business Data Analysis Agent

## Overview
A LangGraph agent for analyzing daily business data (sales, costs, customers) and generating actionable recommendations. Built with my AI and NLP background, focusing on structured data processing similar to JSON pipelines.

## Features
- **Input**: Daily revenue, cost, customers, and optional previous-day data.
- **Processing**: Computes profit, revenue/cost changes, and Customer Acquisition Cost (CAC).
- **Output**: Dictionary with `profit_status`, `alerts`, and `recommendations`.
- **Tests**: `pytest` tests for profitable, loss, and high-CAC scenarios.

## Setup
1. Install dependencies:
   ```bash
   pip install langgraph pytest
   ```
2. Run tests:
   ```bash
   pytest agent.py
   ```
3. Run manually:
   ```bash
   python agent.py
   ```

## LangGraph Studio
- Import `agent2.py` into LangGraph Studio.
- Test with sample input:
  ```json
  {
      "today_revenue": 12000.0,
      "today_cost": 8000.0,
      "today_customers": 100,
      "yesterday_revenue": 10000.0,
      "yesterday_cost": 7000.0,
      "yesterday_customers": 80
  }
  ```

